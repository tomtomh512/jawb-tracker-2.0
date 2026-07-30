import asyncio

from llm.manager import LLMManager
from schemas.llm.resume import InitialResumeScanOutput, ParsedResume
from utils.section_mapping import SECTION_MAPPING

semaphore = asyncio.Semaphore(2)


async def parse_section(llm: LLMManager, section):
    async with semaphore:
        classification = section.classification.value
        config = SECTION_MAPPING.get(classification)

        if not config:
            return None

        prompt = f"""
            Extract the following resume section into structured JSON.

            Section name:
            {section.name}

            Section content:
            {section.content}

            Return only the fields defined by the schema.
            Do not invent information.
        """

        result = await llm.async_prompt(
            prompt=prompt,
            output_model=config["model"],
            log_message=f"Extracting resume section: {section.name}"
        )

        return config["field"], result


async def parse_all_sections(llm: LLMManager, sections):
    tasks = [parse_section(llm, section) for section in sections]
    return await asyncio.gather(*tasks, return_exceptions=True)


async def assemble_parsed_resume(
        llm: LLMManager,
        initial_result: InitialResumeScanOutput
) -> ParsedResume:
    extracted_sections = await parse_all_sections(llm, initial_result.resume_sections)

    combined = ParsedResume(basics=initial_result.basics)
    for result in extracted_sections:
        if result is None:
            continue

        field, section_data = result
        getattr(combined, field).extend(getattr(section_data, field))

    return combined


async def initialResumeScanText(
        llm: LLMManager,
        resume_text: str
) -> InitialResumeScanOutput:
    prompt = f"""
            Extract the basic information and section contents from this resume.

            Resume:
            {resume_text}
        """

    return await llm.async_prompt(
        prompt=prompt,
        output_model=InitialResumeScanOutput,
        log_message=f"Extracting basic information from resume text"
    )


async def initialResumeScanPdf(
        llm: LLMManager,
        pdf_path: str,
) -> InitialResumeScanOutput:
    prompt = "Extract the basic information and section contents from this resume"

    return await llm.async_prompt_pdf(
        pdf_path=pdf_path,
        prompt=prompt,
        output_model=InitialResumeScanOutput,
        log_message=f"Extracting basic information from resume PDF"
    )


async def parse_resume_from_text(
        resume_text: str,
        llm_model: str = "gemini"
) -> ParsedResume:
    llm = LLMManager(llm_model)

    initial_result = await initialResumeScanText(llm, resume_text)
    final_result = await assemble_parsed_resume(llm, initial_result)

    return final_result


async def parse_resume_from_pdf(
        pdf_path: str,
        llm_model: str = "gemini",
) -> ParsedResume:
    llm = LLMManager(llm_model)

    initial_result = await initialResumeScanPdf(llm, pdf_path)
    final_result = await assemble_parsed_resume(llm, initial_result)

    return final_result