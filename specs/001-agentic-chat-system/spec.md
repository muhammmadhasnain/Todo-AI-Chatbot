# Feature Specification: Agentic Chat System using OpenAI ChatKit, OpenAI Agents SDK, MCP, and PostgreSQL

**Feature Branch**: `001-agentic-chat-system`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: " Specification: Agentic Chat System using OpenAI ChatKit, OpenAI Agents SDK, MCP, and PostgreSQL
Overview

This document specifies the architecture, responsibilities, and success criteria for an Agentic Chat System designed to support a task-driven conversational application (Todo Chatbot). The system integrates a OpenAI ChatKit-based frontend, a FastAPI backend, OpenAI Agents SDK for reasoning, and an MCP (Model Context Protocol) server for structured tool execution and database operations.

The goal is to ensure clear separation of concerns, correct message routing, and scalable agent-tool interaction, while maintaining conversation context and reliable persistence.

Target Audience

Software Architects


Backend & AI Engineers

Platform Engineers evaluating Agentic AI architectures

Technical Leads reviewing system design before implementation

Primary Focus

Reliable message flow from frontend to AI agent

Proper use of MCP as a tool execution layer, not a frontend API

Reduction of backend complexity by delegating decisions to the agent

Ensuring conversation context, task management, and persistence

Clear boundaries between UI, API, Agent, MCP, and Database

System Goals

Enable users to interact with an AI-powered task assistant via OpenAI ChatKit

Allow the AI agent to reason, decide, and call tools dynamically

Use MCP tools for structured operations (CRUD on tasks, messages, conversations)

Persist all relevant state in PostgreSQL (Neon DB)

Maintain a clean, extensible Agentic architecture

High-Level Architecture
User
 ↓
OpenAI ChatKit UI (Frontend)
 ↓
POST /api/chat
 ↓
FastAPI Chat Endpoint
 ↓
OpenAI Agents SDK (Agent + Runner)
 ↓
MCP Client (inside Agent)
 ↓
MCP Server (Tools)
 ↓
PostgreSQL (Neon DB)


Responses travel back through the same path in reverse.

Component Responsibilities
1. OpenAI ChatKit UI (Frontend)

Responsibilities:

Render chat interface

Capture user messages

Send messages to backend via /api/chat

Display agent responses

Non-Responsibilities:

Calling MCP tools directly

Managing business logic

Handling database operations

2. FastAPI Server
Chat Endpoint (POST /api/chat)

Responsibilities:

Authenticate user

Accept user message + session/conversation ID

Forward request to Agent Runner

Return agent response to frontend

Non-Responsibilities:

Decision-making logic

Tool execution

Direct database manipulation (outside of infrastructure needs)

3. OpenAI Agents SDK (Agent + Runner)

Responsibilities:

Interpret user intent

Maintain conversation context

Decide whether a tool is required

Call MCP tools via MCP client

Compose final natural-language response

Key Principle:

The agent is the only component allowed to decide when and which tool to call.

4. MCP Client (Inside Agent)

Responsibilities:

Translate agent tool calls into MCP-compliant requests

Communicate with MCP Server

Return structured results to the agent

Non-Responsibilities:

Business logic

Data persistence decisions

5. MCP Server

Responsibilities:

Expose well-defined tools (e.g., create_task, list_tasks, save_message)

Validate inputs and outputs

Act as a controlled execution layer

Non-Responsibilities:

Reasoning or intent detection

Direct user interaction

6. MCP Tools (mcp/tools.py)

Responsibilities:

Perform concrete operations:

Task CRUD

Message storage

Conversation tracking

Interact with PostgreSQL via ORM

Constraints:

Tools must be deterministic

Tools must not contain AI logic

7. PostgreSQL (Neon DB)

Responsibilities:

Persist application state:

Users

Conversations

Messages

Tasks

Message Flow Specification

User sends a message via OpenAI ChatKit UI

Frontend sends POST /api/chat

FastAPI forwards request to Agent Runner

Agent analyzes intent

Agent optionally calls MCP tool(s)

MCP Server executes tool(s)

Results returned to Agent

Agent generates final response

Response returned to frontend

## Skills Integration

This feature leverages specialized skills for implementation:

- **openai-agent-sdk**: For implementing the OpenAI Agents SDK integration, agent orchestration, and AI reasoning capabilities
- **mcp-sdk-skill**: For developing the MCP server, tools, and protocol implementation for structured tool execution
- **openai-chatkit**: For implementing the OpenAI ChatKit frontend interface and real-time chat functionality

## Success Criteria

✅ Frontend never calls MCP directly

✅ All user messages pass through the agent

✅ MCP tools are invoked only by the agent

✅ Conversation context is preserved across messages

✅ Tasks, messages, and conversations are persisted reliably

✅ System can add new tools without frontend changes"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interact with AI Task Assistant via Chat (Priority: P1)

A logged-in user opens the OpenAI ChatKit interface and types natural language commands to manage their tasks. The user can ask to add, list, complete, update, or delete tasks using conversational language. The AI agent processes the request and responds appropriately, showing the results in the chat interface.

**Why this priority**: This is the core value proposition of the system - allowing users to manage tasks through natural language interaction with an AI assistant.

**Independent Test**: Can be fully tested by sending a message like "Add a task to buy groceries" and verifying that the AI processes it, creates a task, and returns an appropriate response.

**Acceptance Scenarios**:

1. **Given** user is authenticated and on the chat page, **When** user sends a message to add a task, **Then** AI agent processes the request, creates the task via MCP tools, and responds with confirmation
2. **Given** user has existing tasks, **When** user asks to list tasks, **Then** AI agent retrieves tasks via MCP tools and presents them in natural language format

---

### User Story 2 - Maintain Conversation Context (Priority: P2)

A user engages in a multi-turn conversation with the AI assistant, where the agent remembers context from previous exchanges and maintains conversation flow. The user can reference previously mentioned tasks or continue discussions about ongoing topics.

**Why this priority**: Essential for a natural conversational experience where users expect continuity across multiple interactions.

**Independent Test**: Can be tested by having a conversation where the user refers back to tasks mentioned in previous messages and verifying the agent maintains context appropriately.

**Acceptance Scenarios**:

1. **Given** user has had a previous conversation with the agent, **When** user makes a follow-up request referencing prior context, **Then** the agent recognizes the context and responds appropriately

---

### User Story 3 - Access Historical Conversations (Priority: P3)

A user can return to previous conversations and continue from where they left off, with the system maintaining conversation history and task state across sessions.

**Why this priority**: Important for user productivity and experience, allowing them to pick up where they left off in their task management workflow.

**Independent Test**: Can be tested by creating a conversation, logging out, logging back in, and verifying access to previous conversations and associated tasks.

**Acceptance Scenarios**:

1. **Given** user has previous conversations, **When** user accesses the chat interface, **Then** they can view and continue previous conversations with preserved context

---

### Edge Cases

- What happens when the AI agent encounters an ambiguous request that could map to multiple MCP tools?
- How does the system handle network interruptions during agent processing?
- What occurs when the user sends multiple rapid-fire messages before receiving responses?
- How does the system handle invalid or malformed tool calls from the agent?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate users before allowing access to the chat interface
- **FR-002**: System MUST process user messages through the AI agent for intent interpretation
- **FR-003**: System MUST allow the agent to call MCP tools based on interpreted user intent
- **FR-004**: System MUST persist all user tasks, messages, and conversations in PostgreSQL
- **FR-005**: System MUST ensure that MCP tools are called only by the AI agent, not directly by the frontend
- **FR-006**: System MUST maintain conversation context between user interactions
- **FR-007**: System MUST route all user messages through the designated chat endpoint (POST /api/chat)
- **FR-008**: System MUST provide real-time chat interface updates as the agent processes requests
- **FR-009**: System MUST validate that users can only access their own tasks and conversations
- **FR-010**: System MUST handle agent processing errors gracefully and provide user-friendly responses

### Key Entities *(include if feature involves data)*

- **User**: Represents an authenticated user with unique identifier, authentication tokens, and personal data
- **Conversation**: Represents a logical grouping of related messages between user and agent, tied to a specific user
- **Message**: Represents an individual exchange in a conversation, including content, timestamp, and sender type (user/assistant)
- **Task**: Represents a user's to-do item with title, description, completion status, timestamps, and user ownership

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully interact with the AI assistant to manage tasks through natural language with 95% accuracy in intent recognition
- **SC-002**: Agent response time remains under 5 seconds for 90% of user requests
- **SC-003**: 90% of user-initiated task operations (create, update, complete, delete) are successfully processed and persisted
- **SC-004**: Users can maintain conversation context across multiple interactions without loss of relevant information
- **SC-005**: System supports concurrent multi-user access with proper data isolation ensuring users only see their own tasks and conversations
- **SC-006**: New MCP tools can be added to the system without requiring frontend changes
