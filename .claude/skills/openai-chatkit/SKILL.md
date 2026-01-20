---
name: openai-chatkit
description: Comprehensive OpenAI ChatKit framework for building high-quality, AI-powered chat experiences with deep UI customization, response streaming, tool integration, and production-ready components. Use when building chat applications that require advanced conversational interfaces with customizable UI, backend integration, and tool capabilities.
---

# OpenAI ChatKit Skill

This skill provides comprehensive guidance for using OpenAI's ChatKit framework to build AI-powered chat experiences with minimal setup and maximum customization.

## Overview

ChatKit is a batteries-included framework for building high-quality, AI-powered chat experiences with:
- Deep UI customization options
- Response streaming capabilities
- Tool integration support
- Production-ready components
- Client and server-side implementations

## Installation

### For React Applications
```bash
npm install @openai/chatkit-react
```

### For HTML/JavaScript
Add the ChatKit JavaScript library to your HTML:
```html
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

## Backend Implementation with FastAPI

### Setting up a ChatKit Session Endpoint
```python
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.post("/api/chatkit/session")
def create_chatkit_session():
    session = openai.chatkit.sessions.create({
      # ... session configuration
    })
    return {"client_secret": session.client_secret}
```

### Creating a ChatKit Endpoint with Tool Integration
```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import StreamingResponse, Response
from chatkit.server import StreamingResult

app = FastAPI(title="ChatKit API")

@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    server = Depends(get_chatkit_server)
) -> Response:
    payload = await request.body()
    result = await server.process(payload, {"request": request})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    if hasattr(result, "json"):
        return Response(content=result.json, media_type="application/json")
    return JSONResponse(result)
```

## Frontend Implementation

### React Component with useChatKit Hook
```tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function MyChat() {
  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        if (existing) {
          // implement session refresh
        }

        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[320px]" />;
}
```

## UI Customization

### Theme Configuration
```javascript
const { control } = useChatKit({
  theme: {
    colorScheme: 'dark',
    radius: 'round',
    color: {
      accent: { primary: '#8B5CF6', level: 2 },
    },
  },
  // ... other options
});
```

### Complete UI Configuration Options
```javascript
const { control } = useChatKit({
  theme: {
    colorScheme: 'dark',
    radius: 'round',
    color: {
      accent: { primary: '#8B5CF6', level: 2 },
    },
  },
  header: {
    enabled: true,
    rightAction: {
      icon: 'light-mode',
      onClick: () => console.log('Toggle theme'),
    },
  },
  history: {
    enabled: true,
    showDelete: true,
    showRename: true,
  },
  startScreen: {
    greeting: 'How can we help?',
    prompts: [
      {
        label: 'Troubleshoot an issue',
        prompt: 'Help me fix an issue',
        icon: 'lifesaver',
      },
      {
        label: 'Request a feature',
        prompt: 'I have an idea',
        icon: 'lightbulb',
      },
    ],
  },
  composer: {
    placeholder: 'Ask the assistant…',
  },
  threadItemActions: {
    feedback: true,
    retry: true,
  },
});
```

## Tool Integration

### Creating Agent-Callable Tools
```python
from agents import function_tool, RunContextWrapper
from chatkit.agents import AgentContext, ClientToolCall

@function_tool(
    description_override="Record a fact shared by the user"
)
async def save_fact(
    ctx: RunContextWrapper[AgentContext],
    fact: str,
) -> dict[str, str] | None:
    try:
        saved = await fact_store.create(text=fact)
        confirmed = await fact_store.mark_saved(saved.id)
        if confirmed is None:
            raise ValueError("Failed to save fact")

        # Trigger client-side tool execution
        ctx.context.client_tool_call = ClientToolCall(
            name="record_fact",
            arguments={"fact_id": confirmed.id, "fact_text": confirmed.text},
        )

        return {"fact_id": confirmed.id, "status": "saved"}
    except Exception:
        return None
```

### Initializing Agent with Tools
```python
from agents import Agent
from chatkit.agents import AgentContext

INSTRUCTIONS = """
You are ChatKit Guide, an onboarding assistant that helps users
understand ChatKit and records facts about themselves. When a user
shares a fact, call save_fact immediately with a concise summary.
When they request theme changes, call switch_theme before responding.
"""

agent = Agent[AgentContext](
    model="gpt-4.1-mini",
    name="ChatKit Guide",
    instructions=INSTRUCTIONS,
    tools=[save_fact, switch_theme, get_weather],
)
```

### Handling Client-Side Tool Calls
```typescript
const chatkit = useChatKit({
  // ... other options
  onClientTool: async (invocation) => {
    if (invocation.name === "switch_theme") {
      const requested = invocation.params.theme;
      if (requested === "light" || requested === "dark") {
        onThemeRequest(requested);
        return { success: true };
      }
      return { success: false };
    }

    if (invocation.name === "record_fact") {
      const id = String(invocation.params.fact_id ?? "");
      const text = String(invocation.params.fact_text ?? "");
      await saveFact(id, text);
      return { success: true };
    }

    return { success: false };
  },
  onError: ({ error }) => {
    console.error("ChatKit error", error);
  },
});
```

## Composer Configuration

### Customizing the Message Composer
```typescript
composer: {
  attachments: {
    enabled: true,
    maxSize: 50 * 1024 * 1024, // 50MB
    maxCount: 5,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif"],
      "text/plain": [".txt"],
    }
  },
  models: [
    // Define available models for user selection
  ],
  placeholder: "Ask the assistant…",
  tools: [
    // List of available tools
  ]
}
```

## Best Practices

1. **Security**: Always store API keys in environment variables and never expose them in client-side code
2. **Session Management**: Implement proper session refresh logic to maintain long-running conversations
3. **Error Handling**: Use the onError callback to gracefully handle ChatKit errors
4. **Performance**: Use response streaming to provide immediate feedback to users
5. **Customization**: Leverage the extensive theme and UI options to match your application's design

## Common Use Cases

- Customer support chat interfaces
- AI-powered assistant applications
- Interactive learning platforms
- Collaborative tools with AI assistance
- E-commerce chat experiences