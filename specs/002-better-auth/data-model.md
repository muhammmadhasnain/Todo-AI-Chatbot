# Data Model: Better Auth for AI Todo Chatbot (CORRECTED)

## Entities

### User
- **user_id**: string (primary identifier from Better Auth system)
- **email**: string (unique, required)
- **name**: string (optional, from OAuth profile via Better Auth)
- **avatar_url**: string (optional, from OAuth profile via Better Auth)
- **email_verified**: boolean (default: false, managed by Better Auth)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-generated)
- **last_login_at**: datetime (optional, updated on each login)

**Relationships**:
- One User to Many Tasks (user_id foreign key in Task model)
- One User to Many Conversations (user_id foreign key in Conversation model)
- One User to Many Messages (user_id foreign key in Message model)

**Validation Rules**:
- email must be valid email format
- email must be unique across all users
- user_id must be unique and non-empty
- email_verified can only be set by Better Auth email verification flow

### OAuthProvider
- **provider_id**: string (e.g., "google")
- **provider_user_id**: string (user ID from OAuth provider via Better Auth)
- **user_id**: string (foreign key to User)
- **email**: string (email from OAuth provider via Better Auth)
- **profile_data**: JSON (optional, name, avatar, etc. from Better Auth)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-generated)

**Relationships**:
- One User to Many OAuthProviders (user_id foreign key)
- One OAuthProvider to One User (user_id foreign key)

**Validation Rules**:
- provider_id + provider_user_id combination must be unique
- user_id must reference existing User
- email must match User.email

## State Transitions

### User Registration Flow
1. **Unregistered** → **Pending Verification** (email/password registration via Better Auth)
   - User provides email and password via Better Auth client
   - Account created by Better Auth with email_verified = false
   - Verification email sent by Better Auth
2. **Pending Verification** → **Active** (email verification via Better Auth)
   - User clicks verification link
   - email_verified set to true by Better Auth
   - Account becomes active

### Authentication Flow
1. **Unauthenticated** → **Authenticated** (successful login via Better Auth)
   - User provides valid credentials or completes OAuth flow via Better Auth
   - Session tokens issued by Better Auth
   - Session state managed by Better Auth client in frontend
2. **Authenticated** → **Unauthenticated** (logout or token expiration)
   - User initiates logout via Better Auth client or tokens expire
   - Session invalidated by Better Auth
   - Session state cleared by Better Auth client

### OAuth Linking Flow
1. **Email/Password Only** → **Dual Method** (OAuth linking via Better Auth)
   - User logs in with OAuth that matches existing email via Better Auth
   - OAuth provider linked to existing account by Better Auth
   - User can now log in with either method via Better Auth

## Backend Session Verification Context

### Session Verification Request (Internal to Better Auth API)
- **session_token**: string (session token from Authorization header)
- **user_id**: string (extracted from verified session)
- **email**: string (from verified session)
- **is_valid**: boolean (verification result)
- **expires_at**: datetime (session expiration from Better Auth)

**Purpose**: Backend calls Better Auth API to verify session tokens and extract user context for protected endpoints. Backend does not store or manage authentication sessions directly.