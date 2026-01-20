'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from '../../lib/auth-client';

export default function VerifyEmail() {
  const [status, setStatus] = useState<'idle' | 'checking' | 'verified' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const router = useRouter();
  const { data: session, isPending: isLoading } = useSession();

  useEffect(() => {
    // Check if the user is already logged in and if their email is verified
    if (!isLoading && session) {
      if (session.data?.user?.emailVerified) {
        setStatus('verified');
        setMessage('Your email is already verified!');
        // Redirect to dashboard after a short delay
        const timer = setTimeout(() => {
          router.push('/dashboard');
        }, 2000);
        return () => clearTimeout(timer);
      } else {
        setStatus('checking');
        setMessage('Please check your email for the verification link.');
      }
    } else if (!isLoading && !session) {
      // If not logged in, redirect to login
      router.push('/login');
    }
  }, [session, isLoading, router]);

  const handleResendVerification = async () => {
    try {
      // In a real implementation, this would trigger a resend of the verification email
      // via the Better Auth API
      setStatus('checking');
      setMessage('Verification email resent. Please check your inbox.');
    } catch (err) {
      setStatus('error');
      setMessage('Failed to resend verification email. Please try again.');
    }
  };

  return (
    <div className="w-full max-w-md p-8 space-y-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
      <div>
        <h2 className="text-2xl font-bold text-center text-gray-900 dark:text-white">
          Verify Your Email
        </h2>
      </div>

      <div className="text-center">
        {status === 'checking' && (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">{message}</p>
          </div>
        )}

        {status === 'verified' && (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <p className="text-green-600 dark:text-green-400">{message}</p>
          </div>
        )}

        {status === 'error' && (
          <div className="p-3 text-red-700 bg-red-100 rounded-md dark:bg-red-900/30 dark:text-red-200">
            {message}
          </div>
        )}

        {status === 'idle' && !isLoading && (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 border-4 border-gray-300 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">Checking verification status...</p>
          </div>
        )}
      </div>

      {status === 'checking' && (
        <div className="text-center mt-4">
          <button
            onClick={handleResendVerification}
            className="text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300"
          >
            Resend verification email
          </button>
        </div>
      )}

      <div className="text-sm text-center text-gray-600 dark:text-gray-400 mt-8">
        <p>Didn't receive the email? Check your spam folder.</p>
      </div>
    </div>
  );
}