from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    full_name: str
    role: str


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
