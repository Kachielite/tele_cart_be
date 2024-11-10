import logging

from fastapi import File
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.product import Product
from app.schemas.product import ProductCreationRequest
from app.utils.image import ImageUtils

NOT_PRODUCT_OWNER = "Business does not own product"
PRODUCT_NOT_FOUND = "Product not found"

logger = logging.getLogger(__name__)

#Intialize ImageUtils
image_utils = ImageUtils()

# Create Product
def create_product(db: Session, product: ProductCreationRequest, business_id: int):
    logger.info("Create Product with the following details: %s %s %s %s %s", product.name, product.description, product.price, product.in_stock, product.category_id)

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        in_stock=product.in_stock,
        category_id=product.category_id,
        businesses_id=business_id
    )

    db.add(new_product)
    db.commit()
    logger.info("Product created successfully")

    return 201, {"message": "Product created successfully"}

# Add Product Image
def add_product_image(db: Session, product_id: int, image: File, business_id: int):
    logger.info("Add Image to Product with the following ID: %s", product_id)
    product = db.query(Product).filter(Product.id == product_id).first()

    if business_id != product.businesses_id:
        logger.error(NOT_PRODUCT_OWNER)
        return 403, {"message": NOT_PRODUCT_OWNER}

    if not product:
        logger.error(PRODUCT_NOT_FOUND)
        return 404, {"message": "Product not found"}

    # Delete the previous image if it exists
    if product.image_url:
        try:
            logger.info("Deleting previous image")
            image_utils.delete_image(product.image_url)
        except Exception as e:
            logger.error(f"Failed to delete previous image: {str(e)}")
            return 500, {"message": "Failed to delete previous image", "error": str(e)}

    try:
        logger.info("Uploading Image")
        image_url = image_utils.upload_image(image, "product")
        product.image_url = image_url
    except Exception as e:
        logger.error(f"Failed to upload image: {str(e)}")
        return 500, {"message": "Failed to upload image", "error": str(e)}

    db.commit()
    logger.info("Image added to Product")

    return 200, {"message": "Image added to Product"}

# Read Product
def read_product(db: Session, product_id: int, business_identifier: str):
    logger.info("Fetching Business ID")
    business_id = db.query(Business).filter(Business.identifier == business_identifier).first().id

    logger.info("Read Product with the following ID: %s", product_id)
    product = db.query(Product).filter(Product.id == product_id).first()

    if business_id != product.businesses_id:
        logger.error(NOT_PRODUCT_OWNER)
        return 403, {"message": NOT_PRODUCT_OWNER}

    if not product:
        logger.error(PRODUCT_NOT_FOUND)
        return 404, {"message": PRODUCT_NOT_FOUND}

    product_found = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "in_stock": product.in_stock,
            "image_url": product.image_url,
            "category_id": product.category_id,
            "created_at": product.created_at.isoformat(timespec='milliseconds') + 'Z',
            "updated_at": product.updated_at.isoformat(timespec='milliseconds') + 'Z'
        }

    logger.info("Product found")
    return 200, product_found


# Read all Products
def read_all_products(db: Session, business_identifier: str):
    logger.info("Fetching Business ID")
    business_id = db.query(Business).filter(Business.identifier == business_identifier).first().id

    logger.info("Reading all Products")
    products = db.query(Product).filter(Product.businesses_id == business_id).all()

    products_found = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "in_stock": product.in_stock,
            "image_url": product.image_url,
            "category_id": product.category_id,
            "created_at": product.created_at.isoformat(timespec='milliseconds') + 'Z',
            "updated_at": product.updated_at.isoformat(timespec='milliseconds') + 'Z'
        }
        for product in products
    ]

    logger.info("Products found")
    return 200, products_found


# Delete Product
def remove_product(db: Session, product_id: int, business_id: int):
    logger.info("Delete Product with the following ID: %s", product_id)
    product = db.query(Product).filter(Product.id == product_id).first()

    if business_id != product.businesses_id:
        logger.error(NOT_PRODUCT_OWNER)
        return 403, {"message": NOT_PRODUCT_OWNER}

    if not product:
        logger.error(PRODUCT_NOT_FOUND)
        return 404, {"message": PRODUCT_NOT_FOUND}
    try:
        logger.info("Deleting Product Image")
        image_utils.delete_image(product.image_url)
        logger.info("Product Image deleted")
    except Exception as e:
        logger.error("Failed to delete Product Image")
        return 500, {"message": "Failed to delete Product Image", "error": str(e)}

    db.delete(product)
    db.commit()
    logger.info("Product deleted")

    return 200, {"message": "Product deleted successfully"}