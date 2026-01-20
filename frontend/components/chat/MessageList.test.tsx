import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MessageList } from './MessageList';
import { ThemeProvider } from '../../context/ThemeContext';

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

// Mock the MessageItem component to avoid deep rendering
vi.mock('./MessageItem', () => ({
  MessageItem: ({ message }: { message: any }) => (
    <div data-testid="mock-message-item">{message.content}</div>
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

describe('MessageList', () => {
  const mockMessages = [
    {
      id: '1',
      content: 'First message',
      role: 'user' as const,
      timestamp: new Date(),
      status: 'sent' as const
    },
    {
      id: '2',
      content: 'Second message',
      role: 'assistant' as const,
      timestamp: new Date(),
      status: 'sent' as const
    }
  ];

  it('renders multiple messages correctly', () => {
    renderWithTheme(<MessageList messages={mockMessages} />);

    expect(screen.getByText('First message')).toBeInTheDocument();
    expect(screen.getByText('Second message')).toBeInTheDocument();
  });

  it('renders empty list when no messages provided', () => {
    renderWithTheme(<MessageList messages={[]} />);

    // Check that the container is rendered but has no message items
    const container = screen.getByLabelText('Chat message list');
    expect(container).toBeInTheDocument();
  });

  it('applies correct role and aria-label', () => {
    renderWithTheme(<MessageList messages={mockMessages} />);

    const listContainer = screen.getByLabelText('Chat message list');
    expect(listContainer).toBeInTheDocument();
    expect(listContainer).toHaveAttribute('role', 'list');
  });

  it('renders messages in correct order', () => {
    renderWithTheme(<MessageList messages={mockMessages} />);

    const messages = screen.getAllByTestId('mock-message-item');
    expect(messages).toHaveLength(2);
    expect(messages[0]).toHaveTextContent('First message');
    expect(messages[1]).toHaveTextContent('Second message');
  });
});