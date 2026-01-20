export interface RetryConfig {
  maxRetries: number;
  baseDelay: number; // in milliseconds
  maxDelay: number; // in milliseconds
  backoffMultiplier: number;
  retryableErrors?: string[]; // specific error codes that should be retried
}

export const defaultRetryConfig: RetryConfig = {
  maxRetries: 3,
  baseDelay: 1000, // 1 second
  maxDelay: 10000, // 10 seconds
  backoffMultiplier: 2,
  retryableErrors: ['MCP_ERROR', 'NETWORK_ERROR', 'TIMEOUT_ERROR', '502', '503', '504']
};

export class RetryError extends Error {
  constructor(message: string, public readonly originalError: Error, public readonly attempts: number) {
    super(message);
    this.name = 'RetryError';
  }
}

export const withRetry = async <T>(
  operation: () => Promise<T>,
  config: RetryConfig = defaultRetryConfig
): Promise<T> => {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Check if this error should be retried
      if (!shouldRetry(error, config)) {
        throw error;
      }

      // If this was the last attempt, throw the error
      if (attempt === config.maxRetries) {
        break;
      }

      // Calculate delay with exponential backoff
      const delay = Math.min(
        config.baseDelay * Math.pow(config.backoffMultiplier, attempt),
        config.maxDelay
      );

      // Wait before retrying
      await sleep(delay);
    }
  }

  throw new RetryError(
    `Operation failed after ${config.maxRetries + 1} attempts`,
    lastError!,
    config.maxRetries + 1
  );
};

const shouldRetry = (error: unknown, config: RetryConfig): boolean => {
  if (!config.retryableErrors) {
    return true; // Retry all errors if no specific errors are defined
  }

  if (error instanceof Error) {
    // Check if error code matches retryable errors
    if (config.retryableErrors.includes(error.name)) {
      return true;
    }

    // Check if error message contains retryable error codes
    return config.retryableErrors.some(retryableError =>
      error.message.includes(retryableError) || error.name.includes(retryableError)
    );
  }

  return true; // Retry unknown errors
};

const sleep = (ms: number): Promise<void> => new Promise(resolve => setTimeout(resolve, ms));

// Enhanced MCP tool call with retry logic
export interface MCPToolCallWithRetry {
  <T = any>(toolName: string, params: any, retryConfig?: RetryConfig): Promise<{ result?: T; error?: { code: string; message: string; details?: any } }>;
}

export const createMCPToolCallWithRetry = (
  callMCPTool: (toolName: string, params: any) => Promise<any>,
  defaultRetryConfig?: RetryConfig
): MCPToolCallWithRetry => {
  return async <T = any>(
    toolName: string,
    params: any,
    retryConfig: RetryConfig = defaultRetryConfig || defaultRetryConfig
  ) => {
    try {
      const result = await withRetry(() => callMCPTool(toolName, params), retryConfig);
      return { result };
    } catch (error) {
      if (error instanceof RetryError) {
        return {
          error: {
            code: 'RETRY_ERROR',
            message: error.message,
            details: {
              originalError: error.originalError,
              attempts: error.attempts
            }
          }
        };
      }

      return {
        error: {
          code: 'UNKNOWN_ERROR',
          message: error instanceof Error ? error.message : String(error),
          details: error
        }
      };
    }
  };
};