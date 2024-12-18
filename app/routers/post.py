from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func



router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)


#---------------------------- Get all posts: sqlAlchemy ------------------------------#
@router.get("/", response_model=list[schemas.PostResponse])
def get_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),
             limit:int = 20,
             skip : int = 0,
             search: Optional[str] = ""):
    print(current_user.id, "===========")
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip)
    post = db.query(models.Post).filter(models.Post.owener_id == current_user.id).limit(limit=limit).offset(skip)
    return post




#---------------------------- Create a post: sqlAlchemy ------------------------------#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # 
    print("**************",current_user.id)
    new_post = models.Post(owener_id = current_user.id,**post.dict()) # unpack it
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#---------------------------- Get a post by id: sqlAlchemy ---------------------------#
@router.get("/{id}", response_model=schemas.PostResponse)
def get_one_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    count = db.query(func.count(models.Vote.post_id)).filter(models.Vote.post_id == id).scalar()
    # print("------------", count)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

    post.vote_count = count

    return post




#---------------------------- Delete a post by id: sqlAlchemy -----------------------#
@router.delete("/{id}")
def delete_post(id:int, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    post_db = post_query.first()
    print("****************",post_db)
    
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found")
    
    if post_db.owener_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized for requested action")
         
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "post got deleted"}








#---------------------------- Update a post by id ---------------------------#
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(post: schemas.PostCreate, id:int, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    post_db = post_query.first()
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found")
    
    if post_db.owener_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized for requested action")
    
    print("_______________>>>>>>>>",type(post))
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"message": "testing update"}