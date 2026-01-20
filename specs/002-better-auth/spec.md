# Feature Specification: Better Auth for AI Todo Chatbot

**Feature Branch**: `001-better-auth`
**Created**: 2025-12-28
**Status**: OBSOLETE - Please use spec.corrected.md instead
**Input**: User description: "Better Auth for AI Todo Chatbot

## NOTICE: This specification is obsolete

This specification contains architectural violations and has been replaced by `spec.corrected.md`. Please refer to the corrected specification for the proper Better Auth implementation architecture.

### Key Issues with this version:
- Incorrectly describes backend implementing authentication endpoints
- Mentions manual JWT verification by backend
- Does not follow Better Auth's recommended architecture

### Correct Architecture:
- Better Auth acts as the identity provider
- Frontend uses Better Auth client for authentication flows
- Backend only verifies sessions via Better Auth API
- No manual JWT handling by backend

Please see `spec.corrected.md` for the proper implementation specification.# Feature Specification: Better Auth for AI Todo Chatbot (CORRECTED)

**Feature Branch**: `001-better-auth`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Better Auth for AI Todo Chatbot

## Purpose
Design and implement a secure, dual-mode authentication system for the AI-driven Todo Chatbot that supports both **Email/Password** and **Google OAuth** login methods, ensuring reliable user identity verification, session management, and secure access control for all backend APIs and MCP tools.

The architecture follows Better Auth's recommended pattern where Better Auth acts as the identity provider, the frontend consumes authentication state, and the backend only verifies sessions via Better Auth API.

## Target Audience
- Full-stack developers building the Todo AI Chatbot
- Backend engineers integrating authentication with MCP & AI agent
- Frontend engineers implementing login UI and protected routes
- QA engineers verifying auth flows and security

## Focus
Enable secure user authentication flows with:
1. Traditional email/password login & signup
2. Social Google login via OAuth

Ensure **session-based authentication** that is verified by the backend via Better Auth API, strictly enforces user isolation, and integrates seamlessly with Better Auth provider and the FastAPI backend for stateless session management.

## Success Criteria
- 🟢 Email/password signup and login flows implemented and tested via Better Auth
- 🟢 Google OAuth login flow implemented and tested via Better Auth
- 🟢 Sessions issued by Better Auth and verified by backend via Better Auth API
- 🟢 Backend session verification service implemented (not JWT decoding)
- 🟢 Protected APIs including /api/{user_id}/chat require valid Better Auth sessions
- 🟢 Sessions correctly map to unique user_id for MCP tool calls
- 🟢 All session flows and edge cases are documented with error handling

## Constraints
- Must support **Email/Password + Google OAuth** login only
- Auth logic must be stateless on backend (no in-memory sessions)
- Must integrate with Better Auth provider (3rd-party auth service)
- Session verification must be secure and reliable via Better Auth API
- Public endpoints allowed for registration, email verification, and password reset initiation (but require proper validation and rate limiting)

## Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
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

## Data Flow
1. User initiates authentication (email/password or Google OAuth) via Better Auth
2. Better Auth handles authentication and issues session tokens
3. Frontend stores session state securely (Better Auth client manages tokens)
4. API requests include Better Auth session in headers/cookies
5. FastAPI backend verifies sessions by calling Better Auth API
6. User-specific data operations use the verified user_id for isolation

## Authentication Responsibilities
- **Better Auth**: Handle all authentication flows (registration, login, OAuth, password reset)
- **Frontend**: Use Better Auth client for UI flows and forward session to backend
- **Backend**: Verify sessions via Better Auth API, never implement auth endpoints

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New User Registration with Email/Password (Priority: P1)

A new user wants to create an account using their email address and password to access the AI Todo Chatbot. The user provides their email address and creates a secure password, then verifies their account through email confirmation.

**Why this priority**: This is the foundational user acquisition flow that enables all other functionality. Without this core registration capability, users cannot access the AI Todo Chatbot service.

**Independent Test**: Can be fully tested by registering a new user with email/password via Better Auth and verifying the account creation process works end-to-end, delivering immediate access to the todo management features.

**Acceptance Scenarios**:

1. **Given** a new user with valid email address, **When** they submit email and password on registration form via Better Auth, **Then** a new account is created and verification email is sent by Better Auth
2. **Given** a user who received verification email, **When** they click the verification link, **Then** their account is activated by Better Auth and they can log in

---

### User Story 2 - User Login with Email/Password (Priority: P1)

An existing user wants to access their AI Todo Chatbot account using their email and password credentials. The user enters their email and password to authenticate and gain access to their personalized todo data.

**Why this priority**: This is the primary authentication method that enables existing users to access their data and continue using the service.

**Independent Test**: Can be fully tested by logging in with valid credentials via Better Auth and verifying access to user-specific data is granted, delivering immediate value of account access.

**Acceptance Scenarios**:

1. **Given** a verified user account exists in Better Auth, **When** user enters correct email and password via Better Auth, **Then** they are authenticated and granted access to their data
2. **Given** user enters incorrect credentials, **When** they attempt to log in via Better Auth, **Then** authentication fails with appropriate error message

---

### User Story 3 - User Login with Google OAuth (Priority: P2)

A user wants to sign in using their Google account instead of creating a separate email/password account. The user clicks "Sign in with Google" and authenticates through Google's OAuth flow.

**Why this priority**: This provides a convenient alternative authentication method that reduces friction for users who prefer social login and already have Google accounts.

**Independent Test**: Can be fully tested by completing the Google OAuth flow via Better Auth and verifying the user is authenticated and granted access, delivering value of frictionless login.

**Acceptance Scenarios**:

1. **Given** user clicks "Sign in with Google" via Better Auth, **When** they complete Google OAuth flow, **Then** they are authenticated by Better Auth and granted access to their todo data
2. **Given** user has previously logged in with Google via Better Auth, **When** they return to the app, **Then** they can log in again using the same Google account

---

### User Story 4 - Password Reset (Priority: P2)

A user who has forgotten their password wants to reset it using their registered email address. The user provides their email address to initiate the password reset flow, receives an email with a secure reset link, and can set a new password through that link.

**Why this priority**: This provides account recovery functionality for users who cannot access their accounts due to forgotten passwords, improving user experience and reducing support requests.

**Independent Test**: Can be fully tested by initiating password reset for a registered user via Better Auth, receiving the reset email, clicking the reset link, and setting a new password, delivering account recovery functionality.

**Acceptance Scenarios**:

1. **Given** user has registered account with valid email in Better Auth, **When** they initiate password reset with their email via Better Auth, **Then** a secure reset token is generated and sent to their email by Better Auth
2. **Given** user receives password reset email from Better Auth, **When** they click the reset link and enter new password, **Then** their password is updated by Better Auth and they can log in with the new password

---

## Security Requirements

### Session Management
- All sessions must be verified via Better Auth API, never manually decoded
- Backend must not implement JWT verification logic
- Session tokens must be forwarded from frontend to backend APIs
- Session expiration must be handled by Better Auth, not custom logic

### User Data Isolation
- All API endpoints must validate user_id from Better Auth session verification
- Users can only access their own data based on verified user_id
- MCP tools must receive authenticated user context from verified session
- Database queries must be scoped by verified user_id

### Token Forwarding
- Frontend must extract Better Auth session and forward to backend APIs
- Backend must verify sessions via Better Auth API calls, not JWT decoding
- No user_id should be manually passed from frontend to backend
- Authentication state must flow through Better Auth verification only