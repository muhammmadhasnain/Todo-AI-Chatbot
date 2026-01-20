
from agents import OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
import os
from ..config import settings



# 0.1. Loading the environment variables


# 1. Which LLM Provider to use? -> Google Chat Completions API Service

external_client = AsyncOpenAI(
    api_key= settings.GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-3-flash-preview",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True ,
)

# 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