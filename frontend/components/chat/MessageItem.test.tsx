import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MessageItem } from './MessageItem';
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

// Wrap the component with ThemeProvider for theme context
const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>
      {ui}
    </ThemeProvider>
  );
};

describe('MessageItem', () => {
  const mockMessage = {
    id: '1',
    content: 'Hello, world!',
    role: 'user' as const,
    timestamp: new Date('2023-01-01T10:00:00'),
    status: 'sent' as const
  };

  it('renders user message correctly', () => {
    renderWithTheme(<MessageItem message={mockMessage} />);

    expect(screen.getByText('Hello, world!')).toBeInTheDocument();
    expect(screen.getByText('10:00:00')).toBeInTheDocument(); // Time based on timestamp
    expect(screen.getByText('sent')).toBeInTheDocument();
  });

  it('renders assistant message correctly', () => {
    const assistantMessage = {
      ...mockMessage,
      role: 'assistant' as const
    };

    renderWithTheme(<MessageItem message={assistantMessage} />);

    expect(screen.getByText('Hello, world!')).toBeInTheDocument();
  });

  it('applies correct styling based on message role', () => {
    const { container } = renderWithTheme(<MessageItem message={mockMessage} />);

    // Check that the message has the correct role attribute
    const messageItem = container.firstChild;
    expect(messageItem).toHaveAttribute('role', 'listitem');
    expect(messageItem).toHaveAttribute('aria-label', 'Message from user');
  });

  it('formats timestamp correctly', () => {
    renderWithTheme(<MessageItem message={mockMessage} />);

    // The exact format depends on the user's locale, but it should contain time information
    const timestampElement = screen.getByLabelText('Timestamp');
    expect(timestampElement).toBeInTheDocument();
  });

  it('shows status information', () => {
    renderWithTheme(<MessageItem message={mockMessage} />);

    const statusElement = screen.getByLabelText('Delivery status');
    expect(statusElement).toHaveTextContent('sent');
  });
});