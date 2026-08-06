import asyncio
from pathlib import Path

from pydantic import BaseModel

from llm.llm_models.gemini import Gemini
from llm.llm_models.groq import Groq


class LLMManager:
    def __init__(self, model: str = "gemini"):
        models = {
            "gemini": Gemini,
            "groq": Groq,
        }

        try:
            self.model = models[model]()
        except KeyError:
            raise ValueError(f"Unknown model: {model}")

    async def async_prompt(
            self,
            prompt: str,
            output_model: type[BaseModel],
            temperature: float = 0.0,
            system_prompt: str | None = None,
            log_message: str | None = None,
    ) -> BaseModel:
        return await self.model.prompt(
            prompt,
            output_model,
            temperature,
            system_prompt,
            log_message
        )

    def prompt(
            self,
            prompt: str,
            output_model: type[BaseModel],
            temperature: float = 0.0,
            system_prompt: str | None = None,
            log_message: str | None = None,
    ) -> BaseModel:
        return asyncio.run(
            self.async_prompt(
                prompt,
                output_model,
                temperature,
                system_prompt,
                log_message
            )
        )

    async def async_prompt_upload(
            self,
            upload_path: str | Path,
            prompt: str,
            output_model: type[BaseModel],
            system_prompt: str | None = None,
            log_message: str | None = None,
    ) -> BaseModel:
        if not hasattr(self.model, "prompt_upload"):
            raise NotImplementedError(
                f"{type(self.model).__name__} does not support upload input."
            )

        return await self.model.prompt_upload(
            upload_path,
            prompt,
            output_model,
            system_prompt,
            log_message
        )

    def prompt_upload(
            self,
            upload_path: str | Path,
            prompt: str,
            output_model: type[BaseModel],
            system_prompt: str | None = None,
            log_message: str | None = None,
    ) -> BaseModel:
        return asyncio.run(
            self.async_prompt_upload(
                upload_path,
                prompt,
                output_model,
                system_prompt,
                log_message
            )
        )