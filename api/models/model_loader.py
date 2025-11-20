from . import orders, order_details, recipes, sandwiches, resources, customers, menuItems, ratingsAndReviews,promotions, payment_info
from ..schemas import ratingsAndReviews as rating_schema
from ..schemas import promotions as promo_schema
from ..dependencies.database import engine


RatingCreate = rating_schema.RatingCreate
RatingUpdate = rating_schema.RatingUpdate
Rating = rating_schema.Rating

PromotionCreate = promo_schema.PromotionCreate
PromotionUpdate = promo_schema.PromotionUpdate
Promotion = promo_schema.Promotion

def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    menuItems.Base.metadata.create_all(engine)
    ratingsAndReviews.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    payment_info.Base.metadata.create_all(engine)
