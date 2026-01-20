"""
Test script to verify frontend-backend communication for authentication
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_backend_auth_communication():
    """
    Test that the backend can communicate with Better Auth API
    """
    print("Testing frontend-backend authentication communication...")

    # Get the Better Auth URL from settings
    better_auth_url = os.getenv("BETTER_AUTH_URL", "http://localhost:3000/api/auth")
    print(f"Testing Better Auth URL: {better_auth_url}")

    # Test if the Better Auth server is accessible (this would fail if server not running)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Try to access the session endpoint with an invalid token
            # This will return a 401, but that's expected and shows the server is accessible
            response = await client.get(
                f"{better_auth_url}/session",
                headers={"Authorization": "Bearer invalid-token"},
            )
            print(f"Better Auth API response: {response.status_code}")

            if response.status_code == 401:
                print("[OK] Better Auth API is accessible and responding correctly")
            elif response.status_code == 200:
                print("? Better Auth API returned 200, which is unexpected for invalid token")
            else:
                print(f"? Better Auth API returned unexpected status: {response.status_code}")

    except httpx.ConnectError:
        print("[ERROR] Better Auth API is not accessible. Is the frontend server running on http://localhost:3000?")
        print("  To fix: Start the frontend server with 'cd frontend && npm run dev'")
        return False
    except httpx.TimeoutException:
        print("[ERROR] Timeout connecting to Better Auth API. Server might be slow to respond.")
        return False
    except Exception as e:
        print(f"[ERROR] Error connecting to Better Auth API: {str(e)}")
        return False

    return True

async def test_backend_initialization():
    """
    Test that the backend can initialize properly without database errors
    """
    print("\nTesting backend initialization...")

    try:
        # Import the backend components to check for initialization errors
        from backend.src.services.auth import SessionVerificationService

        # Create a service instance
        service = SessionVerificationService()
        print(f"[OK] Session verification service initialized with URL: {service.better_auth_url}")

        # Test that the service can be created without errors
        print("[OK] Backend authentication service initialized successfully")
        return True

    except Exception as e:
        print(f"[ERROR] Backend initialization error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("Frontend-Backend Communication Test")
    print("=" * 50)

    # Test backend initialization first
    init_ok = await test_backend_initialization()

    # Test communication
    comm_ok = await test_backend_auth_communication()

    print("\n" + "=" * 50)
    if init_ok and comm_ok:
        print("[OK] All communication tests PASSED!")
        print("\nBackend can properly communicate with Better Auth API.")
        print("Authentication should work once both servers are running.")
    else:
        print("[ERROR] Some communication tests FAILED!")
        print("\nCheck that:")
        print("1. Frontend server is running on http://localhost:3000")
        print("2. Environment variables are properly set")
        print("3. Better Auth is properly configured in the frontend")

if __name__ == "__main__":
    asyncio.run(main())