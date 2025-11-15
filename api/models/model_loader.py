from . import orders, order_details, recipes, sandwiches, resources, customers, menuItems, ratingsAndReviews,promotions, paymentInfo

from ..dependencies.database import engine


RatingCreate = ratingsAndReviews.RatingCreate
RatingUpdate = ratingsAndReviews.RatingUpdate
RatingsAndReviews = ratingsAndReviews.Rating

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
    paymentInfo.Base.metadata.create_all(engine)
