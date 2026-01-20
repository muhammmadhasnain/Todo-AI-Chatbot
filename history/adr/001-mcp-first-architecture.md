# ADR-1: MCP-First Architecture for Agentic Chat System

**Status:** Accepted
**Date:** 2026-01-07

## Context

The Agentic Chat System requires a robust architecture that enables AI agents to perform structured operations on user data (tasks, conversations, messages) while maintaining security, scalability, and maintainability. The system must support natural language processing for task management commands while ensuring proper authentication and authorization boundaries.

Traditional approaches would involve direct API calls from the agent to the database or complex middleware layers. However, the project requirements specifically call for an MCP-first architecture where all structured operations are performed through Model Context Protocol (MCP) tools.

## Decision

We will implement an MCP-first architecture where:

1. **Core Operations as MCP Tools**: All data operations (add_task, list_tasks, complete_task, delete_task, update_task) are implemented as MCP tools that run within an authenticated context
2. **Agent-Tool Interface**: The OpenAI Agent SDK communicates with MCP tools to perform structured operations
3. **Authentication Scoping**: Each MCP tool operates within a verified user session context, ensuring user data isolation
4. **Stateless Design**: The server maintains no in-memory state, with all context stored in the database
5. **API Transport Layer**: The REST API serves as a thin transport layer between frontend and agent services

## Alternatives Considered

1. **Direct Database Access**: The agent could directly query the database through a service layer. This would be simpler but lacks the security and standardization of MCP tools.

2. **Traditional REST API Architecture**: All operations could go through REST endpoints directly. This would be more conventional but doesn't leverage the benefits of structured tooling for AI agents.

3. **GraphQL with AI Gateway**: Using GraphQL for flexible queries with an AI gateway for natural language processing. This would provide flexibility but adds complexity without clear benefits over MCP tools.

## Consequences

**Positive:**
- Enhanced security through explicit tool contracts and authentication scoping
- Clear separation of concerns between AI reasoning and data operations
- Standardized interface for tool operations that can be easily extended
- Better auditability and monitoring of AI operations
- Compliance with project constitution requirements for MCP-first architecture

**Negative:**
- Increased architectural complexity with multiple layers
- Additional overhead in tool call processing
- Requires MCP SDK integration and maintenance
- Learning curve for team members unfamiliar with MCP

## References

- specs/001-agentic-chat-system/plan.md
- specs/001-agentic-chat-system/spec.md
- specs/001-agentic-chat-system/data-model.md
- backend/src/mcp/tools.py
- backend/src/agents/agent.py