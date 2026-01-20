# Quickstart Guide: Agentic Chat System

## Prerequisites

- Python 3.11+
- Node.js 18+
- Next.js 16+
- PostgreSQL (Neon Serverless)
- OpenAI API key
- Better Auth credentials

## Setup Steps

### 1. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Update the following variables:
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_neon_database_url
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_chatkit_domain_key
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install fastapi openai sqlmodel python-multipart better-fastapi python-mcp-sdk

# Run database migrations
python -m backend.db.init

# Start the MCP server
python -m backend.mcp.server
```

### 3. Frontend Setup

```bash
# Install Node.js dependencies
npm install @openai/chatkit-client next react react-dom

# Start the development server
npm run dev
```

### 4. Authentication Setup

```bash
# Configure Better Auth
npx better-auth-cli init
```

## Architecture Overview

```
User → OpenAI ChatKit UI → FastAPI → OpenAI Agent → MCP Tools → PostgreSQL
```

## Key Components

### MCP Tools
- `add_task`: Create new tasks
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark tasks as complete
- `delete_task`: Remove tasks
- `update_task`: Modify existing tasks

### Database Models
- User: Authentication and user data
- Conversation: Chat session tracking
- Message: Individual chat messages
- Task: User's to-do items

## Running Tests

```bash
# Backend tests
pytest tests/

# Frontend tests
npm run test
```

## Development Workflow

1. Define new MCP tools in `mcp/tools.py`
2. Update agent to use new tools if needed
3. Test tool contracts independently
4. Verify integration through chat endpoint