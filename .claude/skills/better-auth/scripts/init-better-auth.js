#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Create the auth configuration files
function createAuthFiles() {
  // Create server auth config
  const serverAuthConfig = `import { betterAuth } from "better-auth";
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
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
  secret: process.env.AUTH_SECRET!, // Required for production
});
`;

  // Create client auth config
  const clientAuthConfig = `import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000", // Your app's base URL
});
`;

  // Create Next.js API route
  const apiRoute = `import { auth } from "../../../server/auth"; // Adjust path to your auth config

export const { GET, POST } = auth;
`;

  // Create .env.example
  const envExample = `DATABASE_URL=your_database_url
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
AUTH_SECRET=your_auth_secret
NEXT_PUBLIC_BASE_URL=http://localhost:3000
`;

  // Create sample React component
  const authComponent = `import { useState } from "react";
import { authClient } from "../lib/auth-client"; // Your client config

export default function AuthForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [isLogin, setIsLogin] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isLogin) {
      // Sign in
      const result = await authClient.signIn.email({
        email,
        password,
      });

      if (result.error) {
        alert(\`Login error: \${result.error.message}\`);
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
        alert(\`Signup error: \${result.error.message}\`);
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
`;

  // Write files to the current directory
  fs.writeFileSync(path.join(process.cwd(), 'server', 'auth.js'), serverAuthConfig);
  fs.writeFileSync(path.join(process.cwd(), 'client', 'auth.js'), clientAuthConfig);
  fs.writeFileSync(path.join(process.cwd(), 'pages', 'api', 'auth', '[...auth].js'), apiRoute);
  fs.writeFileSync(path.join(process.cwd(), '.env.example'), envExample);
  fs.writeFileSync(path.join(process.cwd(), 'components', 'AuthForm.js'), authComponent);

  console.log('Better Auth configuration files created successfully!');
  console.log('Remember to:');
  console.log('1. Install the required dependencies: npm install better-auth @better-auth/oauth-providers @better-auth/client');
  console.log('2. Set up your environment variables');
  console.log('3. Configure your database connection');
  console.log('4. Update import paths as needed for your project structure');
}

createAuthFiles();