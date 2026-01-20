# ADR-002: Backend and Frontend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-07
- **Feature:** 001-agentic-chat-system
- **Context:** The system requires a technology stack that supports the agent-centric architecture, provides good developer experience, scales appropriately, and integrates well with the required AI and MCP components. The stack must support both backend services and frontend UI components.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We have selected a technology stack that includes both backend and frontend components working together:

**Backend Stack:**
- **Framework**: FastAPI for building the backend API
- **AI Integration**: OpenAI Agents SDK for AI reasoning and conversation management
- **ORM**: SQLModel for database operations
- **Database**: Neon Serverless PostgreSQL for data persistence
- **Authentication**: Better Auth for user authentication
- **MCP**: Python MCP SDK for Model Context Protocol implementation

**Frontend Stack:**
- **Framework**: Next.js 16 for the web application
- **UI Component**: OpenAI ChatKit for chat interface
- **Client Libraries**: React with modern JavaScript/TypeScript

## Consequences

### Positive

- **Python Ecosystem**: FastAPI and SQLModel provide excellent integration and type safety
- **AI Integration**: OpenAI Agents SDK and ChatKit offer seamless AI experience
- **Modern Frontend**: Next.js 16 provides excellent developer experience and performance
- **Scalability**: Neon Serverless PostgreSQL adapts to load automatically
- **Authentication**: Better Auth provides secure and easy-to-implement authentication
- **MCP Support**: Python MCP SDK enables proper MCP tool implementation
- **Type Safety**: TypeScript throughout the stack provides compile-time error catching
- **Developer Experience**: Well-documented and mature ecosystem with extensive community support

### Negative

- **Learning Curve**: Team members may need to learn new technologies (MCP, OpenAI Agents SDK)
- **Dependency Management**: Multiple complex dependencies may lead to version conflicts
- **Vendor Lock-in**: Heavy reliance on OpenAI's ecosystem and Neon's serverless offering
- **Complexity**: Multi-layered architecture increases overall system complexity
- **Cost**: Premium services (OpenAI, Neon) may become expensive at scale
- **Limited Control**: Some aspects are managed by third-party services

## Alternatives Considered

**Alternative Backend Stack A**: Node.js/Express + Prisma ORM + MongoDB
- Why rejected: Would not integrate as well with OpenAI's Python-based tools and would require additional language context switching

**Alternative Backend Stack B**: Django + Django REST Framework + PostgreSQL
- Why rejected: Would be more complex than needed for this API-focused application and lacks FastAPI's automatic API documentation and type validation

**Alternative Frontend Stack**: React with custom chat UI + Socket.io
- Why rejected: Would require building chat functionality from scratch instead of leveraging OpenAI's ChatKit optimized for AI interactions

**Alternative Architecture**: Monolithic application instead of layered architecture
- Why rejected: Would violate the MCP-first architecture principles and reduce scalability

## References

- Feature Spec: specs/001-agentic-chat-system/spec.md
- Implementation Plan: specs/001-agentic-chat-system/plan.md
- Related ADRs: ADR-001: Agent-Centric Architecture with MCP-First Design
- Evaluator Evidence: specs/001-agentic-chat-system/research.md
