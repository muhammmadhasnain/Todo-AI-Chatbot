# Quickstart: Todo AI Chatbot Backend

## Prerequisites

- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless recommended)
- Better Auth account and configuration
- OpenAI API key
- Node.js 18+ (for frontend if needed)

## Setup

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <your-repo-url>
cd todo-agent-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Required environment variables:
```env
DATABASE_URL="postgresql://username:password@localhost:5432/todo_agent_db"
BETTER_AUTH_URL="http://localhost:4000/api/auth"
BETTER_AUTH_SECRET="your-better-auth-secret"
OPENAI_API_KEY="your-openai-api-key"
SECRET_KEY="your-secret-key"
```

### 3. Database Setup
```bash
# Run database migrations
cd backend
python -m src.services.data init_db

# Or using Alembic if available
alembic upgrade head
```

### 4. Better Auth Configuration
```bash
# Start Better Auth server separately
# Follow Better Auth documentation for setup
npm install better-auth
# Configure with auth.config.ts
```

### 5. Start Services

Backend:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Frontend (if applicable):
```bash
cd frontend
npm install
npm run dev
```

## MCP Server Integration

The system includes an MCP server that exposes 5 core tools:

1. `add_task` - Create new tasks
2. `list_tasks` - Retrieve user tasks
3. `complete_task` - Mark tasks as complete
4. `delete_task` - Remove tasks
5. `update_task` - Modify tasks

These tools are automatically registered and available to the AI agent.

## API Endpoints

### Chat API
- `POST /api/{user_id}/chat` - Process chat messages and return AI responses

### Task API
- `GET /api/{user_id}/tasks` - List user tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

### Authentication
All endpoints require valid Better Auth session tokens.

## Testing

Run unit tests:
```bash
cd backend
pytest tests/unit/
```

Run integration tests:
```bash
cd backend
pytest tests/integration/
```

## Development

### Adding New MCP Tools
1. Add the tool function to `backend/src/mcp/tools.py`
2. Register it in the MCP server configuration
3. Update the agent configuration to include the new tool

### Modifying Data Models
1. Update the model in `backend/src/models/`
2. Create a new migration using Alembic
3. Run the migration
4. Update related services and API endpoints