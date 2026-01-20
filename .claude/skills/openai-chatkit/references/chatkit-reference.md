# OpenAI ChatKit Reference Documentation

## API Configuration Options

The ChatKitOptions type defines all possible configuration options for ChatKit:

```typescript
type ChatKitOptions = {
  api: CustomApiConfig | HostedApiConfig;
  composer?: ComposerOption;
  disclaimer?: DisclaimerOption;
  entities?: EntitiesOption;
  header?: HeaderOption;
  history?: HistoryOption;
  initialThread?: null | string;
  locale?: SupportedLocale;
  onClientTool?: (toolCall: {
    name: string;
    params: Record<string, unknown>;
  }) => Promise<Record<string, unknown>> | Record<string, unknown>;
  startScreen?: StartScreenOption;
  theme?: ColorScheme | ThemeOption;
  threadItemActions?: ThreadItemActionsOption;
  widgets?: WidgetsOption;
};
```

## Supported Locales

ChatKit supports multiple locales for internationalization:
- en (English)
- es (Spanish)
- fr (French)
- de (German)
- ja (Japanese)
- and more...

## Theme Configuration

### Color Schemes
- light: Light mode theme
- dark: Dark mode theme
- auto: Automatically detect system preference

### Radius Options
- square: Sharp corners
- soft: Slightly rounded corners
- round: Fully rounded corners

## History Options

The history configuration allows you to control chat history features:

```typescript
type HistoryOption = {
  enabled: boolean;
  showDelete: boolean;
  showRename: boolean;
  maxThreads?: number;
};
```

## Composer Attachments

File attachment options include:
- maxSize: Maximum file size in bytes (default: 100MB)
- maxCount: Maximum number of attachments per message (default: 10)
- accept: MIME type filter for file uploads