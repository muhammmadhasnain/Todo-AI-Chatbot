# OpenAI ChatKit API Contracts with MCP Architecture

## 1. MCP Tools for Session Management

### 1.1 Create Chat Session via MCP Tool
**Tool Name**: `create_session`
**Description**: Creates a new chat session with a client secret for authentication with the OpenAI service.

**Parameters**:
- `userId` (string): ID of the authenticated user
- `title` (string, optional): Title for the session
- `metadata` (Record<string, any>): Additional metadata

**Returns**:
- Success:
  ```json
  {
    "sessionId": "string",
    "status": "success",
    "timestamp": "ISO8601 date string"
  }
  ```
- Error:
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
  ```

**Security**: Requires valid authentication token via verify_auth MCP tool

### 1.2 Get Session History via MCP Tool
**Tool Name**: `get_history`
**Description**: Retrieves the message history for a specific chat session.

**Parameters**:
- `sessionId` (string): ID of the chat session
- `userId` (string): ID of the authenticated user
- `limit` (number, optional): Maximum number of messages to return
- `offset` (number, optional): Number of messages to skip

**Returns**:
- Success:
  ```json
  {
    "messages": [
      {
        "id": "string",
        "content": "string",
        "role": "user|assistant|system",
        "timestamp": "ISO8601 date string",
        "status": "sent|sending|delivered|error"
      }
    ],
    "total": "number",
    "status": "success"
  }
  ```
- Error:
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
  ```

## 2. MCP Tools for Message Operations

### 2.1 Send Message via MCP Tool
**Tool Name**: `send_message`
**Description**: Sends a message to the AI assistant via MCP tools.

**Parameters**:
- `sessionId` (string): ID of the chat session
- `message` (string): Content of the message to send
- `userId` (string): ID of the authenticated user
- `metadata` (Record<string, any>): Additional metadata

**Returns**:
- Success:
  ```json
  {
    "messageId": "string",
    "status": "sent",
    "timestamp": "ISO8601 date string"
  }
  ```
- Error:
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
  ```

### 2.2 Get Response via MCP Tool
**Tool Name**: `get_response`
**Description**: Retrieves AI assistant response for a message via MCP tools.

**Parameters**:
- `sessionId` (string): ID of the chat session
- `messageId` (string): ID of the message to get response for
- `userId` (string): ID of the authenticated user

**Returns**:
- Success:
  ```json
  {
    "response": "string",
    "status": "success",
    "timestamp": "ISO8601 date string"
  }
  ```
- Error:
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
  ```

## 3. MCP Tools for Authentication

### 3.1 Verify Authentication via MCP Tool
**Tool Name**: `verify_auth`
**Description**: Verifies the authentication token and returns user information via MCP tools.

**Parameters**:
- `userId` (string): ID of the authenticated user
- `authToken` (string): Authentication token
- `toolName` (string): Name of the MCP tool being accessed

**Returns**:
- Success:
  ```json
  {
    "valid": true,
    "permissions": ["array", "of", "permissions"],
    "expiresAt": "ISO8601 date string"
  }
  ```
- Error:
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
  ```

### 3.2 Refresh Token via MCP Tool
**Tool Name**: `refresh_token`
**Description**: Refreshes authentication token via MCP tools.

**Parameters**:
- `refreshToken` (string): Refresh token to use
- `userId` (string): ID of the authenticated user

**Returns**:
- Success:
  ```json
  {
    "newToken": "string",
    "expiresAt": "ISO8601 date string",
    "status": "success"
  }
  ```
- Error:
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": {}
    }
  }
  ```

## 4. Server-Sent Events for Streaming

### 4.1 Stream Message Response
**Endpoint**: `POST /api/chatkit/stream`
**Description**: Streams AI response in real-time (accessed via MCP tools).

**Request**:
- Headers:
  - `Authorization: Bearer <auth_token>` (required)
  - `Content-Type: application/json`
- Body:
  ```json
  {
    "session_id": "string",
    "message": "string",
    "metadata": {}
  }
  ```

**Response**:
- Success (200): Server-Sent Events stream
  - Event: `message` - partial message content
  - Event: `done` - indicates completion
- Unauthorized (401): Invalid authentication

## 5. Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## 6. Security Requirements

- All MCP tool calls require authentication verification
- MCP tools must follow the specified contracts with proper parameters and return values
- All data must be encrypted in transit
- Rate limiting applies to prevent abuse
- MCP tools must implement proper error handling with user-friendly responses