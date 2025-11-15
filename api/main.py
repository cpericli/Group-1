import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from sqlalchemy.orm import Session
from .dependencies.database import engine, get_db
from .controllers import ratingsAndReviews
from typing import List

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)

@app.post("/ratings_and_reviews/", response_model=model_loader.Rating, tags=["RatingsAndReviews"])
def create_ratings_and_reviews(rating: model_loader.RatingCreate, db: Session= Depends(get_db)):
    return create_ratings_and_reviews.create(db=db, rating=rating)

@app.get("/ratings_and_reviews/", response_model=List[model_loader.Rating], tags=["RatingsAndReviews"])
def read_all_ratings(db: Session= Depends(get_db)):
    return ratingsAndReviews.read_all(db=db)

@app.put("/ratings_and_reviews/{rating_id}", response_model=model_loader.Rating, tags=["RatingsAndReviews"])
def update_one_rating_and_review(rating_id: int, rating: model_loader.RatingUpdate, db: Session = Depends(get_db)):
    rating_db = ratingsAndReviews.read_one(db=db, rating_id=rating_id)
    if rating_db is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return ratingsAndReviews.update(db=db, rating_id=rating_id, rating=rating)

@app.delete("/ratings_and_reviews/{rating_id}", response_model=model_loader.Rating, tags=["RatingsAndReviews"])
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating: ratingsAndReviews.read_one(db=db, rating_id=rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return ratingsAndReviews.delete(db=db, rating_id=rating_id)