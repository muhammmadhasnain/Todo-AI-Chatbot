import React, { useState, useRef, KeyboardEvent, useCallback } from 'react';
import { useTheme } from '../../context/ThemeContext';

interface MessageInputProps {
  userId?: string;
  onSendMessage?: (message: { id: string; content: string; timestamp: Date }) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  userId,
  onSendMessage,
  disabled = false,
  placeholder = 'Type your message...'
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { theme } = useTheme();

  const adjustTextareaHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  }, []);

  const handleInput = useCallback(() => {
    adjustTextareaHeight();
  }, [adjustTextareaHeight]);

  const handleSubmit = useCallback(async () => {
    if (!inputValue.trim() || !userId || isSending || disabled) {
      return;
    }

    setIsSending(true);
    setErrorMessage(null);

    try {
      // Create a new message object to return
      const newMessage = {
        id: `temp-${Date.now()}`,
        content: inputValue.trim(),
        timestamp: new Date()
      };

      // Clear input and reset height
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }

      // Call the callback if provided - this will trigger the API call in ChatKit
      if (onSendMessage) {
        onSendMessage(newMessage);
      }
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to prepare message:', error);
      }
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error occurred');
    } finally {
      setIsSending(false);
    }
  }, [inputValue, userId, isSending, disabled, onSendMessage]);

  const handleKeyDown = useCallback((e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }

    // Allow Shift+Enter for new line
    if (e.key === 'Enter' && e.shiftKey) {
      // Allow the default behavior for new line
      return;
    }

    // Clear input on Escape if it has content
    if (e.key === 'Escape' && inputValue.trim()) {
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  }, [handleSubmit, inputValue]);

  const handleSendClick = useCallback(() => {
    handleSubmit();
  }, [handleSubmit]);

  return (
    <div
      className="message-input-container flex items-end p-4"
      style={{
        borderTop: `1px solid ${theme.secondaryColor}20`,
        backgroundColor: theme.inputBackgroundColor
      }}
      role="form"
      aria-label="Chat message input"
    >
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            handleInput();
          }}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isSending || disabled}
          className="w-full resize-none rounded-lg py-2 px-3 pr-10 focus:outline-none max-h-40"
          style={{
            border: `1px solid ${theme.secondaryColor}20`,
            backgroundColor: theme.backgroundColor,
            color: theme.inputTextColor,
            fontFamily: theme.fontFamily,
            borderRadius: theme.borderRadius,
            padding: '0.5rem 2.5rem 0.5rem 0.75rem'
          }}
          rows={1}
          aria-label="Type your message"
          aria-describedby={errorMessage ? "error-message" : "send-button"}
          aria-disabled={isSending || disabled}
        />
        <button
          id="send-button"
          onClick={handleSendClick}
          disabled={isSending || disabled || !inputValue.trim()}
          className="absolute right-2 bottom-2 rounded-full p-2 transition-colors"
          style={{
            backgroundColor: theme.primaryColor,
            color: 'white',
            opacity: (isSending || disabled || !inputValue.trim()) ? 0.5 : 1,
            cursor: (isSending || disabled || !inputValue.trim()) ? 'not-allowed' : 'pointer'
          }}
          aria-label="Send message"
          aria-disabled={isSending || disabled || !inputValue.trim()}
        >
          {isSending ? (
            <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          )}
        </button>
        {errorMessage && (
          <div
            id="error-message"
            className="text-red-500 text-sm mt-1"
            style={{ color: '#EF4444' }}
            role="alert"
            aria-live="assertive"
          >
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageInput;