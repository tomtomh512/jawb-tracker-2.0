import asyncio

from llm.manager import LLMManager
from schemas.llm.rubric import Rubric, ScoredRubricItem, RubricItem, ScoredRubricItemLLMOutput, ScoredRubric
from utils.normalize_weights import normalize_weights

semaphore = asyncio.Semaphore(2)


async def generate_rubric(
        llm: LLMManager,
        job_posting: str
) -> Rubric:
    prompt = f"""
                Imagine you are the hiring manager reviewing resumes.
                Create an evaluation rubric that represents how candidates should be scored.
                The rubric should prioritize characteristics that distinguish strong candidates, not merely restate every listed requirement.
                Use between 5 and 10 evaluation categories.
                Each category should represent a meaningful hiring dimension rather than an individual skill.

                Do NOT create categories such as, but not limited to:
                - Communication
                - Teamwork
                - Problem Solving
                - Education

                unless those are clearly primary hiring criteria.

                Job Posting:
                {job_posting}
            """

    result = await llm.async_prompt(
        prompt=prompt,
        output_model=Rubric,
        temperature=0.2,
        log_message="Generating rubric"
    )

    return result


async def score_rubric_item(
        llm: LLMManager,
        rubric_item: RubricItem,
        resume: str,
        weight: float,
) -> ScoredRubricItem:
    async with semaphore:
        prompt = f"""
            Score how well the candidate's resume satisfies the following rubric item.

            Rubric item:
            Name: {rubric_item.name}
            Description: {rubric_item.description}
            Required: {rubric_item.required}
            Keywords: {", ".join(rubric_item.keywords) or "None"}
            Evidence sources to consider: {", ".join(rubric_item.evidence_sources) or "any"}
            Minimum years required: {rubric_item.minimum_years if rubric_item.minimum_years is not None else "Not specified"}

            Candidate resume (JSON):
            {resume}

            Score the candidate's fit for this rubric item on a scale of 0 to 10, where:
            0 = no relevant evidence at all
            5 = partial or indirect evidence
            10 = exceptional, thoroughly demonstrated evidence

            Base your score only on evidence found in the resume. Do not invent information.
            Briefly explain your reasoning and cite the specific resume evidence
            (bullet points, skills, coursework, etc.) that informed your score.
        """

        result = await llm.async_prompt(
            prompt=prompt,
            output_model=ScoredRubricItemLLMOutput,
            temperature=0.2,
            log_message=f"Scoring rubric item: {rubric_item.name}"
        )

        return ScoredRubricItem(
            name=rubric_item.name,
            description=rubric_item.description,
            importance=rubric_item.importance,
            required=rubric_item.required,
            weight=weight,
            score=result.score,
            weighted_score=weight * result.score,
            reasoning=result.reasoning,
            evidence=result.evidence,
            strengths=result.strengths,
            weaknesses=result.weaknesses,
        )

async def score_all_items(
        llm: LLMManager,
        rubric_items: list[RubricItem],
        resume: str,
        weights: dict[str, float],
) -> list[ScoredRubricItem]:
    tasks = [score_rubric_item(llm, item, resume, weights[item.name]) for item in rubric_items]
    return await asyncio.gather(*tasks)


async def score_resume(
        resume: str,
        job_posting: str,
        llm_model: str = "gemini"
) -> ScoredRubric:
    llm = LLMManager(llm_model)
    rubric = await generate_rubric(llm, job_posting)
    rubric_items = rubric.items

    if not rubric_items:
        raise ValueError("Job posting has no rubric items")

    weights = normalize_weights(rubric_items)

    scored_items = await score_all_items(
        llm,
        rubric_items,
        resume,
        weights,
    )

    overall_score = round(sum(item.weighted_score for item in scored_items) * 10, 2)

    missing_required = [
        item.name for item in scored_items
        if item.required and item.score < 5
    ]

    all_strengths = []
    all_weaknesses = []
    for item in scored_items:
        all_strengths.extend(item.strengths)
        all_weaknesses.extend(item.weaknesses)

    return ScoredRubric(
        overall_score=overall_score,
        items=scored_items,
        missing_required=missing_required,
        strengths=all_strengths,
        weaknesses=all_weaknesses
    )