import logging
from datetime import datetime, timezone

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import validate_password, create_token, encrypt_password, decode_token
from app.models.business import Business
from app.schemas.auth import AuthRequestSchema
from app.utils.identifier_generator import identifier_generator

logger = logging.getLogger(__name__)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/v1/auth/token", scheme_name="JWT")

def create_business(business: AuthRequestSchema, db: Session):
    logger.info("Creating business with the following details: %s %s %s", business.business_name, business.email, business.phone_number)
    existing_email = db.query(Business).filter(Business.email == business.email).first()
    existing_phone_number = db.query(Business).filter(Business.phone_number == business.phone_number).first()

    if existing_email or existing_phone_number:
        logger.error("Business with email or phone number already exists")
        return 409, {"message": "Business with email or phone number already exists"}

    new_business = Business(
        business_name=business.business_name,
        identifier=identifier_generator(business.business_name),
        phone_number=business.phone_number,
        email=business.email,
        password=encrypt_password(business.password),
        is_active=True,
    )

    logger.info("Adding business to the database")
    db.add(new_business)
    db.commit()
    logger.info("Business created successfully")
    return 201, {"message": "Business created successfully"}


def auth_business(form_data:OAuth2PasswordRequestForm , db: Session):
    logger.info("Authenticating business with email: %s", form_data.username)
    business = db.query(Business).filter(Business.email == form_data.username).first()

    if business is None:
        logger.error("Business not found")
        return 404, {"message": "Business not found"}

    if not validate_password(form_data.password, business.password):
        logger.error("Wrong Credentials")
        return 401, {"message": "Wrong Credentials"}

    token = create_token(business.id)
    logger.info("Business authenticated successfully")
    return 200, {"access_token": token, "token_type": "bearer"}


def get_current_business(token: str, db: Session):
    try:
        logger.info("Getting current business")
        token_data = decode_token(token)

        if token_data.get("expires_at") < datetime.now(timezone.utc).timestamp():
            logger.error("Token expired")
            return 401, {"message": "token expired"}

        logger.info("Fetching business details")
        business = db.query(Business).filter(Business.id == token_data.get('id')).first()

        if business is None:
            logger.error("Business not found")
            return 401, {"message": "Invalid token"}

        logger.info("Business details fetched successfully")
        return 200, {"id": business.id, "business_name": business.business_name, "identifier": business.identifier}

    except ValueError:
        logger.error("Invalid token")
        return 401, {"message": "Authentication failed"}
