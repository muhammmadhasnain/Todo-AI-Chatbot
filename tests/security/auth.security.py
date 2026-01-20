import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add the backend src directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

try:
    from backend.src.main import app  # Assuming you have a main.py file with the FastAPI app
except ImportError:
    # Create a mock app for testing if main.py doesn't exist yet
    from fastapi import FastAPI
    app = FastAPI()

class TestAuthSecurity:
    """
    Security-focused tests to validate proper authentication and authorization
    """

    def test_cross_user_access_prevention(self):
        """
        Test that users cannot access other users' data
        """
        # Mock client for testing
        with TestClient(app) as client:
            # Authenticate as user 1
            headers_user1 = {
                "Authorization": "Bearer valid-session-token-user1"
            }

            # Try to access user 2's data
            response = client.get(
                "/api/user2-id/tasks",
                headers=headers_user1
            )

            # Should return 403 Forbidden
            assert response.status_code == 403

    def test_invalid_session_handling(self):
        """
        Test that invalid sessions are properly rejected
        """
        with TestClient(app) as client:
            # Try with invalid session token
            headers = {
                "Authorization": "Bearer invalid-session-token"
            }

            response = client.get(
                "/api/test-user-id/tasks",
                headers=headers
            )

            # Should return 401 Unauthorized
            assert response.status_code == 401

    def test_session_token_manipulation(self):
        """
        Test protection against session token manipulation
        """
        with TestClient(app) as client:
            # Try with malformed session token
            headers = {
                "Authorization": "Bearer this-is-not-a-valid-token"
            }

            response = client.get(
                "/api/test-user-id/tasks",
                headers=headers
            )

            # Should return 401 Unauthorized
            assert response.status_code == 401

    def test_authentication_bypass_attempts(self):
        """
        Test protection against authentication bypass attempts
        """
        with TestClient(app) as client:
            # Try without Authorization header
            response = client.get("/api/test-user-id/tasks")

            # Should return 401 Unauthorized
            assert response.status_code == 401

            # Try with empty Authorization header
            headers = {
                "Authorization": ""
            }
            response = client.get(
                "/api/test-user-id/tasks",
                headers=headers
            )

            # Should return 401 Unauthorized
            assert response.status_code == 401

            # Try with malformed Authorization header
            headers = {
                "Authorization": "InvalidFormat token"
            }
            response = client.get(
                "/api/test-user-id/tasks",
                headers=headers
            )

            # Should return 401 Unauthorized
            assert response.status_code == 401

    def test_rate_limiting_enforcement(self):
        """
        Test that rate limiting is properly enforced
        """
        with TestClient(app) as client:
            # Authenticate user
            headers = {
                "Authorization": "Bearer valid-session-token"
            }

            # Make multiple requests to trigger rate limiting
            for i in range(10):  # More than the rate limit
                response = client.post(
                    "/api/test-user-id/chat",
                    json={"message": f"Test message {i}"},
                    headers=headers
                )

                # The first few requests should be OK, but after rate limit exceeded
                # we should get 429 status
                if i > 5:  # Assuming rate limit is around 5
                    if response.status_code == 429:
                        # Rate limit is working
                        break

            # Verify that at least one request was rate limited
            assert response.status_code == 429

if __name__ == "__main__":
    pytest.main([__file__])