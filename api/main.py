import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from sqlalchemy.orm import Session
from .dependencies.database import engine, get_db
from .controllers import ratingsAndReviews, promotions

from .dependencies.database import Base
from .dependencies.database import get_db
from api.controllers import orders as order_controller
from api.controllers import payment_info as payment_controller
from api.schemas.orders import Order, OrderCreate, OrderUpdate
from api.schemas.payment_info import Payment, PaymentCreate, PaymentUpdate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/promotions/", response_model=model_loader.Promotion, tags=["Promotions"])
def create_promotion(promotion: model_loader.PromotionCreate, db: Session = Depends(get_db)):
    """Create a new promotion"""
    return promotions.create(db=db, promotion=promotion)

@app.get("/promotions/", response_model=List[model_loader.Promotion], tags=["Promotions"])
def read_all_promotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all promotions"""
    return promotions.read_all(db=db, skip=skip, limit=limit)

@app.get("/promotions/active", response_model=List[model_loader.Promotion], tags=["Promotions"])
def read_active_promotions(db: Session = Depends(get_db)):
    """Get all active and non-expired promotions"""
    return promotions.read_active(db=db)

@app.get("/promotions/{promotion_id}", response_model=model_loader.Promotion, tags=["Promotions"])
def read_one_promotion(promotion_id: int, db: Session = Depends(get_db)):
    """Get a specific promotion"""
    promotion = promotions.read_one(db=db, promotion_id=promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion

@app.get("/promotions/code/{promotion_code}", response_model=model_loader.Promotion, tags=["Promotions"])
def read_promotion_by_code(promotion_code: str, db: Session = Depends(get_db)):
    """Get a promotion by its code"""
    promotion = promotions.read_by_code(db=db, promotion_code=promotion_code)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion code not found")
    return promotion

@app.put("/promotions/{promotion_id}", response_model=model_loader.Promotion, tags=["Promotions"])
def update_promotion(promotion_id: int, promotion: model_loader.PromotionUpdate, db: Session = Depends(get_db)):
    """Update a promotion"""
    db_promotion = promotions.read_one(db=db, promotion_id=promotion_id)
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotions.update(db=db, promotion_id=promotion_id, promotion=promotion)


@app.delete("/promotions/{promotion_id}", response_model=model_loader.Promotion, tags=["Promotions"])
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    """Delete a promotion"""
    promotion = promotions.read_one(db=db, promotion_id=promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotions.delete(db=db, promotion_id=promotion_id)


@app.post("/promotions/apply/{order_id}/{promotion_id}", tags=["Promotions"])
def apply_promotion(order_id: int, promotion_id: int, db: Session = Depends(get_db)):
    """Apply a promotion to an order"""
    return promotions.apply_promotion_to_order(db=db, order_id=order_id, promotion_id=promotion_id)


@app.delete("/promotions/remove/{order_id}", tags=["Promotions"])
def remove_promotion(order_id: int, db: Session = Depends(get_db)):
    """Remove promotion from an order"""
    return promotions.remove_promotion_from_order(db=db, order_id=order_id)

# ==========================
#        ORDER ROUTES
# ==========================

@app.post("/orders/", response_model=Order, tags=["Orders"])
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_controller.create(db=db, request=order)


@app.get("/orders/", response_model=List[Order], tags=["Orders"])
def read_all_orders(db: Session = Depends(get_db)):
    return order_controller.read_all(db=db)


@app.get("/orders/{order_id}", response_model=Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    return order_controller.read_one(db=db, item_id=order_id)


@app.put("/orders/{order_id}", response_model=Order, tags=["Orders"])
def update_order(order_id: int, update: OrderUpdate, db: Session = Depends(get_db)):
    return order_controller.update(db=db, item_id=order_id, request=update)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return order_controller.delete(db=db, item_id=order_id)



@app.post("/payment_info/{order_id}", response_model=Payment, tags=["PaymentInfo"])
def create_payment(order_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    return payment_controller.create(db=db, payment=payment, order_id=order_id)


@app.get("/payment_info/", response_model=List[Payment], tags=["PaymentInfo"])
def read_all_payments(db: Session = Depends(get_db)):
    return payment_controller.read_all(db=db)


@app.get("/payment_info/{payment_id}", response_model=Payment, tags=["PaymentInfo"])
def read_one_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_controller.read_one(db=db, payment_id=payment_id)


@app.put("/payment_info/{payment_id}", response_model=Payment, tags=["PaymentInfo"])
def update_payment(payment_id: int, update: PaymentUpdate, db: Session = Depends(get_db)):
    return payment_controller.update(db=db, payment_id=payment_id, update_data=update)


@app.delete("/payment_info/{payment_id}", tags=["PaymentInfo"])
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_controller.delete(db=db, payment_id=payment_id)
