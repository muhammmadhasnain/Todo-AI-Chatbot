import React from 'react';
import { ChatMessage } from './ChatKit';
import { useTheme } from '../../context/ThemeContext';

interface MessageItemProps {
  message: ChatMessage;
}

const MessageItemComponent: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const { theme } = useTheme();

  return (
    <div
      className={`message-item ${isUser ? 'user-message' : 'assistant-message'}`}
      style={{
        marginBottom: theme.spacing,
        fontFamily: theme.fontFamily
      }}
      role="listitem"
      aria-label={`Message from ${isUser ? 'user' : 'assistant'}`}
    >
      <div
        className="message-content"
        style={{
          backgroundColor: isUser ? theme.primaryColor : theme.inputBackgroundColor,
          color: isUser ? 'white' : theme.textColor,
          padding: '0.5rem 1rem',
          borderRadius: theme.borderRadius,
          maxWidth: '85%',
          alignSelf: isUser ? 'flex-end' : 'flex-start',
          wordWrap: 'break-word'
        }}
        aria-label="Message content"
      >
        {message.content}
      </div>
      <div
        className="message-meta"
        style={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          fontSize: '0.75rem',
          color: theme.textColor + '80', // 50% opacity
          marginTop: '0.25rem',
          gap: '0.5rem'
        }}
        aria-label="Message metadata"
      >
        <span className="message-timestamp" aria-label="Timestamp">
          {typeof message.timestamp === 'string' ? new Date(message.timestamp).toLocaleTimeString() : message.timestamp.toLocaleTimeString()}
        </span>
        <span className="message-status" aria-label="Delivery status">
          {message.status}
        </span>
      </div>
    </div>
  );
};

export const MessageItem = React.memo(MessageItemComponent);

export default MessageItem;