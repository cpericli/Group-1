from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import ratingsAndReviews as controller
from ..schemas import ratingsAndReviews as schema

router = APIRouter(
    tags=["Ratings and Reviews"],
    prefix="/ratings_and_reviews"
)

@router.post("/", response_model=schema.Rating)
def create_ratings_and_reviews(rating: schema.RatingCreate, db: Session= Depends(get_db)):
    return controller.create(db=db, rating=rating)

@router.get("/", response_model=list[schema.Rating])
def read_all_ratings(db: Session= Depends(get_db)):
    return controller.read_all(db=db)

@router.put("/{rating_id}", response_model=schema.Rating)
def update_one_rating_and_review(rating_id: int, rating: schema.RatingUpdate, db: Session = Depends(get_db)):
    rating_db = controller.read_one(db=db, rating_id=rating_id)
    if rating_db is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return controller.update(db=db, rating_id=rating_id, rating=rating)

@router.delete("/{rating_id}", response_model=schema.Rating)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = controller.delete(db=db, rating_id=rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating