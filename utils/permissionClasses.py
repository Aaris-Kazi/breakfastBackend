from utils.permissions import HasRole


class IsAdmin(HasRole):
    allowed_roles = ["ADMIN"]


class IsCustomer(HasRole):
    allowed_roles = ["CUSTOMER"]


class IsDeliveryAgent(HasRole):
    allowed_roles = ["DELIVERY_AGENT"]


class IsManager(HasRole):
    allowed_roles = ["MANAGER"]