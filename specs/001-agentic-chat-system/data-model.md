# Data Model Specification: Agentic Chat System

## Entity: User
**Fields**:
- id (string): Unique identifier for the user
- email (string): User's email address
- name (string, optional): User's display name
- created_at (datetime): Timestamp of user creation
- updated_at (datetime): Timestamp of last update

**Relationships**:
- One-to-many with Conversation
- One-to-many with Task
- One-to-many with Message

**Validation**:
- Email must be valid format
- ID must be unique
- Required fields: id, email

## Entity: Conversation
**Fields**:
- id (integer): Unique identifier for the conversation
- user_id (string): Foreign key to User
- created_at (datetime): Timestamp of conversation creation
- updated_at (datetime): Timestamp of last update

**Relationships**:
- Many-to-one with User
- One-to-many with Message

**Validation**:
- user_id must reference existing User
- Required fields: user_id
- Each conversation belongs to exactly one user

## Entity: Message
**Fields**:
- id (integer): Unique identifier for the message
- user_id (string): Foreign key to User
- conversation_id (integer): Foreign key to Conversation
- role (string): Role of the message sender ("user" or "assistant")
- content (string): Content of the message
- created_at (datetime): Timestamp of message creation

**Relationships**:
- Many-to-one with User
- Many-to-one with Conversation

**Validation**:
- user_id must reference existing User
- conversation_id must reference existing Conversation
- role must be either "user" or "assistant"
- Required fields: user_id, conversation_id, role, content

## Entity: Task
**Fields**:
- id (integer): Unique identifier for the task
- user_id (string): Foreign key to User
- title (string): Title of the task
- description (string, optional): Detailed description of the task
- completed (boolean): Completion status of the task (default: false)
- created_at (datetime): Timestamp of task creation
- updated_at (datetime): Timestamp of last update

**Relationships**:
- Many-to-one with User

**Validation**:
- user_id must reference existing User
- Required fields: user_id, title
- completed defaults to false

## State Transitions

### Task State Transitions
- **Created**: Task is created with completed = false
- **Completed**: Task status changes from false to true via complete_task tool
- **Updated**: Task details (title, description) can be modified via update_task tool
- **Deleted**: Task is removed from the system via delete_task tool

### Conversation State Transitions
- **Started**: New conversation is created when user starts chatting
- **Active**: Conversation has messages added as user and agent interact
- **Inactive**: Conversation remains in database but not currently active

## Database Constraints

### Primary Keys
- User.id: Unique identifier
- Conversation.id: Unique identifier
- Message.id: Unique identifier
- Task.id: Unique identifier

### Foreign Keys
- Message.user_id → User.id
- Message.conversation_id → Conversation.id
- Conversation.user_id → User.id
- Task.user_id → User.id

### Indexes
- User.email: For efficient authentication lookups
- Conversation.user_id: For user-specific conversation queries
- Message.conversation_id: For conversation history retrieval
- Task.user_id: For user-specific task queries
- Message.created_at: For chronological message ordering