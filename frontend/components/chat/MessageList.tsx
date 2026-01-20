import React from 'react';
import { ChatMessage } from './ChatKit';
import { useTheme } from '../../context/ThemeContext';
import { MessageItem } from './MessageItem';

interface MessageListProps {
  messages: ChatMessage[];
}

const MessageListComponent: React.FC<MessageListProps> = ({ messages }) => {
  const { theme } = useTheme();

  return (
    <div
      className="message-list-container"
      style={{
        fontFamily: theme.fontFamily
      }}
      role="list"
      aria-label="Chat message list"
    >
      {messages.map((message) => (
        <MessageItem
          key={message.id}
          message={message}
        />
      ))}
    </div>
  );
};

export const MessageList = React.memo(MessageListComponent);

export default MessageList;