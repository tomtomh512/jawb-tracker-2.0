from typing import Optional

from llm.manager import LLMManager
from schemas.api.job_posting import CoverLetter


async def generate_cover_letter(
        resume: str,
        job_posting: str,
        llm_model: str = "gemini",
        custom_prompt: Optional[str] = None
) -> CoverLetter:
    llm = LLMManager(llm_model)

    prompt = f"""
            You are writing a personalized cover letter.

            Inputs:
            1. Resume (source of truth)
            2. Job posting (target role)
            3. User instructions (how the user wants the cover letter written)

            Rules:
            - The resume is the only source of factual information about the candidate.
            - Adapt the cover letter to the job posting.
            - Obey the user's instructions whenever they do not require inventing information.
            - Never fabricate qualifications or experience.
            - If information is missing, omit it rather than making assumptions.
            - Return only the completed cover letter.

            Additional user instructions (may be empty):
            {custom_prompt}

            If no additional instructions are provided, write a concise, professional cover letter that:
            - is 250–400 words,
            - emphasizes the strongest qualifications,
            - matches the tone of the job posting,
            - and ends with a polite call to action.

            Resume:
            {resume}

            Job Posting:
            {job_posting}
        """

    result = await llm.async_prompt(
        prompt=prompt,
        output_model=CoverLetter,
        temperature=0.5,
        log_message="Generating cover letter."
    )

    return result