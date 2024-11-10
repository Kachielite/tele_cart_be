import logging
from typing import List

from sqlalchemy import and_, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.enums.order_status import OrderStatus
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.models.order_item import OrderItems
from app.schemas.order import OrderRequest, ProductList

NO_ACCESS = "Business does not have access to order"
NOT_FOUND = "Order not found"

logger = logging.getLogger(__name__)

def calculate_total(products: List[ProductList]) -> float:
    return sum(product.quantity * product.price for product in products)

def create_order(db: Session, business_id: int, order: OrderRequest):
    global new_customer
    logger.info("Creating order with the following details: %s %s %s %s %s", order.customer_name, order.customer_phone_number, order.customer_address, order.customer_telegram_id, order.products)

    try:
        # Check if customer exists
        existing_customer = db.query(Customer).filter(Customer.phone_number == order.customer_phone_number).first()

        if existing_customer is None:
            logger.info("Creating new customer")
            new_customer = Customer(
                name=order.customer_name,
                phone_number=order.customer_phone_number,
                address=order.customer_address,
                telegram_id=order.customer_telegram_id,
            )
            db.add(new_customer)
            db.flush()  # Ensures `new_customer.id` is available for new_order
        else:
            new_customer = existing_customer

        logger.info("Creating new order")
        new_order = Order(
            customers_id=new_customer.id,
            businesses_id=business_id,
            total=calculate_total(order.products),
            status=OrderStatus.pending
        )
        db.add(new_order)
        db.flush()  # Ensures `new_order.id` is available for order items

        logger.info("Adding products to the order item table")
        for product in order.products:
            db.execute(
                text(
                    """
                    INSERT INTO order_items (orders_id, products_id, quantity)
                    VALUES (:orders_id, :products_id, :quantity)
                    """
                ),
                {"orders_id": new_order.id, "products_id": product.id, "quantity": product.quantity}
            )

        db.commit()
        logger.info("Order created successfully")
        return 201, {"message": "Order created successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating order: {str(e)}")
        return 500, {"message": "An error occurred while creating the order"}
    finally:
        db.close()


# Fetch all orders
def fetch_orders(db: Session, business_id: int, page: int, page_size: int):
    logger.info("Fetching all orders for business_id: %s", business_id)
    offset = (page - 1) * page_size
    fetched_orders = db.query(Order).filter(Order.businesses_id == business_id).offset(offset).limit(page_size).all()

    orders = [{
        "id": order.id,
        "customer": db.query(Customer).filter(Customer.id == order.customers_id).first().name,
        "products": [{
            "id": product.products_id,
            "name": db.query(Product).filter(Product.id == product.products_id).first().name,
            "quantity": product.quantity,
            "price": db.query(Product).filter(Product.id == product.products_id).first().price,
        } for product in db.query(OrderItems).filter(OrderItems.orders_id == order.id).all()],
        "total": order.total,
        "status": order.status,
        "created_at": order.created_at.isoformat(timespec='milliseconds') + 'Z',
        "updated_at": order.updated_at.isoformat(timespec='milliseconds') + 'Z',
    } for order in fetched_orders]

    logger.info("Orders fetched successfully")
    return 200, orders

# Fetch order by id
def fetch_order_by_id(db: Session, order_id: int, business_id: int):
    logger.info("Fetching order details for order_id: %s", order_id)
    order = db.query(Order).filter(Order.id == order_id).first()

    if order.businesses_id != business_id:
        logger.error(NO_ACCESS)
        return 403, {"message": NO_ACCESS}

    if order is None:
        logger.error(NOT_FOUND)
        return 404, {"message": NOT_FOUND}

    fetched_order = {
        "id": order.id,
        "customer": db.query(Customer).filter(Customer.id == order.customers_id).first().name,
        "products": [{
            "id": product.products_id,
            "name": db.query(Product).filter(Product.id == product.products_id).first().name,
            "quantity": product.quantity,
            "price": db.query(Product).filter(Product.id == product.products_id).first().price,
        } for product in db.query(OrderItems).filter(OrderItems.orders_id == order.id).all()],
        "total": order.total,
        "status": order.status,
        "created_at": order.created_at.isoformat(timespec='milliseconds') + 'Z',
        "updated_at": order.updated_at.isoformat(timespec='milliseconds') + 'Z',
    }

    logger.info("Order details fetched successfully")
    return 200, fetched_order

# Update order status
def update_order_status(db: Session, order_id: int, status: OrderStatus, business_id: int):
    logger.info("Updating order status for order_id: %s", order_id)
    order = db.query(Order).filter(Order.id == order_id).first()

    if order.businesses_id != business_id:
        logger.error(NO_ACCESS)
        return 403, {"message": NO_ACCESS}

    if order is None:
        logger.error(NOT_FOUND)
        return 404, {"message": NOT_FOUND}

    order.status = status
    db.commit()

    logger.info("Order status updated successfully")
    return 200, {"message": "Order status updated successfully"}


# Retrieve Customer Orders
def fetch_customer_orders(db: Session, customer_id: int, business_id: int, page: int = 1, page_size: int = 10):
    logger.info("Fetching all orders for customer_id: %s", customer_id)
    offset = (page - 1) * page_size
    fetched_orders = db.query(Order).filter(and_(Order.customers_id == customer_id, Order.businesses_id == business_id)).offset(offset).limit(page_size).all()

    orders = [{
        "id": order.id,
        "customer": db.query(Customer).filter(Customer.id == order.customers_id).first().name,
        "products": [{
            "id": product.products_id,
            "name": db.query(Product).filter(Product.id == product.products_id).first().name,
            "quantity": product.quantity,
            "price": db.query(Product).filter(Product.id == product.products_id).first().price,
        } for product in db.query(OrderItems).filter(OrderItems.orders_id == order.id).all()],
        "total": order.total,
        "status": order.status,
        "created_at": order.created_at.isoformat(timespec='milliseconds') + 'Z',
        "updated_at": order.updated_at.isoformat(timespec='milliseconds') + 'Z',
    } for order in fetched_orders]

    logger.info("Orders fetched successfully")
    return 200, orders









