from sqlalchemy.orm import Session
from ..models import resources as resource_model
from ..models import sandwiches as sandwich_model
from ..models import recipes as recipe_model
from ..models import menuItems as menu_model

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

    db.add_all([bread, lettuce, tomato, cheese, turkey, mayo])
    db.flush()

    # Sandwiches
    veggie = sandwich_model.Sandwich(sandwich_name="Veggie Sandwich", price=6.50)
    turkey_sandwich = sandwich_model.Sandwich(sandwich_name="Turkey Sandwich", price=7.50)

    db.add_all([veggie, turkey_sandwich])
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
    ])

    db.commit()
