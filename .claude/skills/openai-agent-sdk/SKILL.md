---
name: openai-agent-sdk
description: Comprehensive OpenAI Agent SDK framework for building multi-agent workflows with support for agents, handoffs, guardrails, sessions, and tracing. Use when building agentic AI applications that require sophisticated agent interactions, tool integration, voice interfaces, or multi-agent orchestration.
---

# OpenAI Agent SDK

The OpenAI Agent SDK is a lightweight yet powerful framework for building multi-agent workflows in Python. It provides a provider-agnostic approach to orchestrating LLM-based agents, supporting the OpenAI APIs as well as 100+ other LLM providers through integrations.

## Core Components

### Agents
Agents are LLMs equipped with instructions and tools. They form the fundamental building blocks of your application.

```python
from agents import Agent

agent = Agent(
    name="Assistant",
    instructions="You're speaking to a human, so be polite and concise.",
    model="gpt-5.2",
)
```

### Tools
Tools extend agent capabilities by providing functions they can call to perform actions.

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    # Implementation here
    return f"The weather in {city} is sunny."
```

### Handoffs
Handoffs allow agents to delegate to other agents for specific tasks, enabling specialized routing.

```python
spanish_agent = Agent(
    name="Spanish",
    handoff_description="A spanish speaking agent.",
    instructions="You're speaking to a human, so be polite and concise. Speak in Spanish.",
    model="gpt-5.2",
)

agent = Agent(
    name="Assistant",
    instructions="You're speaking to a human, so be polite and concise. If the user speaks in Spanish, handoff to the spanish agent.",
    model="gpt-5.2",
    handoffs=[spanish_agent],
    tools=[get_weather],
)
```

### Guardrails
Guardrails enable validation of agent inputs and outputs to ensure safety and compliance.

### Sessions
Sessions automatically maintain conversation history across agent runs, eliminating manual history tracking.

## Voice Integration

The SDK includes voice capabilities for building interactive voice agents:

```python
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
)
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

async def main():
    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))
    buffer = np.zeros(24000 * 3, dtype=np.int16)
    audio_input = AudioInput(buffer=buffer)

    result = await pipeline.run(audio_input)

    # Process audio stream
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            # Handle audio data
            pass
```

## When to Use This Skill

Use this skill when you need to:

1. Create multi-agent systems with specialized routing
2. Build voice-enabled AI applications
3. Implement tool-extended agents with custom functionality
4. Create applications requiring agent handoffs for specific tasks
5. Build applications with built-in tracing and debugging capabilities
6. Develop long-running workflows with durable conversation history

## Best Practices

- Keep agent instructions clear and concise
- Use handoffs for specialized tasks rather than complex conditional logic
- Implement guardrails for safety-critical applications
- Leverage sessions for maintaining context across interactions
- Use built-in tracing for debugging and optimization
- Consider using GPT-5 for enhanced reasoning capabilities with configurable effort levels