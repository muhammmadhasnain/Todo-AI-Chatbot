import { describe, it, expect, vi } from 'vitest';
import { withRetry, createMCPToolCallWithRetry, defaultRetryConfig, RetryError } from './retryUtils';

describe('retryUtils', () => {
  describe('withRetry', () => {
    it('executes operation successfully on first try', async () => {
      const operation = vi.fn().mockResolvedValue('success');
      const result = await withRetry(operation);

      expect(operation).toHaveBeenCalledTimes(1);
      expect(result).toBe('success');
    });

    it('retries operation on failure up to maxRetries', async () => {
      const operation = vi.fn()
        .mockRejectedValueOnce(new Error('First try failed'))
        .mockRejectedValueOnce(new Error('Second try failed'))
        .mockResolvedValue('Third try success');

      const config = {
        ...defaultRetryConfig,
        maxRetries: 2
      };

      const result = await withRetry(operation, config);

      expect(operation).toHaveBeenCalledTimes(3);
      expect(result).toBe('Third try success');
    });

    it('fails after maxRetries are exceeded', async () => {
      const operation = vi.fn().mockRejectedValue(new Error('Always fails'));

      const config = {
        ...defaultRetryConfig,
        maxRetries: 1
      };

      await expect(withRetry(operation, config)).rejects.toThrow(RetryError);
      expect(operation).toHaveBeenCalledTimes(2); // Initial + 1 retry
    });

    it('does not retry on non-retryable errors', async () => {
      const operation = vi.fn().mockRejectedValue(new Error('Non-retryable error'));

      const config = {
        ...defaultRetryConfig,
        retryableErrors: ['SOME_OTHER_ERROR']
      };

      await expect(withRetry(operation, config)).rejects.toThrow('Non-retryable error');
      expect(operation).toHaveBeenCalledTimes(1);
    });

    it('retries on retryable errors', async () => {
      const operation = vi.fn()
        .mockRejectedValueOnce(new Error('Retryable error'))
        .mockResolvedValue('Success after retry');

      const config = {
        ...defaultRetryConfig,
        retryableErrors: ['Retryable error']
      };

      const result = await withRetry(operation, config);

      expect(operation).toHaveBeenCalledTimes(2);
      expect(result).toBe('Success after retry');
    });
  });

  describe('createMCPToolCallWithRetry', () => {
    it('wraps MCP tool call with retry logic', async () => {
      const mockCallMCPTool = vi.fn().mockResolvedValue({ result: 'success' });
      const callWithRetry = createMCPToolCallWithRetry(mockCallMCPTool);

      const result = await callWithRetry('test-tool', { param: 'value' });

      expect(mockCallMCPTool).toHaveBeenCalledWith('test-tool', { param: 'value' });
      expect(result).toEqual({ result: 'success' });
    });

    it('handles errors from MCP tool call', async () => {
      const mockCallMCPTool = vi.fn().mockRejectedValue(new Error('Tool error'));
      const callWithRetry = createMCPToolCallWithRetry(mockCallMCPTool);

      const result = await callWithRetry('test-tool', { param: 'value' });

      expect(result).toEqual({
        error: {
          code: 'UNKNOWN_ERROR',
          message: 'Tool error',
          details: expect.any(Error)
        }
      });
    });

    it('handles MCP errors from retry', async () => {
      const mockCallMCPTool = vi.fn()
        .mockRejectedValueOnce(new Error('First attempt failed'))
        .mockResolvedValue({ result: 'success' });

      const callMCPToolWithRetry = vi.fn().mockImplementation(() => withRetry(mockCallMCPTool));
      const callWithRetry = createMCPToolCallWithRetry(callMCPToolWithRetry, {
        maxRetries: 1,
        baseDelay: 1,
        maxDelay: 10,
        backoffMultiplier: 1
      });

      const result = await callWithRetry('test-tool', { param: 'value' });

      expect(result).toEqual({ result: 'success' });
    });
  });

  describe('defaultRetryConfig', () => {
    it('has expected default values', () => {
      expect(defaultRetryConfig).toEqual({
        maxRetries: 3,
        baseDelay: 1000,
        maxDelay: 10000,
        backoffMultiplier: 2,
        retryableErrors: ['MCP_ERROR', 'NETWORK_ERROR', 'TIMEOUT_ERROR', '502', '503', '504']
      });
    });
  });
});