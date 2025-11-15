import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from sqlalchemy.orm import Session
from .dependencies.database import engine, get_db
from .controllers import orders, order_details

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

@app.post("/ratings_and_reviews/", response_model=model_loader.ratingsAndReviews, tags=["RatingsAndRevies"])
def create_ratings_and_reviews(rating: model_loader.RatingCreate, db: Session= Depends(get_db)):
    return create_ratings_and_reviews.create(db=db, ratings_and_reviews=rating)

@app.get("/ratings_and_reviews/", response_model=model_loader.ratingsAndReviews, tags=["RatingsAndReviews"])
def read_ratings_and_reviews(db: Session= Depends(get_db)):
    return read_ratings_and_reviews.read_all(db=db)

@app.put("/ratings_and_reviews/{rating_id}", response_model=model_loader.ratingsAndReviews, tags=["RatingsAndReviews"])
def update_one_rating_and_review(rating_id: int, rating: model_loader.RatingUpdate, db: Session = Depends(get_db)):
    rating_db = model_loader.ratings_and_reviews.read_one(db=db, rating_id=rating_id)
    if rating_db is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return model_loader.ratings_and_reviews.update(db=db, rating_id=rating_id, rating=rating)

@app.delete("/ratings_and_reviews/{rating_id}", response_model=model_loader.ratingsAndReviews, tags=["RatingsAndReviews"])
def delete_one_rating_and_review(rating_id: int, db: Session = Depends(get_db)):
    rating: model_loader.ratings_and_reviews.read_one(db=db, rating_id=rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return model_loader.ratings_and_reviews.delete(db=db, rating_id=rating_id)