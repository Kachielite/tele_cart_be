import logging

from fastapi import File
from sqlalchemy.orm import Session

from app.models.business import Business
from app.schemas.business import BusinessRequestSchema
from app.utils.image import ImageUtils

logger = logging.getLogger(__name__)

BUSINESS_NOT_FOUND = "Business not found"

# Fetch business details
def business_details(business_id: int, db: Session):
    logger.info(f"Fetching business details for business_id: {business_id}")
    business = db.query(Business).filter(Business.id == business_id).first()

    if business is None:
        logger.error(f"Business not found for business_id: {business_id}")
        return 404, {"message": "Business not found"}

    fetched_business = {
        "id": business.id,
        "identifier": business.identifier,
        "name": business.business_name,
        "address": business.address,
        "phone_number" : business.phone_number,
        "description" : business.description,
        "image_url" : business.image_url,
        "created_at" : business.created_at.isoformat(timespec='milliseconds') + 'Z',
        "updated_at" : business.updated_at.isoformat(timespec='milliseconds') + 'Z',
    }

    logger.info(f"Business details fetched successfully for business_id: {business_id}")
    return 200, fetched_business


# Update business details
def update_business(business_id: int, business: BusinessRequestSchema, db: Session):
    logger.info(f"Updating business details for business_id: {business_id}")
    business_to_update = db.query(Business).filter(Business.id == business_id).first()

    if business_to_update is None:
        logger.error(f"Business not found for business_id: {business_id}")
        return 404, {"message": BUSINESS_NOT_FOUND}

    if business.name:
        logger.info(f"Updating business name to: {business.name}")
        business_to_update.business_name = business.name
    if business.address:
        logger.info(f"Updating business address to: {business.address}")
        business_to_update.address = business.address
    if business.description:
        logger.info(f"Updating business description to: {business.description}")
        business_to_update.description = business.description

    logger.info(f"Committing changes to the database")
    db.add(business_to_update)
    db.commit()

    logger.info(f"Business details updated successfully for business_id: {business_id}")
    return 200, {"message": "Business updated successfully"}

# Update business image
def update_business_image(business_id: int, image: File, db: Session):
    logger.info(f"Updating business image for business_id: {business_id}")
    business_to_update = db.query(Business).filter(Business.id == business_id).first()

    if business_to_update is None:
        logger.error(f"Business not found for business_id: {business_id}")
        return 404, {"message": "Business not found"}

    # Check if an image file is provided
    if image is None or image.file is None:
        logger.error("No image file provided for upload")
        return 400, {"message": "No image file provided"}

    # Instantiate ImageUtils class
    image_utils = ImageUtils()

    # Delete the existing image if there is one
    if business_to_update.image_url:
        try:
            logger.info(f"Deleting existing image: {business_to_update.image_url}")
            image_utils.delete_image(business_to_update.image_url)
        except Exception as e:
            logger.error(f"Failed to delete previous image: {str(e)}")
            return 500, {"message": "Failed to delete previous image", "error": str(e)}

    # Upload the new image
    try:
        logger.info("Uploading new image")
        new_image_url = image_utils.upload_image(image, "business")
        business_to_update.image_url = new_image_url
    except Exception as e:
        logger.error(f"Failed to upload new image: {str(e)}")
        return 500, {"message": "Failed to upload image", "error": str(e)}

    # Commit changes to the database
    try:
        logger.info("Committing changes to the database")
        db.add(business_to_update)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to commit changes to the database: {str(e)}")
        return 500, {"message": "Failed to save image to the database", "error": str(e)}

    logger.info(f"Business image updated successfully for business_id: {business_id}")
    return 200, {"message": "Business image updated successfully"}