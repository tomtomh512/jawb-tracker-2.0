import os
import json

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()

class Groq:
    def __init__(self):
        self.model = os.getenv("GROQ_MODEL")

        if not self.model:
            raise ValueError("GROQ_MODEL is not set")

        self.client = AsyncOpenAI(
            base_url=os.getenv("GROQ_BASE_URL"),
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def _log_usage(self, response, log_message):
        usage = response.usage
        if usage:
            print(
                f"prompt_tokens={usage.prompt_tokens} "
                f"completion_tokens={usage.completion_tokens} "
                f"total_tokens={usage.total_tokens}"
            )
        if log_message:
            print(f"log_message={log_message}")

    async def prompt(
            self,
            prompt: str,
            output_model: type[BaseModel],
            system_prompt: str | None = None,
            log_message: str | None = None,
    ) -> BaseModel:
        schema = output_model.model_json_schema()

        base_system_prompt = (
            "Return ONLY a JSON object. "
            "Do not include markdown. "
            "Do not include explanations. "
            "Do not include <think> tags."
        )

        if system_prompt:
            base_system_prompt += "\n\n" + system_prompt

        messages = [
            {
                "role": "system",
                "content": base_system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n"
                    "Return ONLY valid JSON.\n"
                    "The JSON must follow this schema:\n"
                    f"{json.dumps(schema, indent=2)}"
                ),
            }
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            # response_format={
            #     "type": "json_object"
            # },
        )

        self._log_usage(response, log_message)

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("LLM returned empty response")

        try:
            data = json.loads(content)
            return output_model.model_validate(data)

        except (json.JSONDecodeError, ValidationError) as e:
            raise ValueError(
                f"Invalid LLM output:\n{content}\n\nError: {e}"
            )