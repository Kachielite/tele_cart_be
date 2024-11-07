from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    RETURNED = "returned"
    EXCHANGED = "exchanged"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    FAILED = "failed"
    UNKNOWN = "unknown"