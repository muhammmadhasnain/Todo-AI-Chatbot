from fastapi import Request, HTTPException
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import time

class RateLimiter:
    """
    Rate limiter that limits requests based on authenticated user_id.
    Implements the requirement of 5 attempts per 15 minutes per IP/user for protected endpoints.
    """

    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        self.max_attempts = max_attempts
        self.window_seconds = window_minutes * 60
        # Store attempts by user_id
        self.attempts: Dict[str, list] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if the user is allowed to make another request.
        """
        now = time.time()

        # Clean up old attempts outside the window
        if user_id in self.attempts:
            self.attempts[user_id] = [
                timestamp for timestamp in self.attempts[user_id]
                if now - timestamp < self.window_seconds
            ]

        # Check if user has exceeded the limit
        if len(self.attempts[user_id]) >= self.max_attempts:
            return False

        # Record the new attempt
        self.attempts[user_id].append(now)
        return True

# Global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_by_user(user_id: str) -> None:
    """
    Rate limiting function that checks if the authenticated user is within rate limits.
    """
    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {rate_limiter.max_attempts} attempts per {rate_limiter.window_seconds/60} minutes."
        )