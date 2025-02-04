from sqlalchemy.orm import Session
from models import Page, Post, Comment, SocialMediaUser

def get_page(db: Session, username: str):
    return db.query(Page).filter(Page.username == username).first()

def create_page(db: Session, page: dict):
    db_page = Page(**page)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page

def get_or_create_user(db: Session, user_data: dict):
    user = db.query(SocialMediaUser).filter(SocialMediaUser.facebook_id == user_data['facebook_id']).first()
    if not user:
        user = SocialMediaUser(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def create_post(db: Session, post_data: dict, page_id: int):
    post = Post(**post_data, page_id=page_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def create_comment(db: Session, comment_data: dict, post_id: int):
    user_data = comment_data.pop('user')
    user = get_or_create_user(db, user_data)
    comment = Comment(**comment_data, post_id=post_id, user_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def add_followers(db: Session, page: Page, followers: list[dict]):
    for follower_data in followers:
        user = get_or_create_user(db, follower_data)
        page.followers.append(user)
    db.commit()

def add_following(db: Session, page: Page, following: list[dict]):
    for user_data in following:
        user = get_or_create_user(db, user_data)
        page.following.append(user)
    db.commit()

def get_pages_with_filters(db: Session, filters: dict):
    query = db.query(Page)
    if filters.name:
        query = query.filter(Page.name.ilike(f"%{filters.name}%"))
    if filters.category:
        query = query.filter(Page.category == filters.category)
    if filters.follower_min is not None:
        query = query.filter(Page.followers_count >= filters.follower_min)
    if filters.follower_max is not None:
        query = query.filter(Page.followers_count <= filters.follower_max)
    return query.offset((filters.page - 1) * filters.per_page).limit(filters.per_page).all()