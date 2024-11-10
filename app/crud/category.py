import logging

from sqlalchemy.orm import Session

from app.models.category import Category

logger = logging.getLogger(__name__)

# Read all categories
def fetch_categories(db: Session):
    logger.info("Fetching all categories")

    fetched_categories = db.query(Category).all()

    categories = [{
        "id": category.id,
        "name": category.name,
        "description": category.description
    } for category in fetched_categories]

    logger.info("Categories fetched successfully")
    return 200, categories


# Read category by id
def fetch_category_by_id(category_id: int, db: Session):
    logger.info(f"Fetching category details for category_id: {category_id}")
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        logger.error(f"Category not found for category_id: {category_id}")
        return 404, {"message": "Category not found"}

    fetched_category = {
        "id": category.id,
        "name": category.name,
        "description": category.description
    }

    logger.info(f"Category details fetched successfully for category_id: {category_id}")
    return 200, fetched_category