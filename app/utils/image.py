import logging
import cloudinary
import cloudinary.uploader
from fastapi import File

from app.core.config import settings

BUSINESS_IMAGES_FOLDER = "telecart/business_profiles"
PRODUCT_IMAGES_FOLDER = "telecart/product_images"

logger = logging.getLogger(__name__)


class ImageUtils:
    def __init__(self):
        logger.info("Initializing Cloudinary")
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )

    @staticmethod
    def upload_image(image: File, upload_type: str):
        try:
            upload_folder = BUSINESS_IMAGES_FOLDER if upload_type == "business" else PRODUCT_IMAGES_FOLDER

            logger.info(f"Uploading image: {image.filename}")
            image_url = cloudinary.uploader.upload(image.file, folder=upload_folder)

            logger.info(f"Image uploaded successfully: {image_url['secure_url']}")
            return image_url["secure_url"]
        except Exception as e:
            logger.error(f"Error from uploading {str(e)}")
            raise Exception(str(e))

    @staticmethod
    def get_image_url(image_url: str):
        return cloudinary.CloudinaryImage(image_url).image()

    @staticmethod
    def delete_image(image_url: str):
        try:
            # Extract everything after '/upload/' and remove the version and extension
            public_id = '/'.join(image_url.split('/upload/')[1].split('/')[1:]).split('.')[0]

            logger.info(f"Deleting image with id in image util: {public_id}")

            # Perform the deletion using the full public_id
            result = cloudinary.uploader.destroy(public_id)
            logger.info(f"Deletion result: {result}")
        except Exception as e:
            logger.error(f"Error from deletion {str(e)}")
            raise Exception(str(e))


