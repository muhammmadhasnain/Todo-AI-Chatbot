# Data Model: Todo AI Chatbot Backend

## Entity: User
**Fields**:
- user_id: string (unique identifier from Better Auth)
- id: integer (primary key)
- email: string (unique, required)
- name: string (optional)
- avatar_url: string (optional)
- email_verified: boolean (default: false)
- created_at: datetime (auto-generated)
- updated_at: datetime (auto-generated)
- last_login_at: datetime (optional)

**Relationships**:
- One-to-many with Task (user has many tasks)
- One-to-many with Conversation (user has many conversations)
- One-to-many with Message (user has many messages)

**Validation rules**:
- user_id must be unique and come from Better Auth system
- email must be unique and valid email format
- created_at and updated_at automatically managed

## Entity: Task
**Fields**:
- id: integer (primary key)
- user_id: string (foreign key to User)
- title: string (required, max 255 chars)
- description: string (optional, max 1000 chars)
- completed: boolean (default: false)
- created_at: datetime (auto-generated)
- updated_at: datetime (auto-generated)

**Relationships**:
- Many-to-one with User (task belongs to user)

**Validation rules**:
- user_id must match authenticated user for operations
- title is required and cannot be empty
- created_at and updated_at automatically managed

## Entity: Conversation
**Fields**:
- id: integer (primary key)
- user_id: string (foreign key to User)
- created_at: datetime (auto-generated)
- updated_at: datetime (auto-generated)

**Relationships**:
- Many-to-one with User (conversation belongs to user)
- One-to-many with Message (conversation has many messages)

**Validation rules**:
- user_id must match authenticated user for operations
- created_at and updated_at automatically managed

## Entity: Message
**Fields**:
- id: integer (primary key)
- user_id: string (foreign key to User)
- conversation_id: integer (foreign key to Conversation)
- role: string (required, values: "user" or "assistant")
- content: string (required)
- created_at: datetime (auto-generated)

**Relationships**:
- Many-to-one with User (message belongs to user)
- Many-to-one with Conversation (message belongs to conversation)

**Validation rules**:
- user_id must match authenticated user for operations
- role must be either "user" or "assistant"
- content cannot be empty
- created_at automatically managed