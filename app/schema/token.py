from pydantic import BaseModel
from typing import Optional

# Schema for the JWT access token response.
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# Schema for the data encoded within the JWT.
class TokenPayload(BaseModel):
    sub: Optional[str] = None # 'sub' is the standard claim for subject (user identifier)

# Schema for the refresh token request body
class TokenRefreshRequest(BaseModel):
    refresh_token: str
