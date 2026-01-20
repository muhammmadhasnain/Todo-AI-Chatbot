# OpenAI Agent SDK - Detailed Reference

## Architecture Overview

The OpenAI Agents SDK is designed with a minimal set of powerful primitives:

1. **Agents** - LLMs with instructions and tools
2. **Handoffs** - Delegation between agents
3. **Guardrails** - Input/output validation
4. **Sessions** - Conversation history management
5. **Tracing** - Visualization and debugging

## Advanced Usage Patterns

### Multi-Agent Workflows

```python
from agents import Agent, function_tool
import asyncio

@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant information."""
    # Implementation here
    return f"Results for: {query}"

@function_tool
def execute_code(code: str) -> str:
    """Execute code in a safe environment."""
    # Implementation here
    return f"Executed: {code}"

# Research agent
research_agent = Agent(
    name="Researcher",
    instructions="You are a research assistant. Use the knowledge base to find relevant information.",
    model="gpt-5.2",
    tools=[search_knowledge_base]
)

# Code agent
code_agent = Agent(
    name="Coder",
    instructions="You are a coding assistant. Generate and execute code as needed.",
    model="gpt-5.2",
    tools=[execute_code]
)

# Main agent
main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. For research tasks, hand off to the researcher. For coding tasks, hand off to the coder.",
    model="gpt-5.2",
    handoffs=[research_agent, code_agent]
)
```

### Session Management

Sessions automatically maintain conversation history:

```python
from agents import Session

# Create a session
session = Session()

# Run agent in session context
result = await main_agent.run(
    messages=[{"role": "user", "content": "Hello!"}],
    session=session
)

# Subsequent calls maintain context
result2 = await main_agent.run(
    messages=[{"role": "user", "content": "What did I just say?"}],
    session=session
)
```

### Guardrails Implementation

```python
from agents import Guardrail

def content_moderation_guardrail(content: str) -> bool:
    """Check if content is appropriate."""
    # Implementation here
    return True  # Return True if content passes, False otherwise

guardrail = Guardrail(
    name="Content Moderator",
    validator=content_moderation_guardrail
)

agent_with_guardrails = Agent(
    name="Guarded Assistant",
    instructions="Be helpful but safe.",
    model="gpt-5.2",
    guardrails=[guardrail]
)
```

## Voice Pipeline Configuration

For voice-enabled applications:

```python
import numpy as np
import sounddevice as sd
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline

async def voice_application():
    # Create audio buffer
    buffer = np.zeros(24000 * 3, dtype=np.int16)
    audio_input = AudioInput(buffer=buffer)

    # Create voice pipeline
    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))

    # Run the pipeline
    result = await pipeline.run(audio_input)

    # Stream audio response
    player = sd.OutputStream(samplerate=24000, channels=1, dtype=np.int16)
    player.start()

    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            player.write(event.data)
```

## Tracing and Debugging

The SDK includes built-in tracing capabilities:

```python
from agents import trace

# Enable tracing
trace.enable()

# Run your agent
result = await agent.run(messages=[{"role": "user", "content": "Hello"}])

# Access trace information
trace_data = trace.get_current_trace()
print(f"Trace ID: {trace_data.id}")
print(f"Steps: {len(trace_data.steps)}")
```

## Provider Integration

The SDK supports multiple LLM providers:

```python
# Using with OpenAI
agent_openai = Agent(
    name="OpenAI Agent",
    instructions="Use OpenAI models.",
    model="gpt-5.2",
    provider="openai"
)

# Using with other providers via LiteLLM
agent_anthropic = Agent(
    name="Anthropic Agent",
    instructions="Use Anthropic models.",
    model="claude-3.5-sonnet",
    provider="anthropic"
)
```