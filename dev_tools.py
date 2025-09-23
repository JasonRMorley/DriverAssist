from services import DriverService
from repository import *


def get_driver_service():
    driver_repository = DriverRepository()
    roster_repository = RosterRepository()
    duty_repository = DutyRepository()
    driver_service = DriverService(driver_repository=driver_repository,
                                   roster_repository=roster_repository,
                                   duty_repository=duty_repository
                                   )
    return driver_service
