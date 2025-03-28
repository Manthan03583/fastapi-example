from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title : str
    content : str 
    published : bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner: UserOut

    class Config:
        # orm_mode = True
        from_attributes = True

class PostOut(BaseModel):
    Post:Post
    votes: int

    class Config:
        # orm_mode = True
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)] 
    # this assign 1 or less than 1 value to dor cause we need 0 or 1