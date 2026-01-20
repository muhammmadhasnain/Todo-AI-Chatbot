import { auth } from '@/lib/auth.config';
import { toNextJsHandler } from 'better-auth/next-js';

// Create handlers for Better Auth endpoints
export const { GET, POST } = toNextJsHandler(auth);

// Configure runtime for server-side operations
export const runtime = 'nodejs';

// Add revalidation configuration to ensure endpoints are fresh
export const dynamic = 'force-dynamic';
