from sqlalchemy.orm import Session
from ..models import resources as resource_model
from ..models import sandwiches as sandwich_model
from ..models import recipes as recipe_model
from ..models import menuItems as menu_model
from ..models import promotions as promotion_model
from datetime import datetime

def seed_initial_data(db: Session):
    if db.query(resource_model.Resource).count() > 0:
        return

    # Resources
    bread = resource_model.Resource(item="Bread", amount=100)
    lettuce = resource_model.Resource(item="Lettuce", amount=50)
    tomato = resource_model.Resource(item="Tomato", amount=50)
    cheese = resource_model.Resource(item="Cheese", amount=40)
    turkey = resource_model.Resource(item="Turkey", amount=30)
    mayo = resource_model.Resource(item="Mayo", amount=20)
    avocado = resource_model.Resource(item="Avocado", amount=0)

    db.add_all([bread, lettuce, tomato, cheese, turkey, mayo, avocado])
    db.flush()

    # Sandwiches
    veggie = sandwich_model.Sandwich(sandwich_name="Veggie Sandwich", price=6.50)
    turkey_sandwich = sandwich_model.Sandwich(sandwich_name="Turkey Sandwich", price=7.50)
    avocado_deluxe = sandwich_model.Sandwich(sandwich_name="Avocado Deluxe", price=9.50)

    db.add_all([veggie, turkey_sandwich, avocado_deluxe])
    db.flush()

    # Promotions
    save20 = promotion_model.Promotion(
        promotion_code='SAVE20',
        description='20% off your order',
        discount_percentage=20.00,
        discount_amount=None,
        expiration_date=datetime(2025, 12, 31, 23, 59, 59),
        is_active=True
    )

    black_friday = promotion_model.Promotion(
        promotion_code='BLACKFRIDAY',
        description='Black Friday Special - 30% off',
        discount_percentage=30.00,
        discount_amount=None,
        expiration_date=datetime(2025, 11, 29, 23, 59, 59),
        is_active=True
    )

    new_year = promotion_model.Promotion(
        promotion_code='NEWYEAR26',
        description='Happy New Year 2026 - 50% Your First Order in the New Year',
        discount_percentage=50.00,
        discount_amount=None,
        expiration_date=datetime(2026, 1, 10, 23, 59, 59),
        is_active=True
    )

    summer = promotion_model.Promotion(
        promotion_code='SUMMER25',
        description='Summer Sale - 25% off',
        discount_percentage=25.00,
        discount_amount=None,
        expiration_date=datetime(2025, 8, 31, 23, 59, 59),
        is_active=False
    )

    holidays = promotion_model.Promotion(
        promotion_code='HAPPYH0l!DAYS',
        description='Happy Holidays End of Year Sale - 40% off',
        discount_percentage=40.00,
        discount_amount=None,
        expiration_date=datetime(2025, 12, 28, 23, 59, 59),
        is_active=False
    )

    db.add_all([save20, black_friday, new_year, summer, holidays])
    db.flush()

    # Recipes
    db.add_all([
        # Veggie Sandwich
        recipe_model.Recipe(sandwich_id=veggie.id, resource_id=bread.id, amount=2),
        recipe_model.Recipe(sandwich_id=veggie.id, resource_id=lettuce.id, amount=1),
        recipe_model.Recipe(sandwich_id=veggie.id, resource_id=tomato.id, amount=1),
        recipe_model.Recipe(sandwich_id=veggie.id, resource_id=cheese.id, amount=1),

        # Turkey Sandwich
        recipe_model.Recipe(sandwich_id=turkey_sandwich.id, resource_id=bread.id, amount=2),
        recipe_model.Recipe(sandwich_id=turkey_sandwich.id, resource_id=turkey.id, amount=2),
        recipe_model.Recipe(sandwich_id=turkey_sandwich.id, resource_id=cheese.id, amount=1),
        recipe_model.Recipe(sandwich_id=turkey_sandwich.id, resource_id=mayo.id, amount=1),

        # Avocado Deluxe – this will ALWAYS fail ingredient check because avocado=0
        recipe_model.Recipe(sandwich_id=avocado_deluxe.id, resource_id=bread.id, amount=2),
        recipe_model.Recipe(sandwich_id=avocado_deluxe.id, resource_id=avocado.id, amount=2),
    ])

    # Menu items
    db.add_all([
        menu_model.MenuItems(
            dish="Veggie Sandwich",
            ingredients="Bread, Lettuce, Tomato, Cheese",
            price=6.50,
            calories=450,
            food_category="Vegetarian",
        ),
        menu_model.MenuItems(
            dish="Turkey Sandwich",
            ingredients="Bread, Turkey, Cheese, Mayo",
            price=7.50,
            calories=550,
            food_category="High Protein",
        ),
        menu_model.MenuItems(
            dish="Avocado Deluxe",
            ingredients="Bread, Avocado, Lettuce",
            price=9.50,
            calories=650,
            food_category="Vegetarian",
        ),
    ])

    db.commit()
