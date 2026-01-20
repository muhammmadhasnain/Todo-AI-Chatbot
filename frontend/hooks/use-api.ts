import { useState, useEffect } from 'react';
import { authClient } from '../lib/auth-client';

// Define the shape of our API response
interface ApiResponse<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

// Custom hook for making authenticated API calls
export const useApi = <T,>(
  url: string,
  options?: RequestInit,
  deps: React.DependencyList = []
): ApiResponse<T> => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get the current session to access the token
      const session = await authClient.getSession();

      // Prepare headers with the session token
      const headers = {
        'Content-Type': 'application/json',
        ...options?.headers,
      };

      // Add authorization header if we have a valid session
      if (session?.session?.access_token) {
        headers['Authorization'] = `Bearer ${session.session.access_token}`;
      }

      // Make the API call
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  const refetch = () => {
    fetchData();
  };

  return { data, loading, error, refetch };
};

// Specific hooks for common API operations
export const useGet = <T,>(url: string, deps: React.DependencyList = []): ApiResponse<T> => {
  return useApi<T>(url, { method: 'GET' }, deps);
};

export const usePost = <T,>(url: string, body: any) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const executePost = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get the current session to access the token
      const session = await authClient.getSession();

      // Prepare headers with the session token
      const headers = {
        'Content-Type': 'application/json',
      };

      // Add authorization header if we have a valid session
      if (session?.session?.access_token) {
        headers['Authorization'] = `Bearer ${session.session.access_token}`;
      }

      // Make the POST request
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(`POST request failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, executePost };
};