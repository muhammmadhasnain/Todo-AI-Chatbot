import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat import router as chat_router
from .api.tasks import router as tasks_router
from .api.users import router as users_router
from .api.auth import router as auth_router
from .api.mcp import router as mcp_router
from .config import settings
from .mcp.server import mcp_server
import asyncio
import threading
import uvicorn

logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL or "http://localhost:3000"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to frontend
    expose_headers=["Authorization"]
)

# Include API routers
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(tasks_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users")
app.include_router(auth_router, prefix="/api/auth")  # Auth endpoints have their own prefix
app.include_router(mcp_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Todo AI Chatbot Backend", "status": "running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "todo-ai-chatbot-backend"}

# Authentication health check endpoint
@app.get("/auth/health")
async def auth_health_check():
    from .services.auth import session_verification_service
    try:
        # Test connection to Better Auth with proper URL handling
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            auth_url = settings.BETTER_AUTH_URL.rstrip('/')
            # The URL should be in the format http://localhost:3000/api/auth, so we append /session
            session_url = f"{auth_url}/session"

            response = await client.get(session_url)

            # Also test the /me endpoint for completeness
            me_url = f"{auth_url}/me"
            me_response = await client.get(me_url)

            return {
                "auth_service": "available",
                "session_endpoint_status": response.status_code,
                "me_endpoint_status": me_response.status_code,
                "better_auth_url": auth_url,
                "configured": True
            }
    except httpx.ConnectError:
        return {
            "auth_service": "unavailable",
            "error": "Cannot connect to Better Auth service. Is the frontend server running on http://localhost:3000?",
            "recommended_action": "Start the frontend server with 'npm run dev' in the frontend directory"
        }
    except httpx.TimeoutException:
        return {
            "auth_service": "timeout",
            "error": "Timeout connecting to Better Auth service",
            "recommended_action": "Check if the frontend server is responsive"
        }
    except Exception as e:
        return {
            "auth_service": "error",
            "error": str(e),
            "recommended_action": "Verify Better Auth configuration and ensure frontend server is running"
        }


# Detailed authentication diagnostics endpoint
@app.get("/auth/diagnostics")
async def auth_diagnostics():
    """Detailed diagnostics for authentication system to help troubleshoot issues."""
    import httpx
    from .config import settings
    from .services.auth import session_verification_service

    diagnostics = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "better_auth_config": {
            "url": settings.BETTER_AUTH_URL,
            "secret_configured": bool(settings.BETTER_AUTH_SECRET),
        },
        "connection_tests": {},
        "recommendations": []
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Test various auth endpoints
            endpoints_to_test = [
                f"{settings.BETTER_AUTH_URL}/session",
                f"{settings.BETTER_AUTH_URL}/me",
                f"{settings.BETTER_AUTH_URL}/sign-in",
                f"{settings.BETTER_AUTH_URL}/sign-out"
            ]

            for endpoint in endpoints_to_test:
                try:
                    response = await client.get(endpoint)
                    diagnostics["connection_tests"][endpoint] = {
                        "status": response.status_code,
                        "reachable": response.status_code != 0,
                        "error": None
                    }
                except Exception as e:
                    diagnostics["connection_tests"][endpoint] = {
                        "status": 0,
                        "reachable": False,
                        "error": str(e)
                    }

        # Add recommendations based on results
        auth_reachable = any(test.get("reachable", False) for test in diagnostics["connection_tests"].values())
        if not auth_reachable:
            diagnostics["recommendations"].append("Frontend server is not reachable. Please start it with 'npm run dev' in the frontend directory.")

        if not settings.BETTER_AUTH_SECRET:
            diagnostics["recommendations"].append("BETTER_AUTH_SECRET is not configured. Please set it in your environment variables.")

    except Exception as e:
        diagnostics["error"] = f"Could not perform diagnostics: {str(e)}"

    return diagnostics

# Start the MCP server in a separate thread when the application starts
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Todo AI Chatbot Backend...")
    logger.info(f"Registered {len(mcp_server.tools)} MCP tools")

    # Create database tables if they don't exist (user profile table is for application-specific data)
    from .db.session import create_tables
    try:
        create_tables()
        logger.info("Application database tables (including user profiles) created/verified successfully")
        logger.info("Note: Authentication is managed by Better Auth, user profiles are stored separately")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    # Start MCP server in a background thread
    def run_mcp_server():
        import asyncio
        from mcp import stdio_server
        async def start_server():
            # The tools are registered during initialization, so we just need to run the server
            await mcp_server.run_server()

        asyncio.run(start_server())

    # Run MCP server in a separate thread
    import threading
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()
    logger.info("MCP server started in background thread")

if __name__ == "__main__":
    # Run the server with uvicorn when executed directly
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )