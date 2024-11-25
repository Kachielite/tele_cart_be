import logging

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.cart import Cart
from app.models.customer import Customer
from app.models.product import Product

logger = logging.getLogger(__name__)

BUSINESS_NOT_FOUND = "Business not found"

def add_item_to_cart(db: Session, business_identifier: str, product_id: int, user_info):
    logger.info("Received payload for adding item to cart: %s %s %s", business_identifier, product_id, user_info)

    # Check if customer exists
    existing_customer = db.query(Customer).filter(Customer.telegram_id == user_info.id).first()

    if existing_customer is None:
        logger.info("Creating new customer")
        new_customer = Customer(
            name=f"{user_info.first_name} {user_info.last_name}",
            telegram_id=user_info.id,
        )
        db.add(new_customer)
        db.flush()  # Ensures `new_customer.id` is available for new_order
    else:
        logger.info("Customer already exist, no further action")
        new_customer = existing_customer

    # Get business id
    business_id = db.query(Business).filter(and_(Business.identifier == business_identifier, Business.is_active == True)).first().id
    # Check if business exists or not
    if business_id is None:
        logger.error(BUSINESS_NOT_FOUND)
        return 404, {BUSINESS_NOT_FOUND}

    # Check if product already in cart
    product = db.query(Cart).filter(and_(Cart.product_id == product_id, Cart.customer_id == new_customer.id)).first()
    if product is not None:
        logger.error("Product already exist in cart")
        return 402, {"message": "Product already exist in cart"}

    # Create new cart item
    logger.info(f"Creating new cart item for customer with id: {new_customer.id}")
    new_item = Cart(
        business_id=business_id,
        customer_id=new_customer.id,
        product_id=product_id
    )

    # Save cart item
    logger.info("Saving new cart item")
    db.add(new_item)
    db.commit()

    return 201, {"message": "Cart item added"}

def get_user_item(db: Session, telegram_id: int):
    logger.info("Received request to get cart items for customer with telegram_id %s", telegram_id)

    # Step 1: Get Customer from Telegram ID
    customer = db.query(Customer).filter(Customer.telegram_id == telegram_id).first()

    # Check if Customer Exists
    if customer is None:
        logger.error("Could not get items for customer with telegram_id %s", telegram_id)
        return 404, {"message": "Customer not found"}

    # Step 2: Get Cart Items for the Customer
    logger.info("Querying cart items for customer ID %s", customer.id)
    cart_items = db.query(Cart).filter(Cart.customer_id == customer.id).all()

    if not cart_items:
        logger.info("No cart items found for customer ID %s", customer.id)
        return 404, {"message": "Your cart is empty. Add some products to your cart first!"}

    # Step 3: Extract Product IDs from Cart Items
    product_ids = [item.product_id for item in cart_items]

    # Step 4: Query Product Details for the Cart's Product IDs
    logger.info("Querying product details for product IDs %s", product_ids)
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()

    # Step 5: Create a Mapping of Product Details by Product ID
    product_details_map = {product.id: product for product in products}

    # Step 6: Prepare the Cart Response
    cart_response = []
    for item in cart_items:
        product = product_details_map.get(item.product_id)
        if product:
            cart_response.append({
                "cart_item_id": item.id,
                "product_id": product.id,
                "product_name": product.name,
                "product_description": product.description,
                "product_price": product.price,
                "product_image_url": product.image_url,
            })

    logger.info("Returning %d items in the cart for customer ID %s", len(cart_response), customer.id)
    return 200, {"cart": cart_response}

def remove_cart_item(db: Session, product_id: int, telegram_id: int):
    logger.info("Request to remove an item with product id: %s", product_id)

    # Step 1: Get Customer from Telegram ID
    customer = db.query(Customer).filter(Customer.telegram_id == telegram_id).first()

    # Check if Customer Exists
    if customer is None:
        logger.error("Could not get items for customer with telegram_id %s", telegram_id)
        return 404, {"message": "Customer not found"}

    # Step 2: Get the product in cart
    cart_item = db.query(Cart).filter(and_(Cart.product_id == product_id, Cart.customer_id == customer.id)).first()

    if cart_item is None:
        logger.error("Could not find cart item in cart with id")

    logger.info("Deleting found record")
    db.delete(cart_item)
    db.commit()

    logger.info("Deletion successful")
    return 200, {"message": "Deletion successful"}


def empty_cart_items(db: Session, telegram_id: int):
    logger.info("Received request to clear cart items for customer with telegram_id: %s", telegram_id)

    # Step 1: Get Customer from Telegram ID
    customer = db.query(Customer).filter(Customer.telegram_id == telegram_id).first()

    # Check if Customer Exists
    if customer is None:
        logger.error("Customer with telegram_id %s not found.", telegram_id)
        return 404, {"message": "Customer not found"}

    # Step 2: Delete all cart items for the customer
    logger.info("Attempting to clear cart items for customer ID: %s", customer.id)
    cart_items_deleted = db.query(Cart).filter(Cart.customer_id == customer.id).delete(synchronize_session=False)

    if cart_items_deleted == 0:
        logger.info("No cart items found for customer ID: %s", customer.id)
        return 200, {"message": "No cart items to clear"}

    # Commit the transaction
    db.commit()
    logger.info("Successfully cleared %d cart items for customer ID: %s", cart_items_deleted, customer.id)
    return 200, {"message": f"Successfully cleared {cart_items_deleted} items from the cart"}





