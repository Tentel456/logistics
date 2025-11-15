from enum import Enum

class VehicleType(str, Enum):
    van = "van"
    truck = "truck"
    bike = "bike"
    foot = "foot"

class OrderStatus(str, Enum):
    created = "created"
    assigned = "assigned"
    in_transit = "in_transit"
    delivered = "delivered"
    failed = "failed"
