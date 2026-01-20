# OpenAI ChatKit Frontend Integration - Quick Start Guide with MCP Architecture

## Prerequisites

- Node.js 18+ installed
- Next.js 16+ project set up
- Better Auth configured for authentication
- OpenAI API key available in environment
- MCP server configured for chat functionality

## Installation

1. Install the OpenAI ChatKit React package:
   ```bash
   npm install @openai/chatkit-react
   ```

2. Install MCP SDK and additional dependencies:
   ```bash
   npm install @modelcontextprotocol/sdk @types/react
   ```

## MCP Tools Setup

### 1. Create MCP Tools for Chat Functionality

```typescript
// lib/mcp-tools.ts
import { createHandler, json } from '@modelcontextprotocol/sdk';

// MCP tool for sending messages
export const send_message = createHandler(
  'send_message',
  {
    parameters: {
      type: 'object',
      properties: {
        sessionId: { type: 'string' },
        message: { type: 'string' },
        userId: { type: 'string' },
        metadata: { type: 'object' }
      },
      required: ['sessionId', 'message', 'userId']
    },
    result: {
      type: 'object',
      properties: {
        messageId: { type: 'string' },
        status: { type: 'string' },
        timestamp: { type: 'string' }
      }
    }
  },
  async ({ sessionId, message, userId, metadata }) => {
    // Implementation to send message via backend API
    const response = await fetch('/api/chatkit/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify({ session_id: sessionId, message, metadata })
    });

    const result = await response.json();
    return {
      messageId: result.message_id,
      status: 'sent',
      timestamp: new Date().toISOString()
    };
  }
);

// MCP tool for retrieving responses
export const get_response = createHandler(
  'get_response',
  {
    parameters: {
      type: 'object',
      properties: {
        sessionId: { type: 'string' },
        messageId: { type: 'string' },
        userId: { type: 'string' }
      },
      required: ['sessionId', 'messageId', 'userId']
    },
    result: {
      type: 'object',
      properties: {
        response: { type: 'string' },
        status: { type: 'string' },
        timestamp: { type: 'string' }
      }
    }
  },
  async ({ sessionId, messageId, userId }) => {
    // Implementation to get response from backend
    // This might involve polling or SSE depending on implementation
    const response = await fetch(`/api/chatkit/messages/${messageId}/response`, {
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });

    const result = await response.json();
    return {
      response: result.response,
      status: 'success',
      timestamp: new Date().toISOString()
    };
  }
);

// Additional MCP tools for session management, authentication, etc.
```

## Frontend Integration

### 1. Create the Chat Component with MCP Integration

```tsx
// components/chat/ChatKit.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useMCPTools } from 'hooks/useMCPTools'; // Custom hook for MCP integration
import { send_message, get_response } from 'lib/mcp-tools';

export function ChatKitComponent() {
  const { callMCPTool } = useMCPTools();

  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        // Use MCP tools for session management
        const sessionResult = await callMCPTool('create_session', {
          userId: getCurrentUserId(),
          title: 'New Chat Session'
        });

        return sessionResult.client_secret;
      },
    },
    theme: {
      colorScheme: 'light',
      radius: 'round',
      color: {
        accent: { primary: '#8B5CF6', level: 2 },
      },
    },
  });

  // Custom message handler that uses MCP tools
  const handleSendMessage = async (message: string) => {
    const sessionId = getCurrentSessionId();
    const userId = getCurrentUserId();

    // Send message via MCP tool
    await callMCPTool('send_message', {
      sessionId,
      message,
      userId,
      metadata: {}
    });
  };

  return <ChatKit control={control} className="h-[600px] w-[320px]" />;
}
```

### 2. MCP Tools Integration Hook

```tsx
// hooks/useMCPTools.ts
import { useState } from 'react';

export const useMCPTools = () => {
  const [isLoading, setIsLoading] = useState(false);

  const callMCPTool = async (toolName: string, params: any) => {
    setIsLoading(true);
    try {
      // This would connect to your MCP server
      const response = await fetch('/api/mcp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify({
          tool: toolName,
          parameters: params
        })
      });

      const result = await response.json();
      return result;
    } catch (error) {
      console.error(`Error calling MCP tool ${toolName}:`, error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return { callMCPTool, isLoading };
};
```

### 3. Integration in Page

```tsx
// pages/chat.tsx
import { ChatKitComponent } from 'components/chat/ChatKit';
import { withAuth } from 'lib/auth'; // Your auth wrapper

function ChatPage() {
  return (
    <div className="container mx-auto p-4">
      <h1>AI Chat Assistant</h1>
      <ChatKitComponent />
    </div>
  );
}

export default withAuth(ChatPage);
```

## Environment Variables

Add these to your `.env.local`:

```env
OPENAI_API_KEY=your_openai_api_key
NEXTAUTH_SECRET=your_nextauth_secret
MCP_SERVER_URL=your_mcp_server_url
```

## Running the Application

1. Start your development server:
   ```bash
   npm run dev
   ```

2. Visit `http://localhost:3000/chat` to access the chat interface

## Testing

1. Verify the component renders without errors
2. Test sending a message via MCP tools and receiving a response
3. Verify authentication is working properly through MCP tools
4. Test error handling scenarios via MCP tools