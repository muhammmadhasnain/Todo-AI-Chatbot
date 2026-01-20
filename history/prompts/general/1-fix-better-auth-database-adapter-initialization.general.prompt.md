---
id: 1
title: Fix Better Auth database adapter initialization
stage: general
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-better-auth
user: Claude
command: general
labels:
  - authentication
  - better-auth
  - database
  - neon
  - postgresql
  - fix
links:
  - spec: null
  - ticket: null
  - adr: null
  - pr: null
files:
  - C:\Users\Hasnain\Desktop\todo agent app\frontend\lib\auth.config.ts
tests:
  - C:\Users\Hasnain\Desktop\todo agent app\frontend\lib\auth.config.ts
---

## Prompt

The frontend application is showing a 'Failed to initialize database adapter' error from Better Auth. This is causing 500 errors on auth endpoints like /api/auth/get-session and /api/auth/sign-up/social. Please investigate the issue and provide a solution to fix the database adapter initialization in the Better Auth configuration.

## Response

Fixed the Better Auth database adapter initialization issue by properly configuring the PostgreSQL/Neon database connection. The issue was in the `frontend/lib/auth.config.ts` file where the database configuration was incorrectly set up.

### Changes Made:

1. **Updated the database configuration** in `frontend/lib/auth.config.ts`:
   - Replaced the incorrect generic database setup with a proper Neon serverless adapter
   - Used the `@neondatabase/serverless` driver with Drizzle ORM
   - Configured the Drizzle adapter with PostgreSQL provider

2. **Installed required dependencies**:
   - `@neondatabase/serverless` for Neon serverless connections
   - `drizzle-orm` for database operations
   - Updated the configuration to use the Neon serverless adapter

### Technical Details:

The original configuration was trying to determine the provider based on URL format, but Better Auth requires specific database adapters. The fix implements:
- A proper Neon serverless client connection
- Drizzle ORM integration
- PostgreSQL provider specification for Better Auth

### Verification:

- Started the frontend server successfully
- Tested the `/api/auth/get-session` endpoint which now returns 200 status instead of 500
- The database adapter is now properly initialized without errors

The authentication endpoints should now work correctly without the "Failed to initialize database adapter" error.

## Outcome

Successfully resolved the Better Auth database adapter initialization issue by properly configuring the database connection with the Neon serverless adapter. The authentication endpoints are now working correctly.