from . import orders, order_details, menuItems, promotions, ratingsAndReviews, customers, payment_info


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menuItems.router)
    app.include_router(promotions.router)
    app.include_router(ratingsAndReviews.router)
    app.include_router(customers.router)
    app.include_router(payment_info.router)
