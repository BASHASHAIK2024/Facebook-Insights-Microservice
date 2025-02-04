from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from database import Base

page_follower_association = Table(
    'page_follower_association',
    Base.metadata,
    Column('page_id', ForeignKey('pages.id'), primary_key=True),
    Column('user_id', ForeignKey('social_media_users.id'), primary_key=True)
)

page_following_association = Table(
    'page_following_association',
    Base.metadata,
    Column('page_id', ForeignKey('pages.id'), primary_key=True),
    Column('user_id', ForeignKey('social_media_users.id'), primary_key=True)
)

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    url = Column(String(255))
    facebook_id = Column(String(255))
    profile_pic_url = Column(String(512))
    email = Column(String(255))
    website = Column(String(255))
    category = Column(String(255))
    followers_count = Column(Integer)
    likes_count = Column(Integer)
    creation_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    posts = relationship("Post", back_populates="page")
    followers = relationship("SocialMediaUser", secondary=page_follower_association)
    following = relationship("SocialMediaUser", secondary=page_following_association)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"))
    content = Column(Text)
    likes_count = Column(Integer)
    shares_count = Column(Integer)
    comments_count = Column(Integer)
    timestamp = Column(DateTime)
    created_at = Column(DateTime)

    page = relationship("Page", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("social_media_users.id"))
    content = Column(Text)
    timestamp = Column(DateTime)
    created_at = Column(DateTime)

    post = relationship("Post", back_populates="comments")
    user = relationship("SocialMediaUser", back_populates="comments")

class SocialMediaUser(Base):
    __tablename__ = "social_media_users"

    id = Column(Integer, primary_key=True, index=True)
    facebook_id = Column(String(255))
    name = Column(String(255))
    profile_pic_url = Column(String(512))
    created_at = Column(DateTime)

    comments = relationship("Comment", back_populates="user")