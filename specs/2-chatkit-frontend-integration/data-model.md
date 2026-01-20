# Data Model for OpenAI ChatKit Frontend Integration with MCP Architecture

## 1. Core Entities

### 1.1 ChatSession
Represents a conversation between user and AI assistant, containing metadata about the interaction; has unique ID per user (allowing users to have multiple sessions)

**Fields**:
- `id` (string): Unique identifier for the session per user
- `userId` (string): Reference to the authenticated user
- `createdAt` (Date): Timestamp when session was created
- `lastActive` (Date): Timestamp of last interaction
- `title` (string): Optional title for the session
- `metadata` (Record<string, any>): Additional session-specific data

**Validation Rules**:
- ID must be unique per user
- userId must reference a valid authenticated user
- createdAt must be in the past
- lastActive must be >= createdAt

**State Transitions**:
- `active` → `inactive` (after period of inactivity)
- `inactive` → `archived` (after extended inactivity)

### 1.2 ChatMessage
Represents a single message in the conversation, including content, sender, timestamp, and status; has unique ID per session

**Fields**:
- `id` (string): Unique identifier for the message per session
- `sessionId` (string): Reference to the parent session
- `content` (string): The actual message content
- `role` (enum: 'user' | 'assistant' | 'system'): The sender role
- `timestamp` (Date): When the message was sent/received
- `status` (enum: 'sent' | 'sending' | 'delivered' | 'error'): Message transmission status
- `metadata` (Record<string, any>): Additional message-specific data

**Validation Rules**:
- ID must be unique per session
- sessionId must reference a valid session
- content must not be empty
- role must be one of the allowed values
- status must be one of the allowed values

**State Transitions**:
- `sending` → `sent` (on successful transmission)
- `sending` → `error` (on transmission failure)
- `sent` → `delivered` (when confirmed by recipient system)

## 2. Supporting Entities

### 2.1 ChatTheme
Represents theme configuration for the chat interface

**Fields**:
- `primaryColor` (string): Primary color for the theme
- `secondaryColor` (string): Secondary color for the theme
- `backgroundColor` (string): Background color
- `textColor` (string): Text color
- `inputBackgroundColor` (string): Input field background
- `inputTextColor` (string): Input field text color
- `borderRadius` (string): Border radius value
- `spacing` (string): Spacing configuration
- `fontFamily` (string): Font family

### 2.2 ChatError
Represents error information for error handling

**Fields**:
- `code` (string): Error code
- `message` (string): Human-readable error message
- `details` (any): Additional error details
- `timestamp` (Date): When the error occurred

## 3. MCP Tools Specification

### 3.1 send_message Tool
**Purpose**: Send a message to the AI assistant
**Parameters**:
- `sessionId` (string): ID of the chat session
- `message` (string): Content of the message to send
- `userId` (string): ID of the authenticated user
- `metadata` (Record<string, any>): Additional metadata

**Returns**:
- `messageId` (string): ID of the sent message
- `status` (string): Status of the message ('sent', 'error')
- `timestamp` (Date): When the message was processed

### 3.2 get_response Tool
**Purpose**: Retrieve AI assistant response for a message
**Parameters**:
- `sessionId` (string): ID of the chat session
- `messageId` (string): ID of the message to get response for
- `userId` (string): ID of the authenticated user

**Returns**:
- `response` (string): AI assistant response content
- `status` (string): Status of the response ('success', 'error')
- `timestamp` (Date): When the response was generated

### 3.3 create_session Tool
**Purpose**: Create a new chat session
**Parameters**:
- `userId` (string): ID of the authenticated user
- `title` (string, optional): Title for the session
- `metadata` (Record<string, any>): Additional metadata

**Returns**:
- `sessionId` (string): ID of the created session
- `status` (string): Status of the session creation ('success', 'error')
- `timestamp` (Date): When the session was created

### 3.4 get_session Tool
**Purpose**: Retrieve information about a chat session
**Parameters**:
- `sessionId` (string): ID of the chat session
- `userId` (string): ID of the authenticated user

**Returns**:
- `sessionInfo` (object): Session details (id, title, createdAt, lastActive, etc.)
- `status` (string): Status of the session retrieval ('success', 'error')
- `timestamp` (Date): When the session info was retrieved

### 3.5 get_history Tool
**Purpose**: Retrieve message history for a chat session
**Parameters**:
- `sessionId` (string): ID of the chat session
- `userId` (string): ID of the authenticated user
- `limit` (number, optional): Maximum number of messages to return
- `offset` (number, optional): Number of messages to skip

**Returns**:
- `messages` (array): Array of message objects
- `total` (number): Total number of messages in the session
- `status` (string): Status of the history retrieval ('success', 'error')

### 3.6 add_message Tool
**Purpose**: Add a message to a chat session (internal use)
**Parameters**:
- `sessionId` (string): ID of the chat session
- `content` (string): Content of the message
- `role` (string): Role of the message sender ('user', 'assistant', 'system')
- `userId` (string): ID of the authenticated user
- `metadata` (Record<string, any>): Additional metadata

**Returns**:
- `messageId` (string): ID of the added message
- `status` (string): Status of the message addition ('success', 'error')
- `timestamp` (Date): When the message was added

### 3.7 verify_auth Tool
**Purpose**: Verify user authentication for MCP tool access
**Parameters**:
- `userId` (string): ID of the authenticated user
- `authToken` (string): Authentication token
- `toolName` (string): Name of the MCP tool being accessed

**Returns**:
- `valid` (boolean): Whether the authentication is valid
- `permissions` (array): List of permissions for the user
- `expiresAt` (Date): When the authentication expires

### 3.8 refresh_token Tool
**Purpose**: Refresh authentication token
**Parameters**:
- `refreshToken` (string): Refresh token to use
- `userId` (string): ID of the authenticated user

**Returns**:
- `newToken` (string): New authentication token
- `expiresAt` (Date): When the new token expires
- `status` (string): Status of the token refresh ('success', 'error')