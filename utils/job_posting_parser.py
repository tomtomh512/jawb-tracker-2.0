from llm.manager import LLMManager
from schemas.llm.job_posting import ParsedJobPosting


async def parse_job_posting_from_text(
        job_posting: str,
        llm_model: str = "gemini"
) -> ParsedJobPosting:
    llm = LLMManager(llm_model)

    prompt = f"""
            Extract the factual contents of the job posting.

            Job Posting:
            {job_posting}
        """

    result = await llm.async_prompt(
        prompt=prompt,
        output_model=ParsedJobPosting,
        log_message="Parsing job posting"
    )

    return result