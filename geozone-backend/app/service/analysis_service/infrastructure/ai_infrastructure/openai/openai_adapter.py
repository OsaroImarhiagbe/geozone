# services/llm_gateway/infrastructure/openai_adapter.py
from openai import AsyncOpenAI
from ..schema.completion import GenerateRequest, GenerateResponse, TokenUsage


class OpenAiAdapter:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        model = request.model or "gpt-4o"

        response = await self.client.chat.completions.create(
            model=model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            messages=[m.model_dump() for m in request.messages],
        )

        choice = response.choices
        usage = response.usage

        return GenerateResponse(
            text=choice.message.content or "",
            provider="openai",
            model=model,
            usage=TokenUsage(
                input_tokens=usage.prompt_tokens if usage else 0,
                output_tokens=usage.completion_tokens if usage else 0,
            ),
        )
