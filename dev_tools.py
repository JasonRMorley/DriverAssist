from services import DriverService
from repository import *
from flask import redirect, url_for
from functools import wraps

def get_driver_service():
    driver_repository = DriverRepository()
    roster_repository = RosterRepository()
    duty_repository = DutyRepository()
    driver_service = DriverService(driver_repository=driver_repository,
                                   roster_repository=roster_repository,
                                   duty_repository=duty_repository
                                   )
    return driver_service


def driver_handle():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            service = get_driver_service()
            if service.driver_repository.driver_data is None:
                return redirect(url_for("setup_driver"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
