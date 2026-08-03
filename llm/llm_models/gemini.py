import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()


class Gemini:
    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

    def _log_usage(self, response, log_message):
        usage = response.usage_metadata
        if usage:
            print(
                f"prompt_tokens={usage.prompt_token_count} "
                f"output_tokens={usage.candidates_token_count} "
                f"total_tokens={usage.total_token_count}"
            )
        if log_message:
            print(f"log_message={log_message}")

    async def prompt(
            self,
            prompt: str,
            output_model: type[BaseModel],
            temperature: float = 0.0,
            system_prompt: str | None = None,
            log_message: str | None = None
    ) -> BaseModel:
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=output_model,
                system_instruction=system_prompt,
            )
        )

        self._log_usage(response, log_message)

        return output_model.model_validate_json(response.text)

    async def prompt_pdf(
            self,
            pdf_path: str | Path,
            prompt: str,
            output_model: type[BaseModel],
            system_prompt: str | None = None,
            log_message: str | None = None,
    ) -> BaseModel:
        pdf_path = Path(pdf_path)

        uploaded = await self.client.aio.files.upload(file=pdf_path)

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[
                uploaded,
                prompt,
            ],
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=output_model,
                system_instruction=system_prompt,
            ),
        )

        self._log_usage(response, log_message)

        return output_model.model_validate_json(response.text)