import uvicorn
import sys
import os
import logging
from src.main import app

# Add the backend directory to the path so we can import from config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Todo AI Chatbot Backend...")
    logger.info(f"Server will run on {settings.SERVER_HOST}:{settings.SERVER_PORT}")

    # Run the FastAPI application with uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    main()
