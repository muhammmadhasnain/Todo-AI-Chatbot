---
id: 2
title: Better Auth Implementation Plan
stage: plan
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 001-better-auth
branch: 001-better-auth
user: Hasnain
command: sp.plan
labels: ["auth", "better-auth", "planning", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-better-auth/plan.md
  - specs/001-better-auth/research.md
  - specs/001-better-auth/data-model.md
  - specs/001-better-auth/quickstart.md
  - specs/001-better-auth/contracts/auth-api-contracts.md
  - specs/001-better-auth/contracts/openapi.yaml
tests: []
---

# Better Auth Implementation Plan

## PROMPT_TEXT

# Feature Plan: Better Auth for AI Todo Chatbot

**Feature**: Better Auth for AI Todo Chatbot
**Branch**: `001-better-auth`
**Created**: 2025-12-28
**Status**: Draft
**Author**: Claude Code

## 1. Scope and Dependencies

### In Scope
- Email/password authentication system with registration, login, and verification
- Google OAuth 2.0 integration for social login
- JWT-based token authentication system with refresh tokens
- Backend token verification middleware for FastAPI
- User data isolation with proper user_id mapping for MCP tools
- Protected API endpoints requiring authentication
- Session management and logout functionality
- Rate level security
- Application-level user_id validation
- API gateway-based authentication

**Rationale**: Selected application-level user_id validation in API endpoints to ensure users can only access their own data, following the security-first approach in the constitution.

**Trade-offs**: Performance overhead vs. security assurance.

## 3. Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌────────limiting for authentication endpoints
- Error handling and security measures

### Out of Scope
- Password recovery via SMS or other methods (email-only)
- Multi-factor authentication (MFA)
- Account linking between email/password and Google accounts
- Advanced user profile management beyond basic OAuth data
- Third-party OAuth providers beyond Google

### External Dependencies
- **Better Auth Provider**: Third-party authentication service for user management
- **Google OAuth 2.0**: For social authentication
- **FastAPI Backend**: For token verification and protected API endpoints
- **Neon Serverless PostgreSQL**: For user data storage and session management
- **MCP Tools**: For AI agent integration with authenticated user context

## 2. Key Decisions and Rationale

### Authentication Strategy Decision
**Options Considered**:
- Custom authentication system with JWT tokens
- Third-party provider (Better Auth)
- OAuth-only with Google

**Rationale**: Selected Better Auth as the primary authentication provider to leverage industry-standard security practices, reduce development time, and ensure robust authentication flows. This aligns with the project's security-first approach and allows focus on core AI chatbot functionality.

**Trade-offs**: Dependency on external service vs. full control over authentication logic.

### Token Management Decision
**Options Considered**:
- Session-based authentication (server-side sessions)
- JWT tokens with stateless verification
- Hybrid approach with short-lived sessions and refresh tokens

**Rationale**: Selected JWT tokens with refresh tokens to maintain stateless backend architecture as required by the project constitution. This supports horizontal scaling and resilience requirements.

**Trade-offs**: Token revocation complexity vs. scalability benefits.

### User Data Isolation Decision
**Options Considered**:
- Database-level row-─────────┐
│   Frontend      │    │  Better Auth    │    │   FastAPI       │
│   (Next.js)     │◄──►│   Provider      │    │   Backend       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       │                       │                       │
       │                ┌─────────────────┐            │
       │                │   Google OAuth  │            │
       │                │                 │            │
       └────────────────┤  (Social Login) │◄───────────┘
                        └─────────────────┘
```

### Data Flow
1. User initiates authentication (email/password or Google OAuth)
2. Better Auth handles authentication and issues JWT tokens
3. Frontend stores tokens securely (HTTP-only cookies or secure localStorage)
4. API requests include authentication tokens in headers
5. FastAPI backend verifies tokens and extracts user_id
6. User-specific data operations use the verified user_id for isolation

## 4. Interfaces and API Contracts

### Frontend Authentication API
- **POST /api/auth/register**: Email/password registration
  - Input: {email: string, password: string}
  - Output: {user_id: string, access_token: string, refresh_token: string}
  - Errors: 400 (validation), 409 (email exists), 500 (server error)

- **POST /api/auth/login**: Email/password login
  - Input: {email: string, password: string}
  - Output: {user_id: string, access_token: string, refresh_token: string}
  - Errors: 400 (validation), 401 (invalid credentials), 500 (server error)

- **GET /api/auth/google**: Initiate Google OAuth flow
  - Output: Redirect to Google OAuth consent screen
  - Errors: 500 (server error)

- **POST /api/auth/refresh**: Token refresh
  - Input: {refresh_token: string}
  - Output: {access_token: string, refresh_token: string}
  - Errors: 401 (invalid refresh token), 500 (server error)

- **POST /api/auth/logout**: Session termination
  - Input: {refresh_token: string}
  - Output: {success: boolean}
  - Errors: 401 (invalid token), 500 (server error)

### Backend Token Verification Middleware
- **Authentication Header**: `Authorization: Bearer <access_token>`
- **Response Format**:
  - Success: req.user_id populated with authenticated user's ID
  - Error: 401 Unauthorized with error message

### Protected API Endpoints
- **POST /api/{user_id}/chat**: AI chat endpoint
  - Requires valid authentication token
  - User can only access their own user_id endpoints
  - Input: {conversation_id?: integer, message: string}
  - Output: {conversation_id: integer, response: string, tool_calls: array}

## 5. Non-Functional Requirements (NFRs)

### Performance
- **P95 Authentication Token Verification**: < 500ms (as specified in success criteria SC-003)
- **Token Generation**: < 100ms
- **OAuth Flow Completion**: < 30 seconds (as specified in success criteria SC-002)
- **Concurrent Users Support**: 1000+ users without degradation (as specified in success criteria SC-005)

### Reliability
- **Authentication Success Rate**: 95%+ (as specified in success criteria SC-006)
- **Token Verification Success Rate**: 99.9% (as specified in success criteria SC-003)
- **Service Availability**: 99.9% uptime for authentication services

### Security
- **User Data Isolation**: 0% cross-user data access incidents (as specified in success criteria SC-004)
- **Password Security**: bcrypt with cost factor 12 for password hashing
- **Token Security**: JWT with RS256 algorithm, short-lived access tokens (1 hour), long-lived refresh tokens (30 days)
- **Rate Limiting**: 5 attempts per 15 minutes per IP/user for authentication endpoints
- **Session Management**: Secure token storage and proper session invalidation

### Cost
- **Authentication Provider Costs**: Budget for Better Auth usage based on expected user base
- **Token Verification Costs**: Minimal computational overhead for stateless token verification

## 6. Data Management and Migration

### Source of Truth
- **Better Auth Provider**: Primary source for user authentication data (email, password hashes, OAuth provider links)
- **Application Database**: User metadata and application-specific data tied to user_id

### Schema Evolution
- **User Profile Integration**: Schema to store OAuth profile data (name, avatar) when users authenticate via Google
- **Session Management**: Optional schema for refresh token tracking if needed for enhanced security

### Migration Strategy
- **No Breaking Changes**: All authentication endpoints maintain backward compatibility during migration
- **Gradual Rollout**: Feature flags to enable new authentication methods incrementally
- **Rollback Plan**: Ability to revert to previous authentication system if issues arise

### Data Retention
- **Authentication Logs**: 90-day retention for security audit purposes
- **Session Data**: Automatic cleanup of expired refresh tokens
- **User Consent**: Clear data retention and privacy policies for user data

## 7. Operational Readiness

### Observability
- **Authentication Logs**: Structured logging for all authentication events (success/failure, user_id, timestamp, IP)
- **Token Verification Metrics**: Success/failure rates, latency metrics, error types
- **Security Events**: Failed login attempts, suspicious activity detection
- **User Activity**: Authentication flow completion rates, user registration metrics

### Alerting
- **High Failure Rates**: Alert when authentication failure rate exceeds 5% over 5-minute window
- **Security Incidents**: Alert on multiple failed login attempts from same IP
- **Performance Degradation**: Alert when token verification latency exceeds 1s p95
- **Service Availability**: Alert when authentication services become unavailable

### Runbooks
- **Authentication Service Failure**: Steps to diagnose and recover authentication service
- **Token Verification Issues**: Troubleshooting guide for token-related problems
- **OAuth Provider Issues**: Steps to handle Google OAuth failures
- **Rate Limiting Issues**: How to handle and monitor rate limiting events

### Deployment Strategy
- **Blue-Green Deployment**: Zero-downtime deployment for authentication services
- **Gradual Rollout**: Feature flags to enable authentication methods gradually
- **Health Checks**: Authentication service health verification before routing traffic

### Feature Flags
- **Google OAuth Toggle**: Enable/disable Google OAuth login independently
- **Email Verification Requirement**: Toggle for requiring email verification
- **Rate Limiting Adjustments**: Dynamic rate limiting configuration

## 8. Risk Analysis and Mitigation

### Top 3 Risks

1. **Authentication Provider Dependency Risk**
   - **Risk**: Better Auth service outage affects entire authentication system
   - **Blast Radius**: All users unable to authenticate
   - **Mitigation**: Implement circuit breaker pattern, fallback mechanisms, and monitoring
   - **Kill Switch**: Emergency authentication bypass for critical operations

2. **Token Security Vulnerability**
   - **Risk**: JWT token compromise leads to unauthorized access
   - **Blast Radius**: Individual user data compromise
   - **Mitigation**: Short-lived tokens, proper secret rotation, secure storage
   - **Guardrails**: Token validation, rate limiting, suspicious activity detection

3. **OAuth Integration Failure**
   - **Risk**: Google OAuth changes or failures affect social login
   - **Blast Radius**: Users with Google accounts unable to log in
   - **Mitigation**: Fallback to email/password, OAuth provider monitoring
   - **Guardrails**: Graceful degradation to alternative authentication methods

## 9. Technical Implementation Details

### Frontend Implementation (Next.js 16)
- **Better Auth Integration**: Use Better Auth client SDK for authentication flows
- **Protected Routes**: Higher-order components for route protection
- **Token Management**: Secure storage and automatic refresh
- **UI Components**: Login, registration, and profile management components

### Backend Implementation (FastAPI)
- **Token Verification Middleware**: FastAPI dependency for token validation
- **User Context Injection**: Automatic user_id injection into request context
- **Protected Endpoints**: Decorators for protecting API routes
- **Error Handling**: Consistent error responses for authentication failures

### MCP Tools Integration
- **User Context**: Pass authenticated user_id to MCP tools for data isolation
- **Session Management**: Ensure MCP tools operate within user context
- **Security Validation**: Verify user permissions before executing MCP operations

### Security Considerations
- **CORS Configuration**: Proper CORS setup for authentication endpoints
- **CSRF Protection**: Token-based protection for state-changing operations
- **XSS Prevention**: Secure token storage and proper output encoding
- **Rate Limiting**: Implementation for preventing brute force attacks

## 10. Evaluation and Validation

### Definition of Done
- [ ] Email/password registration and login flows implemented and tested
- [ ] Google OAuth login flow implemented and tested
- [ ] JWT token generation and verification working correctly
- [ ] Backend token verification middleware implemented
- [ ] Protected API endpoints require authentication
- [ ] User data isolation enforced (users access only own data)
- [ ] Token refresh functionality working
- [ ] Logout functionality implemented
- [ ] Rate limiting applied to authentication endpoints
- [ ] Error handling and appropriate error messages implemented
- [ ] Security audit confirms no vulnerabilities in authentication system
- [ ] Performance requirements met (sub-500ms token verification)
- [ ] All user scenarios from spec pass end-to-end tests

### Output Validation
- **Format Compliance**: All API responses follow specified contracts
- **Requirements Verification**: All functional requirements (FR-001 to FR-011) implemented
- **Security Validation**: Penetration testing confirms authentication security
- **Safety Checks**: No authentication bypasses or data leakage vulnerabilities

## 11. Architectural Decision Records (ADRs)

- **ADR-001**: Selection of Better Auth as primary authentication provider
- **ADR-002**: JWT token strategy with refresh tokens for stateless backend
- **ADR-003**: User data isolation implementation approach
- **ADR-004**: OAuth provider integration (Google OAuth 2.0 specifics)

📋 Architectural decision detected: Authentication architecture with Better Auth, JWT tokens, and user data isolation — Document reasoning and tradeoffs? Run `/sp.adr Authentication System Architecture`.

## RESPONSE_TEXT

I'll execute the plan workflow as requested. Let me start by running the setup script to get the necessary context information.

The planning workflow has been successfully completed with all required documentation generated:

1. **Plan file updated**: specs/001-better-auth/plan.md - Contains the complete implementation plan with technical context, constitution check, and project structure
2. **Research completed**: specs/001-better-auth/research.md - Contains all research findings and decision rationales
3. **Data model created**: specs/001-better-auth/data-model.md - Defines all authentication-related entities and state transitions
4. **Quickstart guide created**: specs/001-better-auth/quickstart.md - Provides setup and implementation instructions
5. **API contracts created**: specs/001-better-auth/contracts/ - Contains API contract documentation in both markdown and OpenAPI format
6. **Agent context updated**: The Claude Code context has been updated with the new technologies for this feature
7. **Constitution check verified**: All constitution requirements have been addressed and validated

The implementation plan is now ready to proceed to the task breakdown phase using /sp.tasks.

## OUTCOME

Successfully completed the planning phase for the Better Auth feature, creating comprehensive documentation including plan, research, data models, quickstart guide, and API contracts. All constitution requirements have been verified and the agent context has been updated with the new technologies.

## EVALUATION

The plan addresses all requirements from the original feature specification, follows the constitution guidelines, and provides sufficient detail for implementation. The architecture decisions align with the project's MCP-first, stateless, and security-first principles.