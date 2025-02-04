from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, crud, scraper, models
from .database import get_db

app = FastAPI()

@app.get("/pages/{username}", response_model=schemas.Page)
def get_page(username: str, db: Session = Depends(get_db)):
    db_page = crud.get_page(db, username)
    if db_page:
        return db_page
    # Scrape if not found
    scraped_data = scraper.scrape_facebook_page(username)
    if not scraped_data:
        raise HTTPException(status_code=404, detail="Page not found")
    # Create page and related data
    page_info = scraped_data['page_info']
    db_page = models.Page(**page_info)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    # Add followers
    for follower in scraped_data['followers']:
        user = crud.get_or_create_user(db, follower)
        db_page.followers.append(user)
    # Add following
    for user_data in scraped_data['following']:
        user = crud.get_or_create_user(db, user_data)
        db_page.following.append(user)
    # Add posts and comments
    for post_data in scraped_data['posts']:
        post = models.Post(**post_data, page_id=db_page.id)
        db.add(post)
        db.commit()
        db.refresh(post)
        for comment_data in post_data['comments']:
            user = crud.get_or_create_user(db, comment_data['user'])
            comment = models.Comment(**comment_data, post_id=post.id, user_id=user.id)
            db.add(comment)
    db.commit()
    return db_page

@app.get("/pages/", response_model=List[schemas.Page])
def get_pages(filters: schemas.PageFilters = Depends(), db: Session = Depends(get_db)):
    return crud.get_pages_with_filters(db, filters)

@app.get("/pages/{username}/followers", response_model=List[schemas.SocialMediaUser])
def get_followers(username: str, db: Session = Depends(get_db)):
    page = crud.get_page(db, username)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.followers

@app.get("/pages/{username}/following", response_model=List[schemas.SocialMediaUser])
def get_following(username: str, db: Session = Depends(get_db)):
    page = crud.get_page(db, username)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.following

@app.get("/pages/{username}/posts", response_model=List[schemas.Post])
def get_posts(username: str, db: Session = Depends(get_db)):
    page = crud.get_page(db, username)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.posts[:15]  # Return recent 15 posts