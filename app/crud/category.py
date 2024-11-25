import logging

from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.category import Category
from app.models.product import Product

BUSINESS_NOT_FOUND = "Business not found"

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


# Get all Categories with Products for a Business
def get_categories_with_products(business_identifier: str, db: Session):
    logger.info(f"Fetching all categories with products for business_identifier: {business_identifier}")
    business = db.query(Business).filter(Business.identifier == business_identifier).first()

    if business is None:
        logger.error(f"Business not found for business_identifier: {business_identifier}")
        return 404, {"message": BUSINESS_NOT_FOUND}

    # Fetch unique category IDs from products for the given business
    category_ids = db.query(Product.category_id).filter(Product.businesses_id == business.id).distinct().all()
    category_ids = [category_id[0] for category_id in category_ids]

    # Retrieve categories based on the fetched category IDs
    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    logger.info(f"Categories with products fetched successfully for business_identifier: {business_identifier}")
    return 200, categories