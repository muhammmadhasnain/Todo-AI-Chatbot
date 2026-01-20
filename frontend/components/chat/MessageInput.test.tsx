import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MessageInput } from './MessageInput';
import { ThemeProvider } from '../../context/ThemeContext';

// Mock the useMCPTools hook
vi.mock('../../hooks/useMCPTools', () => ({
  useMCPTools: () => ({
    callMCPToolWithRetry: vi.fn().mockResolvedValue({ result: { messageId: '123', status: 'sent' } }),
    isLoading: false
  })
}));

// Mock the useTheme hook
vi.mock('../../context/ThemeContext', async () => {
  const actual = await vi.importActual('../../context/ThemeContext');
  return {
    ...actual,
    useTheme: () => ({
      theme: {
        primaryColor: '#8B5CF6',
        secondaryColor: '#EC4899',
        backgroundColor: '#FFFFFF',
        textColor: '#374151',
        inputBackgroundColor: '#F9FAFB',
        inputTextColor: '#1F2937',
        borderRadius: '0.5rem',
        spacing: '1rem',
        fontFamily: 'system-ui'
      }
    })
  };
});

// Wrap the component with ThemeProvider for theme context
const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>
      {ui}
    </ThemeProvider>
  );
};

describe('MessageInput', () => {
  const defaultProps = {
    sessionId: 'test-session',
    userId: 'test-user',
    onSendMessage: vi.fn(),
    placeholder: 'Type your message...'
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders correctly with placeholder', () => {
    renderWithTheme(<MessageInput {...defaultProps} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    expect(textarea).toBeInTheDocument();
    expect(textarea).toHaveAttribute('aria-label', 'Type your message');
  });

  it('allows typing in the input field', () => {
    renderWithTheme(<MessageInput {...defaultProps} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(textarea, { target: { value: 'Hello, world!' } });

    expect(textarea).toHaveValue('Hello, world!');
  });

  it('submits message when Enter is pressed', async () => {
    const mockOnSendMessage = vi.fn();
    renderWithTheme(
      <MessageInput
        {...defaultProps}
        onSendMessage={mockOnSendMessage}
      />
    );

    const textarea = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(textarea, { target: { value: 'Test message' } });
    fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: false });

    await waitFor(() => {
      expect(mockOnSendMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          content: 'Test message'
        })
      );
    });
  });

  it('allows new line when Shift+Enter is pressed', () => {
    renderWithTheme(<MessageInput {...defaultProps} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(textarea, { target: { value: 'Line 1' } });
    fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: true });

    expect(textarea).toHaveValue('Line 1\n');
  });

  it('clears input when Escape is pressed with content', () => {
    renderWithTheme(<MessageInput {...defaultProps} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(textarea, { target: { value: 'Some text' } });
    fireEvent.keyDown(textarea, { key: 'Escape' });

    expect(textarea).toHaveValue('');
  });

  it('disables input when disabled prop is true', () => {
    renderWithTheme(<MessageInput {...defaultProps} disabled={true} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    expect(textarea).toBeDisabled();
  });

  it('shows error message when message sending fails', async () => {
    // Mock a failed message send
    const mockCallMCPToolWithRetry = vi.fn().mockResolvedValue({
      error: { message: 'Failed to send message' }
    });

    vi.mocked(require('../../hooks/useMCPTools').useMCPTools).mockReturnValue({
      callMCPToolWithRetry: mockCallMCPToolWithRetry,
      isLoading: false
    } as any);

    renderWithTheme(<MessageInput {...defaultProps} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(textarea, { target: { value: 'Test message' } });
    fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: false });

    await waitFor(() => {
      expect(screen.getByText('Failed to send message')).toBeInTheDocument();
    });
  });
});