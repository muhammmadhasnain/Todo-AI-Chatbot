import React, { useState, useEffect, useRef } from 'react';
import { MessageItem } from './MessageItem';
import { ChatMessage } from './MessageList';
import { useTheme } from '../../context/ThemeContext';

interface VirtualMessageListProps {
  messages: ChatMessage[];
}

// Height of each message item in pixels (approximate)
const MESSAGE_ITEM_HEIGHT = 80;

export const VirtualMessageList: React.FC<VirtualMessageListProps> = ({ messages }) => {
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 10 });
  const containerRef = useRef<HTMLDivElement>(null);
  const { theme } = useTheme();

  // Calculate visible range based on scroll position
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const scrollTop = container.scrollTop;
      const containerHeight = container.clientHeight;

      // Calculate how many items are visible
      const itemsVisible = Math.ceil(containerHeight / MESSAGE_ITEM_HEIGHT);
      const startIndex = Math.floor(scrollTop / MESSAGE_ITEM_HEIGHT);
      const endIndex = Math.min(startIndex + itemsVisible + 5, messages.length); // Add buffer of 5 items

      setVisibleRange({
        start: Math.max(0, startIndex - 5), // Add buffer of 5 items before
        end: endIndex
      });
    };

    // Initial calculation
    handleScroll();

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [messages.length]);

  // Calculate total height for scroll container
  const totalHeight = messages.length * MESSAGE_ITEM_HEIGHT;

  // Calculate offset for the first visible item
  const offset = visibleRange.start * MESSAGE_ITEM_HEIGHT;

  // Get the messages to render in the visible range
  const messagesToRender = messages.slice(visibleRange.start, visibleRange.end);

  return (
    <div
      ref={containerRef}
      className="virtual-message-list"
      style={{
        height: '100%',
        overflowY: 'auto',
        position: 'relative',
        fontFamily: theme.fontFamily
      }}
      role="list"
      aria-label="Chat message list"
    >
      {/* Spacer div to maintain scroll height */}
      <div style={{ height: `${totalHeight}px`, position: 'relative' }}>
        {/* Rendered messages positioned absolutely */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            transform: `translateY(${offset}px)`,
          }}
        >
          {messagesToRender.map((message) => (
            <div key={message.id} style={{ height: `${MESSAGE_ITEM_HEIGHT}px` }}>
              <MessageItem message={message} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default VirtualMessageList;