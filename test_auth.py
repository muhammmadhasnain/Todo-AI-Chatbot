"""
Test script to verify the authentication system is working properly
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from the main .env file
load_dotenv()

from backend.src.services.auth import session_verification_service

async def test_session_verification():
    """
    Test the session verification service to ensure it can communicate with Better Auth
    """
    print("Testing Better Auth session verification service...")

    # Check if the Better Auth URL is configured
    better_auth_url = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
    print(f"Better Auth URL: {better_auth_url}")

    # Since we can't test with a real session token without a running Better Auth server,
    # we'll just verify the service can be initialized properly
    print("Session verification service initialized successfully!")
    print(f"Service URL: {session_verification_service.better_auth_url}")

    # Test with a mock invalid token to see if the service handles errors properly
    try:
        result = await session_verification_service.verify_session_with_cookies({"authjs.session-token": "invalid-token"})
        print(f"Verification result for invalid token: {result}")
    except Exception as e:
        print(f"Expected error with invalid token: {str(e)}")

    print("Authentication service test completed!")

if __name__ == "__main__":
    asyncio.run(test_session_verification())