from datetime import datetime
from pydantic import BaseModel

class SocialMediaUserBase(BaseModel):
    facebook_id: str
    name: str
    profile_pic_url: str | None = None

class SocialMediaUserCreate(SocialMediaUserBase):
    pass

class SocialMediaUser(SocialMediaUserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str
    timestamp: datetime

class CommentCreate(CommentBase):
    user: SocialMediaUserCreate

class Comment(CommentBase):
    id: int
    user: SocialMediaUser
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    content: str
    likes_count: int | None = 0
    shares_count: int | None = 0
    comments_count: int | None = 0
    timestamp: datetime

class PostCreate(PostBase):
    comments: list[CommentCreate] = []

class Post(PostBase):
    id: int
    comments: list[Comment] = []
    created_at: datetime

    class Config:
        orm_mode = True

class PageBase(BaseModel):
    username: str
    name: str
    url: str | None = None
    facebook_id: str | None = None
    profile_pic_url: str | None = None
    email: str | None = None
    website: str | None = None
    category: str | None = None
    followers_count: int | None = 0
    likes_count: int | None = 0
    creation_date: datetime | None = None

class PageCreate(PageBase):
    posts: list[PostCreate] = []
    followers: list[SocialMediaUserCreate] = []
    following: list[SocialMediaUserCreate] = []

class Page(PageBase):
    id: int
    posts: list[Post] = []
    followers: list[SocialMediaUser] = []
    following: list[SocialMediaUser] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PageFilters(BaseModel):
    name: str | None = None
    category: str | None = None
    follower_min: int | None = None
    follower_max: int | None = None
    page: int = 1
    per_page: int = 10