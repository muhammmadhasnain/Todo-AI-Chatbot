# Email & Password Authentication Guide

## Configuration Options

Better Auth provides several options for email and password authentication:

```typescript
emailAndPassword: {
  enabled: true,                    // Enable email/password auth (default: false)
  requireEmailVerification: true,   // Require email verification (default: false)
  sendEmailVerificationOnSignUp: true, // Send verification email on sign up (default: true)
  sendEmailVerificationOnUpdate: true,  // Send verification on email update (default: false)
  password: {
    // Password requirements
    minLength: 8,                   // Minimum password length (default: 8)
    requireSpecialChar: true,       // Require special character (default: false)
    requireNumbers: true,           // Require numbers (default: false)
    requireUppercase: true,         // Require uppercase (default: false)
    requireLowercase: true,         // Require lowercase (default: false)
  },
  async getUserByEmail(email) {
    // Custom function to get user by email (optional)
  },
  async generateUserId() {
    // Custom function to generate user ID (optional)
  }
}
```

## Password Security Best Practices

1. **Password Requirements**:
   - Minimum 8 characters (recommended 12+)
   - Include uppercase, lowercase, numbers, and special characters
   - Avoid common passwords and patterns

2. **Rate Limiting**:
   - Implement rate limiting on sign in attempts
   - Consider account lockout after multiple failed attempts

3. **Secure Storage**:
   - Passwords are automatically hashed using bcrypt or scrypt
   - Never store plain text passwords

## Email Verification

When `requireEmailVerification` is enabled:

1. New users must verify their email before signing in
2. Verification emails are sent automatically on sign up
3. Users can request a new verification email if needed

```typescript
// Resend verification email
await authClient.emailVerification.sendVerificationEmail({
  email: "user@example.com"
});
```

## Session Management

Better Auth handles sessions automatically:

```typescript
// Session configuration
session: {
  expiresIn: 7 * 24 * 60 * 60,    // 7 days in seconds
  updateAge: 24 * 60 * 60,        // Update session every 24 hours
  rememberMe: {
    expiresIn: 30 * 24 * 60 * 60, // Remember me for 30 days
  },
}
```

## Common Operations

### Sign Up
```typescript
const result = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "User Name" // Optional
});
```

### Sign In
```typescript
const result = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
});
```

### Password Reset
```typescript
// Send password reset email
await authClient.passwordReset.sendResetLink({
  email: "user@example.com"
});

// Reset password with token
const result = await authClient.passwordReset.resetPassword({
  token: "reset-token",
  newPassword: "newSecurePassword123"
});
```

### Update Password
```typescript
// For authenticated users
const result = await authClient.updatePassword({
  newPassword: "newSecurePassword123",
  currentPassword: "currentPassword123"
});
```

## Error Handling

Common error responses:

- `EMAIL_NOT_FOUND`: Email doesn't exist
- `INVALID_PASSWORD`: Password is incorrect
- `EMAIL_NOT_VERIFIED`: Email verification required
- `USER_NOT_FOUND`: User doesn't exist
- `INVALID_EMAIL`: Invalid email format
- `EMAIL_ALREADY_EXISTS`: Email already in use

Example error handling:
```typescript
const result = await authClient.signIn.email({
  email: "user@example.com",
  password: "password"
});

if (result.error) {
  switch(result.error.code) {
    case "EMAIL_NOT_FOUND":
      console.error("Email not found");
      break;
    case "INVALID_PASSWORD":
      console.error("Invalid password");
      break;
    default:
      console.error("Sign in failed:", result.error.message);
  }
} else {
  console.log("Signed in successfully");
}
```

## Security Recommendations

1. Always use HTTPS in production
2. Implement proper password requirements
3. Enable email verification for sensitive applications
4. Use strong secrets for session encryption
5. Implement rate limiting to prevent brute force attacks
6. Regularly audit authentication logs
7. Consider implementing two-factor authentication for sensitive applications