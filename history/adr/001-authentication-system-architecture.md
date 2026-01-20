# ADR-001: Authentication System Architecture

## Status
Accepted

## Context
The AI Todo Chatbot application requires a robust authentication system that supports both email/password and Google OAuth login methods. The system must provide secure token-based authentication while maintaining a stateless backend architecture as required by the project constitution. User data isolation is critical to ensure users can only access their own data.

## Decision
We have selected Better Auth as the primary authentication provider with JWT tokens and refresh tokens for maintaining stateless authentication. The architecture includes:

- Better Auth for user management and authentication flows
- JWT tokens with short-lived access tokens (1 hour) and long-lived refresh tokens (30 days)
- FastAPI middleware for token verification and user context injection
- User data isolation through user_id validation in all data access operations
- MCP tools with authenticated user context for data operations

## Alternatives Considered
1. **Custom authentication system**: Would require more development time and security expertise
2. **Session-based authentication**: Would violate stateless architecture requirements
3. **OAuth-only with Google**: Would limit user choice and acquisition
4. **Multiple OAuth providers**: Would increase complexity beyond requirements

## Consequences
### Positive
- Leverages industry-standard security practices
- Reduces development time compared to custom solution
- Supports horizontal scaling with stateless architecture
- Provides multiple authentication options for users
- Ensures user data isolation through validation

### Negative
- Dependency on external service (Better Auth)
- Token revocation complexity with JWT tokens
- Additional complexity for implementing custom user data requirements

## Implementation
- Better Auth configured with email/password and Google OAuth
- JWT tokens validated through FastAPI middleware
- All database queries scoped by user_id
- MCP tools receive authenticated user context
- Token refresh and logout functionality implemented

## Notes
This architecture aligns with the project's security-first approach and allows focus on core AI chatbot functionality while maintaining required security measures.