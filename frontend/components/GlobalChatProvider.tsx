'use client';

import { useSession } from '../lib/auth-client';
import { FloatingChatButton } from './FloatingChatButton';

export default function GlobalChatProvider() {
  const { data: session, isPending } = useSession();

  // Only show the floating chat button if the user is authenticated
  if (isPending || !session?.user) {
    return null;
  }

  return (
    <FloatingChatButton
      userId={session.user.id}
      authToken={session.session?.token}
    />
  );
}