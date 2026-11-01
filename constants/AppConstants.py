from enum import Enum
from utils import Configurations
from .AppEnums import AppEnums


class AppConstants(Enum):
    DEFAULT_DELIVERY_FEE = Configurations.get_configurations("DEFAULT_DELIVERY_FEE", AppEnums.DEFAULT_DELIVERY_FEE)