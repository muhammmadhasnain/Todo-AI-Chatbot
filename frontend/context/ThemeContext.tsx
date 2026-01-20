import React, { createContext, useContext, useState, ReactNode } from 'react';

// Define the theme structure
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

// Define the context type
interface ThemeContextType {
  theme: ChatTheme;
  updateTheme: (newTheme: Partial<ChatTheme>) => void;
}

// Default theme values
const defaultTheme: ChatTheme = {
  primaryColor: '#8B5CF6', // purple-500
  secondaryColor: '#EC4899', // pink-500
  backgroundColor: '#FFFFFF',
  textColor: '#374151',
  inputBackgroundColor: '#F9FAFB',
  inputTextColor: '#1F2937',
  borderRadius: '0.5rem', // 8px
  spacing: '1rem', // 16px
  fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
};

// Create the context
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme provider component
interface ThemeProviderProps {
  children: ReactNode;
  initialTheme?: Partial<ChatTheme>;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  initialTheme = {}
}) => {
  const [theme, setTheme] = useState<ChatTheme>({
    ...defaultTheme,
    ...initialTheme
  });

  const updateTheme = (newTheme: Partial<ChatTheme>) => {
    setTheme(prev => ({
      ...prev,
      ...newTheme
    }));
  };

  return (
    <ThemeContext.Provider value={{ theme, updateTheme }}>
      <div
        style={{
          backgroundColor: theme.backgroundColor,
          color: theme.textColor,
          fontFamily: theme.fontFamily,
        }}
        className="h-full w-full"
      >
        {children}
      </div>
    </ThemeContext.Provider>
  );
};

// Custom hook to use the theme context
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Export the default theme for direct use
export { defaultTheme };