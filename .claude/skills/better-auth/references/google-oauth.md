# Google OAuth Setup Guide

## Creating Google OAuth Credentials

To use Google login with Better Auth, you need to create OAuth credentials in the Google Cloud Console:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (or Google People API)
4. Go to "Credentials" in the left sidebar
5. Click "Create Credentials" > "OAuth 2.0 Client IDs"
6. For Application type, select "Web application"
7. Add your authorized redirect URIs:
   - For development: `http://localhost:3000/api/auth/callback/google`
   - For production: `https://yourdomain.com/api/auth/callback/google`
8. Download the credentials file or note the Client ID and Client Secret

## Required Environment Variables

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Google OAuth Configuration in Better Auth

```typescript
import { betterAuth } from "better-auth";
import { google } from "better-auth/oauth-providers";

export const auth = betterAuth({
  // ... other configuration
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      scope: ["email", "profile"], // Additional scopes if needed
    },
  },
});
```

## Additional Google OAuth Options

The Google OAuth provider supports additional configuration options:

- `scope`: Array of OAuth scopes to request (default: ["email", "profile"])
- `authorizationParams`: Additional parameters to send with the authorization request
- `clientConfig`: Custom OAuth client configuration if needed

## Troubleshooting Common Issues

1. **Redirect URI mismatch**: Ensure the redirect URI in Google Cloud Console matches the one Better Auth generates
2. **Domain verification**: For production, you may need to verify your domain in Google Cloud Console
3. **API enablement**: Make sure you've enabled the Google People API in your project
4. **Credentials**: Ensure your Client ID and Secret are correctly set in environment variables

## Security Considerations

- Never expose your Client Secret in client-side code
- Use HTTPS in production
- Regularly rotate your OAuth credentials
- Monitor your Google Cloud Console for unauthorized access