# ADR-001: Agent-Centric Architecture with MCP-First Design

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-07
- **Feature:** 001-agentic-chat-system
- **Context:** The system requires an architecture that allows an AI agent to interpret user intent and make decisions about which tools to call, while maintaining clear separation of concerns between frontend, backend, and data operations. The architecture must support stateless servers and enforce security boundaries.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement an agent-centric architecture where the AI agent is the single decision-maker responsible for interpreting user intent and selecting appropriate tools to execute. This architecture clusters several related components:

- **OpenAI Agents SDK**: Used for reasoning and conversation management
- **MCP Server**: Exposes 5 specific tools (add_task, list_tasks, complete_task, delete_task, update_task) that the AI agent can call
- **Agent-Driven Flow**: All user interactions flow through the AI agent for intent interpretation
- **MCP-First Tool Execution**: Database operations are performed exclusively through MCP tools, not direct API calls
- **Stateless Backend**: Server holds no in-memory state, all conversation context is loaded from/persisted to database

## Consequences

### Positive

- Clear separation of concerns with well-defined responsibilities for each component
- Scalable architecture with stateless servers that support horizontal scaling
- Enforced security boundaries with MCP tools as the only path for data operations
- Flexibility for the AI agent to compose multiple tools in a single interaction
- Future extensibility - new capabilities can be added via new MCP tools without frontend changes
- Predictable debugging and observability with structured tool calls

### Negative

- Additional complexity with multiple architectural layers
- Potential latency overhead from tool invocation layer
- Increased development complexity due to distributed architecture
- Learning curve for team members to understand the agent-centric flow
- Dependency on OpenAI's agent platform and MCP protocol

## Alternatives Considered

**Backend-Driven Architecture**: Traditional approach where backend processes user intent and directly calls database operations.
- Why rejected: Would violate the agent-centric principle and reduce AI's decision-making capability

**Direct Database Access from Agent**: Allow the AI agent to connect directly to the database.
- Why rejected: Would bypass security controls and violate the MCP-first architecture principle

**Frontend-Initiated Tool Calls**: Allow the frontend to call MCP tools directly based on user commands.
- Why rejected: Would violate the principle that all user interactions flow through the AI agent

## References

- Feature Spec: specs/001-agentic-chat-system/spec.md
- Implementation Plan: specs/001-agentic-chat-system/plan.md
- Related ADRs: ADR-001: Authentication System Architecture, ADR-001: Frontend Chat Component Architecture with OpenAI ChatKit
- Evaluator Evidence: specs/001-agentic-chat-system/research.md
