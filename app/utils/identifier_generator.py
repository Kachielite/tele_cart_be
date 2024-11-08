import uuid

def identifier_generator(business_name: str) -> str:
    prefix = business_name[:3].upper()
    unique_suffix = str(uuid.uuid4())[:4]
    return f"{prefix}{unique_suffix.upper()}"