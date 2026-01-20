---
name: better-auth
description: Comprehensive authentication setup using Better Auth with Email & Password and Google login. Use when implementing authentication for web applications requiring secure user registration, login, social authentication, and session management.
---

# Better Auth Skill

This skill provides comprehensive authentication setup using Better Auth with both Email & Password and Google login capabilities.

## When to Use This Skill

Use this skill when you need to:
1. Set up authentication for a web application
2. Implement both email/password and social (Google) authentication
3. Configure secure user registration and login flows
4. Manage user sessions and authentication state

## Implementation

### Server-Side Configuration

Create an authentication configuration file with both email/password and Google authentication:

```typescript
import { betterAuth } from "better-auth";
import { google } from "better-auth/oauth-providers";

export const auth = betterAuth({
  database: {
    provider: "sqlite", // or your preferred database
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true, // Recommended for security
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  // Additional configuration options
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
  secret: process.env.AUTH_SECRET!, // Required for production
});
```

### Client-Side Configuration

Create a client configuration to interact with the authentication server:

```typescript
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000", // Your app's base URL
  fetchOptions: {
    // Optional: Add any custom fetch options
  },
});
```

### Environment Variables

Add these environment variables to your project:

```
DATABASE_URL=your_database_url
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
AUTH_SECRET=your_auth_secret
NEXT_PUBLIC_BASE_URL=your_base_url
```

### Usage Examples

#### Email & Password Registration

```typescript
// Sign up with email and password
const result = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "User Name", // Optional
});

if (result.error) {
  console.error("Sign up error:", result.error.message);
} else {
  console.log("User signed up:", result.data);
}
```

#### Email & Password Login

```typescript
// Sign in with email and password
const result = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
});

if (result.error) {
  console.error("Sign in error:", result.error.message);
} else {
  console.log("User signed in:", result.data);
}
```

#### Google Login

```typescript
// Sign in with Google
await authClient.signIn.social({
  provider: "google",
  callbackURL: "/dashboard", // Where to redirect after successful login
  errorCallbackURL: "/login?error=google", // Where to redirect if error occurs
});
```

#### Getting Current User Session

```typescript
// Get current session
const session = await authClient.getSession();

if (session.data) {
  console.log("User is logged in:", session.data.user);
} else {
  console.log("No active session");
}
```

#### Logout

```typescript
// Sign out
await authClient.signOut();
```

### Next.js API Route Integration

For Next.js applications, create an API route to handle authentication:

```typescript
// pages/api/auth/[...auth].ts (for pages router)
// or
// app/api/auth/[...auth]/route.ts (for app router)

import { auth } from "../../../server/auth"; // Adjust path to your auth config

export const { GET, POST } = auth;
```

### React Component Example

Here's an example of how to use authentication in a React component:

```tsx
import { useState } from "react";
import { authClient } from "../lib/auth-client"; // Your client config

export default function AuthForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [isLogin, setIsLogin] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (isLogin) {
      // Sign in
      const result = await authClient.signIn.email({
        email,
        password,
      });

      if (result.error) {
        alert(`Login error: ${result.error.message}`);
      } else {
        // Redirect to dashboard or home page
        window.location.href = "/dashboard";
      }
    } else {
      // Sign up
      const result = await authClient.signUp.email({
        email,
        password,
        name,
      });

      if (result.error) {
        alert(`Signup error: ${result.error.message}`);
      } else {
        // Redirect to dashboard or home page
        window.location.href = "/dashboard";
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {!isLogin && (
        <div>
          <label htmlFor="name">Name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required={!isLogin}
          />
        </div>
      )}
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">
        {isLogin ? "Sign In" : "Sign Up"}
      </button>
      <button type="button" onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Need an account? Sign Up" : "Already have an account? Sign In"}
      </button>
      <button
        type="button"
        onClick={() => {
          authClient.signIn.social({
            provider: "google",
            callbackURL: "/dashboard",
          });
        }}
      >
        Sign in with Google
      </button>
    </form>
  );
}
```

## Security Best Practices

1. Always use HTTPS in production
2. Set strong password requirements
3. Enable email verification for new accounts
4. Use environment variables for sensitive configuration
5. Implement rate limiting to prevent abuse
6. Regularly rotate secrets and API keys

## Required Dependencies

Install these packages in your project:

```bash
npm install better-auth @better-auth/oauth-providers
```

For client-side usage:

```bash
npm install @better-auth/client
```