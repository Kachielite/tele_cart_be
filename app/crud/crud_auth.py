from datetime import datetime, timezone

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import validate_password, create_token, encrypt_password, decode_token
from app.models.business import Business
from app.schemas.auth_schema import AuthRequestSchema
from app.utils.identifier_generator import identifier_generator

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token", scheme_name="JWT")

def create_business(business: AuthRequestSchema, db: Session):
    existing_email = db.query(Business).filter(Business.email == business.email).first()
    existing_phone_number = db.query(Business).filter(Business.phone_number == business.phone_number).first()

    if existing_email or existing_phone_number:
        return 409, {"message": "Business with email or phone number already exists"}

    new_business = Business(
        business_name=business.business_name,
        identifier=identifier_generator(business.business_name),
        phone_number=business.phone_number,
        email=business.email,
        password=encrypt_password(business.password),
        is_active=True,
    )

    db.add(new_business)
    db.commit()
    return 201, {"message": "Business created successfully"}


def auth_business(form_data:OAuth2PasswordRequestForm , db: Session):
    business = db.query(Business).filter(Business.email == form_data.username).first()
    if business is None:
        return 404, {"message": "Business not found"}

    if not validate_password(form_data.password, business.password):
        return 401, {"message": "Wrong Credentials"}

    token = create_token(business.id)
    return 200, {"access_token": token, "token_type": "bearer"}


def get_current_business(token: str, db: Session):
    try:
        token_data = decode_token(token)
        if token_data.get("expires_at") < datetime.now(timezone.utc).timestamp():
            return 401, {"message": "token expired"}
        business = db.query(Business).filter(Business.id == token_data.get('id')).first()
        if business is None:
            return 401, {"message": "Invalid token"}
        return 200, {"id": business.id, "business_name": business.business_name, "identifier": business.identifier}
    except ValueError:
        return 401, {"message": "Authentication failed"}
