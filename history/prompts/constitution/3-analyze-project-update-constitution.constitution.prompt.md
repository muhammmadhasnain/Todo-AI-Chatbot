---
id: 3
title: analyze-project-update-constitution
stage: constitution
date: 2025-12-25
surface: agent
model: Claude Sonnet 4.5
feature: todo-ai-chatbot
branch: master
user: Hasnain
command: /sp.constitution
labels: [constitution, todo-ai-chatbot, update, requirements]
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
      Analyze my project and update my constitution by adding any elements that are missing according to the requirements of my project                                           Phase III: Todo AI Chatbot
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
Tec  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                 │  │     │                on_id
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
The MCP server must expose the following tools for the AI agent:
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
[{"id": 1, "title": "Buy groceries", "completed": false}, ...]

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
Task Creaithout trailing slash)
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

Updated the Todo AI Chatbot constitution from version 1.1.0 to 1.2.0 to include missing elements identified from the project requirements:

1. Added "Database-Driven Architecture" principle specifying exact database model requirements
2. Added "Conversation Flow Management" principle detailing the stateless request cycle
3. Added "AI Agent Behavior Specification" principle with detailed behavioral rules
4. Added "Database Model Requirements" section with exact specifications for Task, Conversation, and Message models
5. Added "API Contract Standards" section with detailed endpoint specifications
6. Added "Natural Language Processing Requirements" section mapping user commands to agent actions
7. Added "ChatKit Deployment Requirements" section with domain allowlist configuration
8. Added "Architecture Benefits" section detailing the benefits of the chosen architecture

The constitution now fully aligns with all project requirements including database models, API contracts, agent behavior, conversation flow, and deployment specifications.

## Outcome

- ✅ Impact: Enhanced constitution with comprehensive project requirements coverage
- 🧪 Tests: N/A for documentation task
- 📁 Files: Updated .specify/memory/constitution.md to version 1.2.0
- 🔁 Next prompts: Can proceed with spec generation using /sp.spec
- 🧠 Reflection: Constitution now includes all technical specifications from requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate feature specification using /sp.spec