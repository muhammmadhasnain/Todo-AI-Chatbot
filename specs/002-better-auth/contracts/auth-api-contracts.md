# Authentication API Contracts (CORRECTED)

## Protected API Endpoints

### POST /api/{user_id}/chat
Chat with AI assistant (requires authenticated session).

**Headers**:
```
Authorization: Bearer <better_auth_session_token>
```

**Path Parameters**:
- `user_id`: The user ID in the path (must match authenticated user)

**Request**:
```json
{
  "conversation_id": 123,
  "message": "Hello, help me create a todo"
}
```

**Response (200)**:
```json
{
  "conversation_id": 123,
  "response": "Sure, I can help you create a todo",
  "tool_calls": []
}
```

**Errors**:
- 401: Invalid or expired session
- 403: User ID in path doesn't match authenticated user
- 500: Server error

### GET /api/{user_id}/tasks
Get user's tasks (requires authenticated session).

**Headers**:
```
Authorization: Bearer <better_auth_session_token>
```

**Path Parameters**:
- `user_id`: The user ID in the path (must match authenticated user)

**Response (200)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "completed": false,
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

**Errors**:
- 401: Invalid or expired session
- 403: User ID in path doesn't match authenticated user
- 500: Server error

### POST /api/{user_id}/tasks
Create a new task (requires authenticated session).

**Headers**:
```
Authorization: Bearer <better_auth_session_token>
```

**Path Parameters**:
- `user_id`: The user ID in the path (must match authenticated user)

**Request**:
```json
{
  "title": "New task",
  "description": "Task description"
}
```

**Response (201)**:
```json
{
  "id": 123,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "created_at": "2024-01-01T12:00:00Z"
}
```

**Errors**:
- 401: Invalid or expired session
- 403: User ID in path doesn't match authenticated user
- 500: Server error

## Session Verification Flow

### Frontend to Backend Token Forwarding
1. Frontend authenticates user via Better Auth client
2. Frontend extracts session token from Better Auth
3. Frontend includes session token in Authorization header for backend API calls
4. Backend calls Better Auth API to verify session and get user info
5. Backend processes request with verified user context

## Backend Session Verification API

### Internal: Verify Better Auth Session
Backend makes internal call to Better Auth API to verify session.

**Request** (Internal to Better Auth):
```json
{
  "session_token": "better_auth_session_token"
}
```

**Response** (from Better Auth):
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "is_valid": true,
  "expires_at": "2024-01-01T12:00:00Z"
}
```

This verification happens automatically via backend middleware for all protected endpoints.