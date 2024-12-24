from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import Literal



class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False
    
class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owener_id : int
    owner : UserResponse

    
class UserCreate(BaseModel):
    email: EmailStr
    password: str


    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id: Optional[str] = None
    # token_type : str
    
class VoteCreate(BaseModel):
    post_id: int
    dir: Literal[0,1]
    
    
