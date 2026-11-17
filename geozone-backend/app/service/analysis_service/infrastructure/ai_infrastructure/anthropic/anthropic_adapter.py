# services/llm_gateway/infrastructure/anthropic_adapter.py
from anthropic import AsyncAnthropic
from app.service.analysis_service.schemas.analysis_schema import (GenerateRequest,GenerateResponse,TokenUsage)


class AnthropicAdapter:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=api_key)

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        model = request.model or "claude-sonnet-4-6"

        system_prompt = next(
            (m.content for m in request.messages if m.role == "system"),
            None,
        )
        chat_messages = [
            {"role": m.role, "content": m.content}
            for m in request.messages
            if m.role != "system"
        ]

        response = await self.client.messages.create(
            model=model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=system_prompt,
            messages=chat_messages,
        )

        text = "".join(
            block.text for block in response.content if block.type == "text"
        )

        return GenerateResponse(
            text=text,
            provider="anthropic",
            model=model,
            usage=TokenUsage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            ),
        )
