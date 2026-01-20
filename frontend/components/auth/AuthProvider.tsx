'use client';

import { createContext, useContext, ReactNode } from 'react';
import { authClient, useSession } from '../../lib/auth-client';

interface AuthContextType {
  session: any;
  isLoading: boolean;
  signIn: any;
  signOut: any;
  signUp: any;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export default function AuthProvider({ children }: AuthProviderProps) {
  const { data: session, isPending: isLoading } = useSession();

  const signIn = authClient.signIn;
  const signOut = authClient.signOut;
  const signUp = authClient.signUp;

  return (
    <AuthContext.Provider value={{ session, isLoading, signIn, signOut, signUp }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};