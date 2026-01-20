import { useState } from 'react';
import { createMCPToolCallWithRetry, defaultRetryConfig, RetryConfig } from '../utils/retryUtils';

export interface MCPToolCall {
  tool: string;
  parameters: any;
}

export interface MCPResult {
  result?: any;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

export const useMCPTools = (defaultRetryConfigOverride?: RetryConfig) => {
  const [isLoading, setIsLoading] = useState(false);

  const callMCPTool = async (toolName: string, params: any): Promise<MCPResult> => {
    setIsLoading(true);
    try {
      // This would connect to your MCP server
      const response = await fetch('/api/mcp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify({
          tool: toolName,
          parameters: params
        })
      });

      const result = await response.json();
      return result;
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        console.error(`Error calling MCP tool ${toolName}:`, error);
      }
      return {
        error: {
          code: 'MCP_ERROR',
          message: `Error calling MCP tool ${toolName}: ${error}`,
          details: error
        }
      };
    } finally {
      setIsLoading(false);
    }
  };

  // Enhanced call with retry logic
  const callMCPToolWithRetry = createMCPToolCallWithRetry(
    callMCPTool,
    defaultRetryConfigOverride
  );

  return { callMCPTool, callMCPToolWithRetry, isLoading };
};

// Helper function to get auth token
const getAuthToken = (): string => {
  // Get token from context, local storage, or wherever it's stored
  return typeof window !== 'undefined' ? localStorage.getItem('authToken') || '' : '';
};