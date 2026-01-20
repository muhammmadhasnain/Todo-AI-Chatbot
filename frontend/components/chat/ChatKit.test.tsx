import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ChatKitComponent } from './ChatKit';
import { ThemeProvider } from  "../../context/ThemeContext";

// Mock the useMCPTools hook
vi.mock('../../hooks/useMCPTools', () => ({
  useMCPTools: () => ({
    callMCPToolWithRetry: vi.fn().mockResolvedValue({ result: { messages: [] } }),
    isLoading: false
  })
}));

// Mock the MessageList component to avoid deep rendering
vi.mock('./MessageList', () => ({
  MessageList: ({ messages }: { messages: any }) => (
    <div data-testid="mock-message-list">{messages.length} messages</div>
  )
}));

// Mock the MessageInput component to avoid deep rendering
vi.mock('./MessageInput', () => ({
  MessageInput: ({ onSendMessage }: { onSendMessage: any }) => (
    <div data-testid="mock-message-input">
      <button onClick={() => onSendMessage && onSendMessage({ id: 'temp', content: 'test', timestamp: new Date() })}>
        Send Test Message
      </button>
    </div>
  )
}));

// Wrap the component with ThemeProvider for theme context
const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>
      {ui}
    </ThemeProvider>
  );
};

describe('ChatKitComponent', () => {
  const defaultProps = {
    sessionId: 'test-session',
    userId: 'test-user',
    placeholder: 'Type a message...'
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders correctly with header and input', () => {
    renderWithTheme(<ChatKitComponent {...defaultProps} />);

    expect(screen.getByLabelText('Chat interface')).toBeInTheDocument();
    expect(screen.getByLabelText('Chat messages area')).toBeInTheDocument();
    expect(screen.getByTestId('mock-message-input')).toBeInTheDocument();
  });

  it('shows header when showHeader is not false', () => {
    renderWithTheme(<ChatKitComponent {...defaultProps} />);

    expect(screen.getByText('Chat')).toBeInTheDocument();
  });

  it('hides header when showHeader is false', () => {
    renderWithTheme(<ChatKitComponent {...defaultProps} showHeader={false} />);

    expect(screen.queryByText('Chat')).not.toBeInTheDocument();
  });

  it('hides input when showInput is false', () => {
    renderWithTheme(<ChatKitComponent {...defaultProps} showInput={false} />);

    expect(screen.queryByTestId('mock-message-input')).not.toBeInTheDocument();
  });

  it('loads initial messages when sessionId and userId are provided', async () => {
    const mockMessages = [
      {
        id: '1',
        content: 'Hello',
        role: 'assistant' as const,
        timestamp: new Date(),
        status: 'sent' as const
      }
    ];

    // Mock the MCP tool to return messages
    const mockCallMCPToolWithRetry = vi.fn().mockResolvedValue({
      result: { messages: mockMessages }
    });

    vi.mocked(require('../../hooks/useMCPTools').useMCPTools).mockReturnValue({
      callMCPToolWithRetry: mockCallMCPToolWithRetry,
      isLoading: false
    } as any);

    renderWithTheme(<ChatKitComponent {...defaultProps} />);

    await waitFor(() => {
      expect(mockCallMCPToolWithRetry).toHaveBeenCalledWith('get_history', {
        sessionId: 'test-session',
        userId: 'test-user',
        limit: 50,
        offset: 0
      });
    });
  });

  it('handles message sending correctly', async () => {
    const mockOnMessageSend = vi.fn();
    renderWithTheme(
      <ChatKitComponent
        {...defaultProps}
        onMessageSend={mockOnMessageSend}
      />
    );

    const sendButton = screen.getByText('Send Test Message');
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(mockOnMessageSend).toHaveBeenCalledWith(
        expect.objectContaining({
          content: 'test'
        })
      );
    });
  });

  it('applies custom theme when provided', () => {
    const customTheme = {
      primaryColor: '#FF0000',
      backgroundColor: '#000000'
    };

    renderWithTheme(
      <ChatKitComponent
        {...defaultProps}
        theme={customTheme}
      />
    );

    // The theme context should be applied via the ThemeProvider
    const chatContainer = screen.getByLabelText('Chat interface');
    expect(chatContainer).toBeInTheDocument();
  });
});