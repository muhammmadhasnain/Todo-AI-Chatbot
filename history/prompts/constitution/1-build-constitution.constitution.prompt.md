---
id: 1
title: build-constitution
stage: constitution
date: 2025-12-25
surface: agent
model: Claude Sonnet 4.5
feature: todo-ai-chatbot
branch: master
user: Hasnain
command: /sp.constitution
labels: [constitution, todo-ai-chatbot, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
    build a consitution                                                          Phase III: Todo AI Chatbot
Basic Level Functionality
Objective: Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture and using Claude Code and Spec-Kit Plus.
Development Approach: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will review the process, prompts, and iterations to judge each phase and project.
Requirements
Implement conversational interface for all Basic Level features
Use OpenAI Agents SDK for AI logic
Build MCP server with Official MCP SDK that exposes task operations as tools
Stateless chat endpoint that persists conversation state to database
AI agents use MCP tools to manage tasks. The MCP tools will also be stateless and will store state in the database.
Technology Stack
Component
Technology
Frontend
OpenAI ChatKit
Backend
Python FastAPI
AI Framework
OpenAI Agents SDK
MCP Server
Official MCP SDK
ORM
SQLModel
Database
Neon Serverless PostgreSQL
Authentication
Better Auth

Architecture
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │    Neon DB      │
│  (Frontend)     │     │  │  POST /api/chat              must expose the following tools for the AI agent:
Tool: add_task
Purpose
Create a new task
Parameters
user_id (string, required), title (string, required), description (string, optional)
Returns
task_id, status, title
Example Input
{“user_id”: “ziakhan”, "title": "Buy groceries", "description": "Milk, eggs, bread"}
Example Output
{"task_id": 5, "status": "created", "title": "Buy groceries"}

Tool: list_tasks
Purpose
Retrieve tasks from the list
Parameters
status (string, optional: "all", "pending", "completed")
Returns
Array of task objects
Example Input
{user_id (string, required), "status": "pending"}
Example Output
[{"id": 1, "title": "Bu──────────────────────────────┘     └─────────────────┘
Database Models
Model
Fields
Description
Task
user_id, id, title, description, completed, created_at, updated_at
Todo items
Conversation
user_id, id, created_at, updated_at
Chat session
Message
user_id, id, conversation_id, role (user/assistant), content, created_at
Chat history

Chat API Endpoint
Method
Endpoint
Description
POST
/api/{user_id}/chat
Send message & get AI response

Request
Field
Type
Required
Description
conversation_id
integer
No
Existing conversation ID (creates new if not provided)
message
string
Yes
User's natural language message

Response
Field
Type
Description
conversation_id
integer
The conversation ID
response
string
AI assistant's response
tool_calls
array
List of MCP tools invoked

MCP Tools Specification
The MCP servery groceries", "completed": false}, ...]

Tool: complete_task
Purpose
Mark a task as complete
Parameters
user_id (string, required), task_id (integer, required)
Returns
task_id, status, title
Example Input
{“user_id”: “ziakhan”, "task_id": 3}
Example Output
{"task_id": 3, "status": "completed", "title": "Call mom"}

Tool: delete_task
Purpose
Remove a task from the list
Parameters
user_id (string, required), task_id (integer, required)
Returns
task_id, status, title
Example Input
{“user_id”: “ziakhan”, "task_id": 2}
Example Output
{"task_id": 2, "status": "deleted", "title": "Old task"}

Tool: update_task
Purpose
Modify task title or description
Parameters
user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
Returns
task_id, status, title
Example Input
{“user_id”: “ziakhan”, "task_id": 1, "title": "Buy groceries and fruits"}
Example Output
{"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}

Agent Behavior Specification
Behavior
Description
Task Creation
When user mentions adding/creating/remembering something, use add_task
Task Listing
When user asks to see/show/list tasks, use list_tasks with appropriate filter
Task Completion
When user says done/complete/finished, use complete_task
Task Deletion
When user says delete/remove/cancel, use delete_task
Task Update
When user says change/update/rename, use update_task
Confirmation
Always confirm actions with friendly response
Error Handling
Gracefully handle task not found and other errors


Conversation Flow (Stateless Request Cycle)
Receive user message
Fetch conversation history from database
Build message array for agent (history + new message)
Store user message in database
Run agent with MCP tools
Agent invokes appropriate MCP tool(s)
Store assistant response in database
Return response to client
Server holds NO state (ready for next request)
Natural Language Commands
The chatbot should understand and respond to:
User Says
Agent Should
"Add a task to buy groceries"
Call add_task with title "Buy groceries"
"Show me all my tasks"
Call list_tasks with status "all"
"What's pending?"
Call list_tasks with status "pending"
"Mark task 3 as complete"
Call complete_task with task_id 3
"Delete the meeting task"
Call list_tasks first, then delete_task
"Change task 1 to 'Call mom tonight'"
Call update_task with new title
"I need to remember to pay bills"
Call add_task with title "Pay bills"
"What have I completed?"
Call list_tasks with status "completed"

Deliverables
GitHub repository with:
/frontend – ChatKit-based UI
/backend – FastAPI + Agents SDK + MCP
/specs – Specification files for agent and MCP tools
Database migration scripts
README with setup instructions

Working chatbot that can:
Manage tasks through natural language via MCP tools
Maintain conversation context via database (stateless server)
Provide helpful responses with action confirmations
Handle errors gracefully
Resume conversations after server restart

OpenAI ChatKit Setup & Deployment
Domain Allowlist Configuration (Required for Hosted ChatKit)

Before deploying your chatbot frontend, you must configure OpenAI's domain allowlist for security:

Deploy your frontend first to get a production URL:
 Vercel: `https://your-app.vercel.app`
 GitHub Pages: `https://username.github.io/repo-name`
 Custom domain: `https://yourdomain.com`

Add your domain to OpenAI's allowlist:
Navigate to: https://platform.openai.com/settings/organization/security/domain-allowlist
Click "Add domain"
Enter your frontend URL (without trailing slash)
Save changes

Get your ChatKit domain key:
After adding the domain, OpenAI will provide a domain key
Pass this key to your ChatKit configuration

Environment Variables
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here

Note: The hosted ChatKit option only works after adding the correct domains under Security → Domain Allowlist. Local development (`localhost`) typically works without this configuration.
Key Architecture Benefits
Aspect
Benefit
MCP Tools
Standardized interface for AI to interact with your app
Single Endpoint
Simpler API — AI handles routing to tools
Stateless Server
Scalable, resilient, horizontally scalable
Tool Composition
Agent can chain multiple tools in one turn


Key Stateless Architecture Benefits
Scalability: Any server instance can handle any request
Resilience: Server restarts don't lose conversation state
Horizontal scaling: Load balancer can route to any backend
Testability: Each request is independent and reproducible
```

## Response snapshot

Created a constitution for the Todo AI Chatbot project with the following key principles:
- MCP-First Architecture: Every feature must be exposed as an MCP tool with stateless design
- AI-Driven Interface: All user interactions flow through the AI agent
- Test-First approach: TDD mandatory with Red-Green-Refactor cycle
- Stateless Design: All conversation state persisted in database
- Observability and Error Handling: Structured logging and graceful error handling
- Security-First Approach: Authentication required for all operations

The constitution also includes technology stack requirements (OpenAI ChatKit, FastAPI, OpenAI Agents SDK, etc.) and development workflow guidelines using the Agentic Dev Stack approach.

## Outcome

- ✅ Impact: Created foundational constitution document for Todo AI Chatbot project
- 🧪 Tests: N/A for documentation task
- 📁 Files: Updated .specify/memory/constitution.md with new project constitution
- 🔁 Next prompts: Can proceed with spec generation using /sp.spec
- 🧠 Reflection: Constitution properly captures the key architectural principles of the Todo AI Chatbot project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate feature specification using /sp.spec