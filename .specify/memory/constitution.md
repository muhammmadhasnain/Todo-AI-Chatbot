<!-- Sync Impact Report:
     Version change: 1.2.0 → 1.3.0
     Modified principles: Technology Stack Requirements updated to include Next.js 16
     Added sections: None
     Removed sections: None
     Templates requiring updates: ✅ updated
     Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### MCP-First Architecture
Every feature must be exposed as an MCP tool; Tools must be stateless with persistent state in the database; All tools must have defined inputs, outputs, and error handling as specified in the MCP Tools Specification; All 5 required tools (add_task, list_tasks, complete_task, delete_task, update_task) must be implemented with proper contracts

### AI-Driven Interface
Every user interaction flows through the AI agent; Natural language processing required for all commands; AI must use MCP tools to manage application state

### Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced for all MCP tools and AI interactions

### Stateless Design
All conversation state must be persisted in the database; Server holds no in-memory state; Scalable and resilient architecture with horizontal scaling capabilities

### Database-Driven Architecture
All data models must follow the exact specifications: Task model (user_id, id, title, description, completed, created_at, updated_at), Conversation model (user_id, id, created_at, updated_at), Message model (user_id, id, conversation_id, role (user/assistant), content, created_at); All data operations must use SQLModel ORM with Neon Serverless PostgreSQL

### Observability and Error Handling
All MCP tool calls must be logged; Structured logging required for AI interactions; Graceful error handling with user-friendly responses; Proper error taxonomy with status codes as defined in specifications

### Security-First Approach
Authentication required for all operations; User data isolation mandatory; Secure API key handling and database connection management; All user data must be properly scoped by user_id

### Conversation Flow Management
Stateless request cycle must follow: Receive user message → Fetch conversation history from database → Build message array for agent → Store user message in database → Run agent with MCP tools → Agent invokes appropriate MCP tool(s) → Store assistant response in database → Return response to client; Server must hold NO state and be ready for next request

### AI Agent Behavior Specification
The AI agent must follow these behavioral rules: When user mentions adding/creating/remembering something, use add_task; When user asks to see/show/list tasks, use list_tasks with appropriate filter; When user says done/complete/finished, use complete_task; When user says delete/remove/cancel, use delete_task; When user says change/update/rename, use update_task; Always confirm actions with friendly response; Gracefully handle task not found and other errors

## MCP Tools Specification Requirements

The MCP server must expose the following 5 tools for the AI agent with exact contracts:

- **add_task**: Create new task; Requires user_id (string), title (string), optional description; Returns task_id, status, title
- **list_tasks**: Retrieve tasks; Requires user_id (string), optional status filter ("all", "pending", "completed"); Returns array of task objects
- **complete_task**: Mark task as complete; Requires user_id (string), task_id (integer); Returns task_id, status, title
- **delete_task**: Remove task; Requires user_id (string), task_id (integer); Returns task_id, status, title
- **update_task**: Modify task; Requires user_id (string), task_id (integer), optional title/description; Returns task_id, status, title

## Database Model Requirements

All database models must follow these exact specifications:

- **Task Model**: user_id, id, title, description, completed, created_at, updated_at (Todo items)
- **Conversation Model**: user_id, id, created_at, updated_at (Chat session)
- **Message Model**: user_id, id, conversation_id, role (user/assistant), content, created_at (Chat history)

## API Contract Standards

The chat API endpoint must follow these specifications:

- **Endpoint**: POST /api/{user_id}/chat
- **Purpose**: Send message & get AI response
- **Request Fields**:
  - conversation_id (integer, optional): Existing conversation ID (creates new if not provided)
  - message (string, required): User's natural language message
- **Response Fields**:
  - conversation_id (integer): The conversation ID
  - response (string): AI assistant's response
  - tool_calls (array): List of MCP tools invoked

## Natural Language Processing Requirements

The AI agent must understand and respond to these natural language commands:

- **"Add a task to buy groceries"** → Call add_task with title "Buy groceries"
- **"Show me all my tasks"** → Call list_tasks with status "all"
- **"What's pending?"** → Call list_tasks with status "pending"
- **"Mark task 3 as complete"** → Call complete_task with task_id 3
- **"Delete the meeting task"** → Call list_tasks first, then delete_task
- **"Change task 1 to 'Call mom tonight'"** → Call update_task with new title
- **"I need to remember to pay bills"** → Call add_task with title "Pay bills"
- **"What have I completed?"** → Call list_tasks with status "completed"

## Technology Stack Requirements

Frontend: Next.js 16 with OpenAI ChatKit, Backend: Python FastAPI, AI Framework: OpenAI Agents SDK, MCP Server: Official MCP SDK, ORM: SQLModel, Database: Neon Serverless PostgreSQL, Authentication: Better Auth

## Development Workflow

Use Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code; No manual coding allowed; MCP tools must follow specified contracts with proper parameters and return values; All database models (Task, Conversation, Message) must be implemented as specified

## ChatKit Deployment Requirements

OpenAI ChatKit setup must include: Domain allowlist configuration for security with deployed frontend URL; ChatKit domain key must be added to environment variables as NEXT_PUBLIC_OPENAI_DOMAIN_KEY; Proper configuration for both production and localhost environments

## Architecture Benefits

- **MCP Tools**: Standardized interface for AI to interact with your app
- **Single Endpoint**: Simpler API — AI handles routing to tools
- **Stateless Server**: Scalable, resilient, horizontally scalable
- **Tool Composition**: Agent can chain multiple tools in one turn
- **Key Stateless Architecture Benefits**: Scalability (any server instance handles any request), Resilience (server restarts don't lose conversation state), Horizontal scaling (load balancer routes to any backend), Testability (each request is independent and reproducible)

## Governance

All PRs/reviews must verify MCP tool compliance; All AI interactions must use defined tools; MCP tools must follow the specified contracts with proper error handling; All 5 required tools must be fully functional before any release; Database models must match exact specifications; API endpoints must follow contract standards

**Version**: 1.3.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-26