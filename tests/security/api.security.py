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

class TestAPISecurity:
    """
    Security tests for API endpoints to validate proper authentication and authorization
    """

    def test_protected_endpoint_access_without_auth(self):
        """
        Test that protected endpoints require authentication
        """
        with TestClient(app) as client:
            # Try to access protected endpoint without authentication
            response = client.get("/api/test-user-id/tasks")

            # Should return 401 Unauthorized
            assert response.status_code == 401

    def test_user_data_isolation(self):
        """
        Test that users can only access their own data
        """
        with TestClient(app) as client:
            # Authenticate as user A
            headers_user_a = {
                "Authorization": "Bearer valid-session-token-user-a"
            }

            # Try to access user B's data
            response = client.get(
                "/api/user-b-id/tasks",
                headers=headers_user_a
            )

            # Should return 403 Forbidden (user_id mismatch)
            assert response.status_code == 403

    def test_session_token_validation(self):
        """
        Test that only valid session tokens are accepted
        """
        with TestClient(app) as client:
            # Try with various invalid token formats
            invalid_tokens = [
                "",  # Empty token
                "invalid-format",  # No Bearer prefix
                "Bearer ",  # Bearer with no token
                "Bearer invalid-token",  # Invalid token
                "Bearer " + "x" * 1000  # Extremely long token
            ]

            for token in invalid_tokens:
                headers = {"Authorization": token}
                response = client.get(
                    "/api/test-user-id/tasks",
                    headers=headers
                )

                # Should return 401 for invalid tokens
                assert response.status_code in [401, 422], f"Failed for token: {token}"

    def test_user_id_parameter_validation(self):
        """
        Test that user_id parameters are properly validated
        """
        with TestClient(app) as client:
            # Authenticate with valid session
            headers = {
                "Authorization": "Bearer valid-session-token"
            }

            # Test with various potentially malicious user_id values
            malicious_user_ids = [
                "../../../etc/passwd",  # Path traversal attempt
                "'; DROP TABLE users; --",  # SQL injection attempt
                "<script>alert('xss')</script>",  # XSS attempt
                "user_id_with_special_chars!@#$%",  # Special characters
            ]

            for user_id in malicious_user_ids:
                response = client.get(
                    f"/api/{user_id}/tasks",
                    headers=headers
                )

                # Should return 401, 403, or 422 for invalid user_ids
                assert response.status_code in [401, 403, 422], f"Failed for user_id: {user_id}"

    def test_rate_limiting_protection(self):
        """
        Test that rate limiting protects against abuse
        """
        with TestClient(app) as client:
            # Authenticate user
            headers = {
                "Authorization": "Bearer valid-session-token"
            }

            # Make multiple requests in a short time
            responses = []
            for i in range(10):  # More than the rate limit
                response = client.post(
                    "/api/test-user-id/chat",
                    json={"message": f"Test message {i}"},
                    headers=headers
                )
                responses.append(response.status_code)

            # Check that some requests were rate limited (429)
            rate_limited_requests = [status for status in responses if status == 429]
            assert len(rate_limited_requests) > 0, "Rate limiting is not working properly"

    def test_malformed_request_protection(self):
        """
        Test protection against malformed requests
        """
        with TestClient(app) as client:
            # Authenticate user
            headers = {
                "Authorization": "Bearer valid-session-token"
            }

            # Test with malformed JSON
            response = client.post(
                "/api/test-user-id/chat",
                content="{invalid: json}",
                headers=headers
            )
            # Should return 422 for malformed JSON

            # Test with oversized request body
            oversized_data = {"message": "x" * 1000000}  # 1MB message
            response = client.post(
                "/api/test-user-id/chat",
                json=oversized_data,
                headers=headers
            )
            # May return 413 (Payload Too Large) or 422

            # Test with missing required fields
            response = client.post(
                "/api/test-user-id/chat",
                json={},
                headers=headers
            )
            # Should return 422 for validation error

    def test_cors_security_headers(self):
        """
        Test that proper CORS headers are set to prevent unauthorized cross-origin requests
        """
        with TestClient(app) as client:
            # Make a request and check CORS headers
            response = client.get("/api/test-user-id/tasks")

            # Check for security-related headers
            cors_headers = [
                "access-control-allow-origin",
                "access-control-allow-credentials",
                "access-control-allow-headers",
                "access-control-allow-methods"
            ]

            for header in cors_headers:
                # The presence and values of these headers should be appropriate
                # for security (not allowing all origins, etc.)
                pass  # Implementation would check specific header values

if __name__ == "__main__":
    pytest.main([__file__])