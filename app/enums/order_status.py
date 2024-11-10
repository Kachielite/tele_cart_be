from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"
    completed = "completed"
    refunded = "refunded"
    returned = "returned"
    exchanged = "exchanged"
    shipped = "shipped"
    delivered = "delivered"
    failed = "failed"
    unknown = "unknown"