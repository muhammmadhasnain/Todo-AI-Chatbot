# API Contract: Agentic Chat System

## Chat API Endpoint

### POST /api/{user_id}/chat

**Purpose**: Send message & get AI response

**Request Parameters**:
- user_id (path parameter, string): Unique identifier of the authenticated user

**Request Body**:
```json
{
  "conversation_id": "integer (optional)",
  "message": "string (required)"
}
```

**Response Body**:
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array"
}
```

**Error Responses**:
- 400: Invalid request format
- 401: Unauthorized access
- 403: User access violation
- 500: Internal server error

## MCP Tool Contracts

### add_task
**Purpose**: Create new task
**Parameters**:
- user_id (string, required): User identifier
- title (string, required): Task title
- description (string, optional): Task description

**Returns**:
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### list_tasks
**Purpose**: Retrieve tasks
**Parameters**:
- user_id (string, required): User identifier
- status (string, optional): Filter by status ("all", "pending", "completed")

**Returns**:
```json
{
  "tasks": "array of task objects"
}
```

### complete_task
**Purpose**: Mark task as complete
**Parameters**:
- user_id (string, required): User identifier
- task_id (integer, required): Task identifier

**Returns**:
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### delete_task
**Purpose**: Remove task
**Parameters**:
- user_id (string, required): User identifier
- task_id (integer, required): Task identifier

**Returns**:
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### update_task
**Purpose**: Modify task
**Parameters**:
- user_id (string, required): User identifier
- task_id (integer, required): Task identifier
- title (string, optional): New task title
- description (string, optional): New task description

**Returns**:
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```