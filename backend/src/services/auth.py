import logging
from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from ..config import settings

logger = logging.getLogger(__name__)

class SessionVerificationResponse(BaseModel):
    user_id: str
    email: str
    name: Optional[str] = None
    is_valid: bool
    expires_at: Optional[str] = None

class SessionVerificationService:
    def __init__(self):
        # Better Auth server URL (typically runs with Next.js frontend on port 3000)
        # Using settings from config which loads from .env file
        self.better_auth_url = settings.BETTER_AUTH_URL
        self.better_auth_secret = settings.BETTER_AUTH_SECRET

    async def verify_session_with_cookies(self, cookies: Dict[str, str]) -> SessionVerificationResponse:
        """
        Verify a session by making a request to Better Auth with the provided cookies.
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Make the API call to Better Auth to verify the session using cookies
                auth_url = self.better_auth_url.rstrip('/')

                logger.debug(f"Attempting to verify session with cookies: {list(cookies.keys()) if cookies else 'None'}")

                # Enhanced logging to help with debugging
                if not cookies:
                    logger.warning("No cookies provided for session verification")
                    return SessionVerificationResponse(
                        user_id="",
                        email="",
                        name=None,
                        is_valid=False,
                        expires_at=None
                    )

                # Try the main session endpoint first
                session_url = f"{auth_url}/session"
                logger.debug(f"Session URL: {session_url}")

                response = await client.get(
                    session_url,
                    cookies=cookies
                )

                logger.debug(f"Better Auth session endpoint response status: {response.status_code}")

                if response.status_code == 200:
                    # Session is valid, parse the response
                    try:
                        data = response.json()
                        logger.debug(f"Better Auth session response data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")

                        # Better Auth typically returns the session and user data directly
                        # without nesting in "session" and "user" keys
                        session_info = data if isinstance(data, dict) else {}
                        user_info = session_info.get("user", {}) or session_info

                        # Extract user ID, email, and name from either format
                        user_id = session_info.get("userId") or session_info.get("user", {}).get("id") or session_info.get("id", "")
                        email = session_info.get("email") or session_info.get("user", {}).get("email") or session_info.get("userEmail", "")
                        name = session_info.get("name") or session_info.get("user", {}).get("name") or session_info.get("userName", "")

                        return SessionVerificationResponse(
                            user_id=user_id,
                            email=email,
                            name=name,
                            is_valid=True,
                            expires_at=session_info.get("expiresAt") or session_info.get("expires", None)
                        )
                    except Exception as parse_error:
                        logger.error(f"Error parsing session response: {parse_error}")
                        # If parsing fails, treat as invalid session
                        return SessionVerificationResponse(
                            user_id="",
                            email="",
                            name=None,
                            is_valid=False,
                            expires_at=None
                        )

                elif response.status_code == 401:
                    # Session is invalid or expired
                    logger.info("Session is invalid (401)")
                    return SessionVerificationResponse(
                        user_id="",
                        email="",
                        name=None,
                        is_valid=False,
                        expires_at=None
                    )
                elif response.status_code == 404:
                    # Session endpoint not found - try alternative endpoints
                    logger.debug("Session endpoint not found, trying /me endpoint")

                    me_url = f"{auth_url}/me"
                    logger.debug(f"Trying /me endpoint: {me_url}")

                    me_response = await client.get(
                        me_url,
                        cookies=cookies
                    )

                    logger.debug(f"Better Auth /me endpoint response status: {me_response.status_code}")

                    if me_response.status_code == 200:
                        try:
                            data = me_response.json()
                            logger.debug(f"Better Auth /me response data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")

                            # Handle different response formats
                            if isinstance(data, dict):
                                # If response is an object with user info
                                user_info = data.get("user", data)  # Handle both nested and flat structures

                                user_id = user_info.get("id", user_info.get("_id", ""))
                                email = user_info.get("email", "")
                                name = user_info.get("name", user_info.get("userName", ""))
                            else:
                                # Unexpected response format
                                user_id = ""
                                email = ""

                            return SessionVerificationResponse(
                                user_id=user_id,
                                email=email,
                                name=name,
                                is_valid=True,
                                expires_at=None  # /me endpoint might not return expiration info
                            )
                        except Exception as parse_error:
                            logger.error(f"Error parsing /me response: {parse_error}")
                            return SessionVerificationResponse(
                                user_id="",
                                email="",
                                name=None,
                                is_valid=False,
                                expires_at=None
                            )
                    elif me_response.status_code == 404:
                        # Try the /get-session endpoint which Better Auth also exposes
                        logger.debug("Trying /get-session endpoint as alternative")
                        get_session_url = f"{auth_url}/get-session"

                        get_session_response = await client.get(
                            get_session_url,
                            cookies=cookies
                        )

                        logger.debug(f"Better Auth /get-session endpoint response status: {get_session_response.status_code}")

                        if get_session_response.status_code == 200:
                            try:
                                data = get_session_response.json()
                                logger.debug(f"Better Auth /get-session response data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")

                                # Handle different response formats for /get-session
                                if isinstance(data, dict):
                                    # The response might have user info directly or nested
                                    user_info = data.get("user", data) if isinstance(data, dict) else data

                                    user_id = user_info.get("id", user_info.get("userId", user_info.get("_id", "")))
                                    email = user_info.get("email", user_info.get("userEmail", ""))
                                    name = user_info.get("name", user_info.get("userName", ""))
                                else:
                                    user_id = ""
                                    email = ""
                                    name = ""

                                return SessionVerificationResponse(
                                    user_id=user_id,
                                    email=email,
                                    name=name,
                                    is_valid=True,
                                    expires_at=None  # /get-session might not return expiration info
                                )
                            except Exception as parse_error:
                                logger.error(f"Error parsing /get-session response: {parse_error}")
                                return SessionVerificationResponse(
                                    user_id="",
                                    email="",
                                    name=None,
                                    is_valid=False,
                                    expires_at=None
                                )
                        elif get_session_response.status_code == 404:
                            # All endpoints return 404, which means no valid session exists
                            logger.warning(f"All session endpoints (/session, /me, /get-session) returned 404. No valid session exists.")
                            return SessionVerificationResponse(
                                user_id="",
                                email="",
                                name=None,
                                is_valid=False,
                                expires_at=None
                            )
                        else:
                            # /get-session endpoint returned a different error
                            logger.error(f"/get-session endpoint failed with status: {get_session_response.status_code}")
                            logger.error(f"Response text: {get_session_response.text}")
                            raise HTTPException(
                                status_code=503,
                                detail=f"Authentication service returned unexpected status from /get-session: {get_session_response.status_code}. Please ensure the frontend server is running and Better Auth is properly configured."
                            )
                    else:
                        # /me endpoint returned a different error
                        logger.error(f"/me endpoint failed with status: {me_response.status_code}")
                        logger.error(f"Response text: {me_response.text}")
                        raise HTTPException(
                            status_code=503,
                            detail=f"Authentication service returned unexpected status: {me_response.status_code}. Please ensure the frontend server is running and Better Auth is properly configured."
                        )
                else:
                    # Unexpected response from Better Auth API
                    logger.error(f"Better Auth API error: {response.status_code}, {response.text}")

                    # If we get a 500 or other server error, it might mean the frontend server isn't running properly
                    if response.status_code >= 500:
                        raise HTTPException(
                            status_code=503,
                            detail="Authentication service is not available. Please ensure the frontend server is running on http://localhost:3000."
                        )
                    else:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Better Auth API error: {response.status_code} - {response.text}"
                        )

        except httpx.ConnectError as e:
            logger.error(f"Connection error to Better Auth: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Authentication service is not available. Please ensure the frontend server is running on http://localhost:3000."
            )
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error when connecting to Better Auth: {str(e)}")
            raise HTTPException(
                status_code=504,
                detail="Timeout connecting to Better Auth server. Please ensure the frontend server is running and responsive."
            )
        except httpx.RequestError as e:
            # Handle other HTTP-related errors
            logger.error(f"HTTP request error when connecting to Better Auth: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Authentication service request failed. Please ensure the frontend server is running and accessible."
            )
        except Exception as e:
            # Other errors
            logger.error(f"General session verification error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Session verification error: {str(e)}"
            )

# Global instance of the service
session_verification_service = SessionVerificationService()