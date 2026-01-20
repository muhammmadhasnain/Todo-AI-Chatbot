import React, { useState, useEffect, useCallback } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { ThemeProvider } from '../../context/ThemeContext';
import { sendChatMessage, getUserConversations, getConversation } from '../../lib/chat-api';

interface ChatKitProps {
  sessionId?: string;
  userId?: string;
  authToken?: string;
  endpoint: string; // Backend API endpoint
  initialMessages?: ChatMessage[];
  placeholder?: string;
  disabled?: boolean;
  showHeader?: boolean;
  showInput?: boolean;
  theme?: ChatTheme;
  customMessageRenderer?: (message: ChatMessage) => React.ReactNode;
  customInputRenderer?: () => React.ReactNode;
  onMessageSend?: (message: ChatMessage) => void;
  onMessageReceive?: (message: ChatMessage) => void;
  onError?: (error: ChatError) => void;
  onStatusChange?: (status: ChatStatus) => void;
}

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  status: 'sent' | 'sending' | 'delivered' | 'error';
  metadata?: Record<string, any>;
}

interface ChatError {
  code: string;
  message: string;
  details?: any;
  timestamp: Date;
}

interface ChatTheme {
  primaryColor: string;
  secondaryColor: string;
  backgroundColor: string;
  textColor: string;
  inputBackgroundColor: string;
  inputTextColor: string;
  borderRadius: string;
  spacing: string;
  fontFamily: string;
}

interface ChatStatus {
  status: 'idle' | 'connecting' | 'connected' | 'disconnected' | 'error';
}

export function ChatKitComponent({ theme: propTheme, ...restProps }: ChatKitProps) {
  // Initialize messages from localStorage if available, otherwise use initialMessages or empty array
  const initializeMessages = (): ChatMessage[] => {
    if (restProps.userId) {
      const savedMessages = localStorage.getItem(`chat-messages-${restProps.userId}`);
      if (savedMessages) {
        try {
          return JSON.parse(savedMessages).map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp) // Convert string back to Date
          }));
        } catch (e) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error parsing saved messages:', e);
          }
        }
      }
    }
    return restProps.initialMessages || [];
  };

  const [messages, setMessages] = useState<ChatMessage[]>(initializeMessages());
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);

  // Load initial conversation history from backend to sync with server data
  useEffect(() => {
    const loadInitialConversation = async () => {
      if (restProps.userId) {
        setIsLoading(true);

        try {
          // Get user's conversations from backend
          const userConversations = await getUserConversations(restProps.userId);

          if (userConversations && userConversations.length > 0) {
            // Use the most recent conversation (first in the list due to descending order)
            const mostRecentConversation = userConversations[0];
            setCurrentConversationId(mostRecentConversation.id);

            // Load messages from this conversation
            const conversationData = await getConversation(restProps.userId, mostRecentConversation.id);
            if (conversationData.messages) {
              // Convert the received messages to proper ChatMessage format
              const backendMessages: ChatMessage[] = conversationData.messages.map((msg: any) => ({
                id: msg.id,
                content: msg.content,
                role: msg.role,
                timestamp: new Date(msg.timestamp),
                status: msg.status || 'sent'
              }));

              // Update state and localStorage with backend data to ensure sync
              setMessages(backendMessages);
              localStorage.setItem(`chat-messages-${restProps.userId}`, JSON.stringify(backendMessages));
            }
          }
        } catch (error) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error loading initial conversation from backend:', error);
          }
          // If backend fails, we keep the messages loaded from localStorage during initialization
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadInitialConversation();
  }, [restProps.userId]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (restProps.userId) {
      localStorage.setItem(`chat-messages-${restProps.userId}`, JSON.stringify(messages));
    }
  }, [messages, restProps.userId]);

  // Load messages when currentConversationId changes (e.g., when switching conversations)
  useEffect(() => {
    const loadMessagesForConversation = async () => {
      if (restProps.userId && currentConversationId) {
        setIsLoading(true);
        try {
          const conversationData = await getConversation(restProps.userId, currentConversationId);
          if (conversationData.messages) {
            // Convert the received messages to proper ChatMessage format
            const backendMessages: ChatMessage[] = conversationData.messages.map((msg: any) => ({
              id: msg.id,
              content: msg.content,
              role: msg.role,
              timestamp: new Date(msg.timestamp),
              status: msg.status || 'sent'
            }));

            // Update state and localStorage with backend data
            setMessages(backendMessages);
            localStorage.setItem(`chat-messages-${restProps.userId}`, JSON.stringify(backendMessages));
          }
        } catch (error) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error loading messages for conversation:', error);
          }
          // Fallback to loading from localStorage if backend fails
          const savedMessages = localStorage.getItem(`chat-messages-${restProps.userId}`);
          if (savedMessages) {
            try {
              const parsedMessages: ChatMessage[] = JSON.parse(savedMessages).map((msg: any) => ({
                ...msg,
                timestamp: new Date(msg.timestamp) // Convert string back to Date
              }));
              setMessages(parsedMessages);
            } catch (e) {
              if (process.env.NODE_ENV === 'development') {
                console.error('Error parsing saved messages:', e);
              }
            }
          }
        } finally {
          setIsLoading(false);
        }
      }
    };

    // Only load if we have a conversation ID that's different from initial load
    if (restProps.userId && currentConversationId) {
      loadMessagesForConversation();
    }
  }, [restProps.userId, currentConversationId]);

  const handleSendMessage = useCallback(async (messageData: { id: string; content: string; timestamp: Date }) => {
    if (!restProps.userId) {
      throw new Error('User ID is required');
    }

    // Add the user message to the state immediately
    const userMessage: ChatMessage = {
      id: messageData.id,
      content: messageData.content,
      role: 'user',
      timestamp: messageData.timestamp,
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);

    // Optionally call the onMessageSend callback
    if (restProps.onMessageSend) {
      restProps.onMessageSend(userMessage);
    }

    try {
      // Send the message to the backend API and get the AI response
      const response = await sendChatMessage(
        restProps.userId,
        messageData.content,
        currentConversationId || undefined
      );

      // Update the current conversation ID if it changed
      if (response.conversation_id && currentConversationId !== response.conversation_id) {
        setCurrentConversationId(response.conversation_id);
      }

      // Add the AI response to the messages
      const aiMessage: ChatMessage = {
        id: `ai-${Date.now()}`,
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        status: 'sent'
      };

      setMessages(prev => [...prev, aiMessage]);

      // Optionally call the onMessageReceive callback
      if (restProps.onMessageReceive) {
        restProps.onMessageReceive(aiMessage);
      }
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Error sending message to backend:', error);
      }

      // Add an error message to the UI
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request.',
        role: 'system',
        timestamp: new Date(),
        status: 'error'
      };

      setMessages(prev => [...prev, errorMessage]);

      // Optionally call the onError callback
      if (restProps.onError) {
        restProps.onError({
          code: 'API_ERROR',
          message: error instanceof Error ? error.message : 'Unknown error occurred',
          timestamp: new Date()
        });
      }
    }
  }, [restProps.userId, restProps.onMessageSend, restProps.onMessageReceive, restProps.onError, currentConversationId]);

  const handleNewMessage = useCallback((message: ChatMessage) => {
    setMessages(prev => [...prev, message]);
    if (restProps.onMessageReceive) {
      restProps.onMessageReceive(message);
    }
  }, [restProps.onMessageReceive]);

  return (
    <ThemeProvider initialTheme={propTheme}>
      <div
        className="flex flex-col h-full w-full"
        role="region"
        aria-label="Chat interface"
      >
        <div className="h-full w-full flex flex-col">
          {restProps.showHeader !== false && (
            <div className="p-4 border-b border-gray-200" role="banner">
              <h2 className="text-lg font-semibold text-gray-800">Chat</h2>
            </div>
          )}
          <div
            className="flex-1 overflow-y-auto p-4"
            role="main"
            aria-label="Chat messages area"
          >
            {isLoading ? (
              <div className="flex justify-center items-center h-full" role="status" aria-live="polite">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600" aria-label="Loading messages"></div>
              </div>
            ) : (
              <MessageList messages={messages} />
            )}
          </div>
          {restProps.showInput !== false && (
            <MessageInput
              sessionId={restProps.sessionId}
              userId={restProps.userId}
              onSendMessage={handleSendMessage}
              disabled={restProps.disabled}
              placeholder={restProps.placeholder || 'Type your message...'}
            />
          )}
        </div>
      </div>
    </ThemeProvider>
  );
}

export default ChatKitComponent;