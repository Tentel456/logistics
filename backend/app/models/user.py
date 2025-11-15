from pydantic import BaseModel, Field

class UserOut(BaseModel):
    id: str
    email: str
    role: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
