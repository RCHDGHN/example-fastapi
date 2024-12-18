from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional




router = APIRouter(
    prefix= "/votes",
    tags= ["Votes"]
)


# add a vote

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteCreate, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
   
    if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exit") 
            
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on {vote.post_id}")

        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote created"}
    else:
       if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found")
        
       vote_query.delete(synchronize_session=False)
       db.commit()
       return {"message": "vote got delete"}
    