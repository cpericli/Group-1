from sqlalchemy.orm import Session
from ..models.ratingsAndReviews import RatingAndReview
from ..schemas.ratingsAndReviews import RatingCreate, RatingUpdate

def create(db: Session, rating: RatingCreate):
    db_rating = RatingAndReview(**rating.model_dump())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def read_all(db: Session):
    return db.query(RatingAndReview).all()

def read_one(db: Session, rating_id: int):
    return db.query(RatingAndReview).filter(RatingAndReview.id == rating_id).first()

def update(db: Session, rating_id: int, rating: RatingUpdate):
    db_rating = db.query(RatingAndReview).filter(RatingAndReview.id == rating_id).first()
    if db_rating:
        update_data = rating.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_rating, key, value)
        db.commit()
        db.refresh(db_rating)
    return db_rating

def delete(db: Session, rating_id: int):
    db_rating = db.query(RatingAndReview).filter(RatingAndReview.id == rating_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return db_rating