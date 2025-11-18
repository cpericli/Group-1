from . import orders, order_details, menu, menuItems, promotions, ratingsAndReviews


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu.router)
    app.include_router(menuItems.router)
    app.include_router(promotions.router)
    app.include_router(ratingsAndReviews.router)
