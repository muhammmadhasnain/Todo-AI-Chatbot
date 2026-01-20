# Tasks: Better Auth for AI Todo Chatbot

**Feature**: Better Auth for AI Todo Chatbot
**Branch**: `001-better-auth`
**Created**: 2025-12-28
**Status**: OBSOLETE - Please use tasks.corrected.md instead
**Total Tasks**: 25
**Priority**: P1 (Critical), P2 (High), P3 (Medium)

## NOTICE: This task list is obsolete

This task list contains architectural violations and has been replaced by `tasks.corrected.md`. Please refer to the corrected task list for the proper Better Auth implementation approach.

### Key Issues with this version:
- Includes tasks for backend to implement authentication endpoints
- Mentions JWT token verification tasks for backend
- Does not follow Better Auth's recommended architecture

### Correct Approach:
- Frontend Better Auth client integration tasks
- Backend session verification service tasks
- Token forwarding utility implementation tasks
- Protected API endpoint implementation tasks

Please see `tasks.corrected.md` for the proper task breakdown.# Tasks: Better Auth for AI Todo Chatbot (CORRECTED)

**Feature**: Better Auth for AI Todo Chatbot
**Branch**: `001-better-auth`
**Created**: 2025-12-28
**Status**: Draft
**Total Tasks**: 25
**Priority**: P1 (Critical), P2 (High), P3 (Medium)

## Authentication Infrastructure Setup

### T001: Set up Better Auth client configuration
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: None
- **Description**: Configure Better Auth client in frontend with email/password and Google OAuth providers
- **Acceptance Criteria**:
  - [x] Better Auth client initialized in frontend with email/password support
  - [x] Google OAuth configured with proper client ID in frontend
  - [x] Environment variables set up for frontend authentication configuration
  - [x] Authentication client properly integrated with Next.js application
- **Tests**:
  - [ ] Unit test: Better Auth client initialization
  - [ ] Integration test: OAuth configuration verification
- **Files**: `frontend/lib/auth-client.ts`, `frontend/.env.local`

### T002: Implement backend session verification service
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T001
- **Description**: Create service to verify sessions via Better Auth API and extract user_id
- **Acceptance Criteria**:
  - [x] Service calls Better Auth API to verify session tokens
  - [x] Service extracts user_id from verified session and adds to request context
  - [x] Invalid sessions return 401 Unauthorized
  - [x] Session expiration handled properly via Better Auth API
- **Tests**:
  - [ ] Unit test: Valid session verification via Better Auth API
  - [ ] Unit test: Invalid session rejection
  - [ ] Unit test: Expired session handling
- **Files**: `backend/src/services/auth.py`, `backend/src/dependencies/auth.py`

### T003: Implement frontend token forwarding utility
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T001
- **Description**: Create utility to extract Better Auth session and forward to backend APIs
- **Acceptance Criteria**:
  - [x] Utility extracts current session from Better Auth client
  - [x] Utility includes session in Authorization header for backend API calls
  - [x] Utility handles session refresh automatically
  - [x] Utility provides error handling for authentication failures
- **Tests**:
  - [ ] Unit test: Session extraction from Better Auth
  - [ ] Unit test: Authorization header inclusion
  - [ ] Integration test: API calls with forwarded session
- **Files**: `frontend/lib/api-client.ts`, `frontend/hooks/use-api.ts`

## Protected API Endpoints

### T004: Implement protected chat endpoint with session verification
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T002
- **Description**: Create chat endpoint that verifies session via Better Auth API and processes user requests
- **Acceptance Criteria**:
  - [x] Chat endpoint accepts user_id in path and verifies session via Better Auth API
  - [x] Endpoint validates that user_id matches authenticated user
  - [x] Returns chat responses with proper user context
  - [x] Invalid sessions return appropriate error
- **Tests**:
  - [ ] Unit test: Valid session with matching user_id
  - [ ] Unit test: Invalid session rejection
  - [ ] Unit test: User_id mismatch detection
  - [ ] Integration test: Full chat flow with session verification
- **Files**: `backend/src/api/chat.py`, `backend/src/dependencies/auth.py`

### T005: Implement protected user data endpoints
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T002, T004
- **Description**: Create endpoints for user data (tasks, etc.) that verify sessions via Better Auth API
- **Acceptance Criteria**:
  - [x] Data endpoints verify session via Better Auth API
  - [x] Endpoints validate user_id matches authenticated user
  - [x] User can only access their own data
  - [x] Invalid sessions return appropriate error
- **Tests**:
  - [ ] Unit test: Valid session with data access
  - [ ] Unit test: Session-user_id validation
  - [ ] Unit test: Cross-user access prevention
  - [ ] Integration test: Full data access flow
- **Files**: `backend/src/api/tasks.py`, `backend/src/api/users.py`

## Frontend Authentication Integration

### T006: Implement login UI with Better Auth client
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T001
- **Description**: Create login UI that uses Better Auth client for authentication
- **Acceptance Criteria**:
  - [x] Login form uses Better Auth email/password authentication
  - [x] Google OAuth login button uses Better Auth client
  - [x] Authentication state properly managed in frontend
  - [x] Error handling for authentication failures
- **Tests**:
  - [ ] Unit test: Email/password login flow
  - [ ] Unit test: Google OAuth login flow
  - [ ] Integration test: Complete authentication flow
- **Files**: `frontend/components/auth/LoginForm.tsx`, `frontend/components/auth/AuthProvider.tsx`

### T007: Implement registration UI with Better Auth client
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T001, T006
- **Description**: Create registration UI that uses Better Auth client for account creation
- **Acceptance Criteria**:
  - [x] Registration form uses Better Auth email/password registration
  - [x] Email verification handled by Better Auth
  - [x] User account creation via Better Auth client
  - [x] Proper validation and error handling
- **Tests**:
  - [ ] Unit test: Registration form validation
  - [ ] Unit test: Account creation flow
  - [ ] Integration test: Complete registration flow
- **Files**: `frontend/components/auth/RegisterForm.tsx`, `frontend/components/auth/VerifyEmail.tsx`

## Backend Security Implementation

### T008: Implement user data isolation with verified user_id
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T002, T004, T005
- **Description**: Ensure all database operations are scoped by verified user_id from Better Auth session
- **Acceptance Criteria**:
  - [x] All database queries include user_id filter from verified session
  - [x] Users cannot access other users' data
  - [x] MCP tools receive authenticated user context
  - [x] Proper error handling for unauthorized access attempts
- **Tests**:
  - [ ] Unit test: User_id filtering in queries
  - [ ] Unit test: Cross-user access prevention
  - [ ] Integration test: Data isolation validation
- **Files**: `backend/src/models/user.py`, `backend/src/services/data.py`

### T009: Implement rate limiting for protected endpoints
- **Priority**: P2
- **Effort**: 0.5 day
- **Dependencies**: T004, T005
- **Description**: Add rate limiting to protected API endpoints based on authenticated user
- **Acceptance Criteria**:
  - [x] Rate limiting applied to protected endpoints
  - [x] Limits based on authenticated user_id
  - [x] Proper error responses for rate limit exceeded
  - [x] Rate limit counters properly managed
- **Tests**:
  - [ ] Unit test: Rate limit enforcement
  - [ ] Integration test: Rate limit exceeded handling
- **Files**: `backend/src/middleware/rate_limit.py`, `backend/src/api/chat.py`

## MCP Tool Integration

### T010: Implement authenticated MCP tool calls
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T002, T008
- **Description**: Ensure MCP tools receive authenticated user context from verified session
- **Acceptance Criteria**:
  - [x] MCP tool calls include verified user_id from Better Auth session
  - [x] Tools validate user context for operations
  - [x] User isolation maintained in MCP tool operations
  - [x] Proper error handling for unauthorized tool access
- **Tests**:
  - [ ] Unit test: User context passing to MCP tools
  - [ ] Integration test: MCP tool operations with user context
- **Files**: `backend/src/mcp/tools.py`, `backend/src/api/chat.py`

## Testing and Validation

### T011: Implement end-to-end authentication tests
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: All previous tasks
- **Description**: Create comprehensive end-to-end tests for authentication flows
- **Acceptance Criteria**:
  - [x] Complete authentication flow test (register → login → API access)
  - [x] Session verification end-to-end test
  - [x] User data isolation end-to-end test
  - [x] Error handling end-to-end test
- **Tests**:
  - [x] E2E test: Complete registration and login flow
  - [x] E2E test: API access with valid session
  - [x] E2E test: Session invalidation handling
- **Files**: `tests/e2e/auth.e2e.ts`, `tests/e2e/api.e2e.py`

### T012: Implement security validation tests
- **Priority**: P1
- **Effort**: 1 day
- **Dependencies**: T005, T008, T011
- **Description**: Create security-focused tests to validate proper authentication and authorization
- **Acceptance Criteria**:
  - [x] Cross-user data access prevention test
  - [x] Invalid session handling test
  - [x] Session token manipulation test
  - [x] Authentication bypass attempt test
- **Tests**:
  - [x] Security test: Cross-user access prevention
  - [x] Security test: Invalid token handling
  - [x] Security test: Session tampering attempts
  - [x] Security test: Authentication bypass attempts
- **Files**: `tests/security/auth.security.py`, `tests/security/api.security.py`