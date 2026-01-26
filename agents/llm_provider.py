"""
LLM provider wrapper for governed agent cognition.

This module isolates the external model call from governance logic and
enforces structured JSON output with schema validation and repair loops.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, ValidationError

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    load_dotenv = None

try:
    import anthropic
except Exception:  # pragma: no cover - optional dependency
    anthropic = None


class LLMProviderError(RuntimeError):
    pass


class MissingAPIKeyError(LLMProviderError):
    pass


class MissingDependencyError(LLMProviderError):
    pass


class BudgetExceededError(LLMProviderError):
    pass


@dataclass
class LLMResult:
    data: Dict[str, Any]
    model: str
    input_tokens: int
    output_tokens: int
    prompt_hash: str
    raw_text: str


class LLMProvider:
    """Thin wrapper around the Anthropic SDK with governance controls."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4000,
        max_total_tokens: int = 50000,
        run_cost_cap: float = 2.0,
        input_cost_per_million: float = 3.0,
        output_cost_per_million: float = 15.0,
        max_retries: int = 2,
        concurrency: int = 4,
    ) -> None:
        if anthropic is None:
            raise MissingDependencyError(
                "anthropic is not installed. Install agents/requirements.txt to enable LLM calls."
            )
        if not api_key:
            raise MissingAPIKeyError("ANTHROPIC_API_KEY is required for LLM calls.")

        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.max_total_tokens = max_total_tokens
        self.run_cost_cap = run_cost_cap
        self.input_cost_per_million = input_cost_per_million
        self.output_cost_per_million = output_cost_per_million
        self.max_retries = max_retries
        self._semaphore = asyncio.Semaphore(concurrency)
        self._tokens_used = 0
        self._estimated_cost = 0.0

    @classmethod
    def from_env(cls) -> "LLMProvider":
        if load_dotenv is not None:
            load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise MissingAPIKeyError("ANTHROPIC_API_KEY is not set.")
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        max_tokens = int(os.getenv("MAX_TOKENS_PER_CALL", os.getenv("ANTHROPIC_MAX_TOKENS", "1200")))
        max_total_tokens = int(os.getenv("RUN_TOKEN_CAP", os.getenv("ANTHROPIC_MAX_TOTAL_TOKENS", "15000")))
        max_retries = int(os.getenv("MAX_REPAIR_RETRIES", os.getenv("ANTHROPIC_MAX_RETRIES", "2")))
        concurrency = int(os.getenv("MAX_CONCURRENCY", os.getenv("ANTHROPIC_CONCURRENCY", "3")))
        run_cost_cap = float(os.getenv("RUN_COST_CAP", "2.0"))
        input_cost = float(os.getenv("INPUT_COST_PER_MILLION", "3.0"))
        output_cost = float(os.getenv("OUTPUT_COST_PER_MILLION", "15.0"))
        return cls(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
            max_total_tokens=max_total_tokens,
            run_cost_cap=run_cost_cap,
            input_cost_per_million=input_cost,
            output_cost_per_million=output_cost,
            max_retries=max_retries,
            concurrency=concurrency,
        )

    @property
    def tokens_used(self) -> int:
        return self._tokens_used

    @property
    def estimated_cost(self) -> float:
        return self._estimated_cost

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_model: Type[BaseModel],
    ) -> LLMResult:
        schema_payload = json.dumps(schema_model.model_json_schema(), indent=2)
        system_with_schema = (
            f"{system_prompt}\n\n"
            "Return ONLY valid JSON. Do not wrap in markdown.\n"
            "Schema:\n"
            f"{schema_payload}"
        )

        attempt = 0
        last_error = ""
        response_text = ""

        while attempt <= self.max_retries:
            attempt += 1
            response_text = await self._call(system_with_schema, user_prompt)
            try:
                payload = self._extract_json(response_text)
                validated = schema_model.model_validate(payload)
                return LLMResult(
                    data=validated.model_dump(),
                    model=self.model,
                    input_tokens=self._last_input_tokens,
                    output_tokens=self._last_output_tokens,
                    prompt_hash=self._hash_prompt(system_with_schema, user_prompt),
                    raw_text=response_text,
                )
            except (json.JSONDecodeError, ValidationError) as exc:
                last_error = str(exc)
                user_prompt = (
                    "Your previous output was invalid or did not match the schema.\n"
                    f"Validation error:\n{last_error}\n\n"
                    "Return corrected JSON only."
                )

        raise LLMProviderError(f"LLM output could not be validated: {last_error}")

    async def _call(self, system_prompt: str, user_prompt: str) -> str:
        if self._tokens_used >= self.max_total_tokens:
            raise BudgetExceededError("Token budget exceeded before request.")
        if self._estimated_cost >= self.run_cost_cap:
            raise BudgetExceededError("Cost budget exceeded before request.")

        async with self._semaphore:
            try:
                message = await asyncio.to_thread(
                    self._client.messages.create,
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )
            except Exception as exc:
                raise LLMProviderError(f"LLM call failed: {exc}") from exc

        text = self._extract_text(message)
        input_tokens = getattr(message.usage, "input_tokens", 0) if message else 0
        output_tokens = getattr(message.usage, "output_tokens", 0) if message else 0
        self._last_input_tokens = input_tokens
        self._last_output_tokens = output_tokens
        self._tokens_used += input_tokens + output_tokens
        self._estimated_cost = self._calculate_cost(input_tokens, output_tokens)

        if self._tokens_used > self.max_total_tokens:
            raise BudgetExceededError("Token budget exceeded after request.")
        if self._estimated_cost > self.run_cost_cap:
            raise BudgetExceededError("Cost budget exceeded after request.")

        return text

    @staticmethod
    def _extract_text(message: Any) -> str:
        if not message or not getattr(message, "content", None):
            return ""
        content = message.content
        if isinstance(content, list) and content:
            first = content[0]
            return getattr(first, "text", "") if hasattr(first, "text") else str(first)
        return str(content)

    @staticmethod
    def _extract_json(text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start == -1 or end == -1:
                raise
            return json.loads(text[start : end + 1])

    @staticmethod
    def _hash_prompt(system_prompt: str, user_prompt: str) -> str:
        payload = f"{system_prompt}\n{user_prompt}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        input_cost = (input_tokens / 1_000_000) * self.input_cost_per_million
        output_cost = (output_tokens / 1_000_000) * self.output_cost_per_million
        return self._estimated_cost + input_cost + output_cost
