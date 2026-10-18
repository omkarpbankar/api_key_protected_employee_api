import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# Expected API key; default to requirement example 'super30-secret-key' or override via environment
API_KEY_NAME = "X-API-Key"
EXPECTED_API_KEY = os.getenv("API_KEY", "super30-secret-key")

api_key_header_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header_scheme)) -> str:
    """
    Validates the X-API-Key header.
    Returns 401 Unauthorized if the header is missing.
    Returns 403 Forbidden if the header key is invalid.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide the 'X-API-Key' header.",
        )
    if api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid API Key provided.",
        )
    return api_key
