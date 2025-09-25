from datetime import date, timedelta
from repository import *


class DriverService:
    def __init__(self, driver_repository, roster_repository, duty_repository):
        self.roster_repository = roster_repository
        self.driver_repository = driver_repository
        self.duty_repository = duty_repository
        self.date_today = date.today()
        if self.driver_repository.driver_data is not None:
            if self.driver_repository.driver_data["previous_login_date"] != self.driver_repository.driver_data[
                    "current_login_date"]:
                self.auto_update_line_number()

    def get_driver_details_from_file(self) -> dict:
        return self.driver_repository.load_from_file()

    def update_line_number(self, line_number: str):
        self.driver_repository.driver_data["line_number"] = line_number
        self.driver_repository.save_to_file()
        return

    def retrieve_roster_weeks(self, weeks: int):
        line_number = self.driver_repository.driver_data["line_number"]
        return self.roster_repository.get_weeks(line_number=line_number, weeks=weeks)

    def get_line_from_date(self, today_date: date, target_date: date, current_line: str) -> str:
        delta = today_date - target_date
        weeks_passed = delta.days // 7

        return str(int(current_line) - weeks_passed).zfill(len(current_line))

    def calculate_time_passed(self, check_date: date):
        if check_date.weekday() == 6:
            return check_date
        else:
            days_since_sunday = check_date.weekday() + 1
            return check_date - timedelta(days=days_since_sunday)

    def retrieve_line_from_date(self, target_date):
        target_date = self.calculate_time_passed(target_date)
        line_number = self.driver_repository.driver_data["line_number"]
        check_line = self.get_line_from_date(today_date=self.date_today,
                                             target_date=target_date,
                                             current_line=line_number
                                             )
        return self.roster_repository.get_line(check_line)

    def retrieve_duty(self, duty_number: str):
        return self.duty_repository.get_duty(duty_number=duty_number)

    def auto_update_line_number(self):
        previous_login_date = self.driver_repository.driver_data["previous_login_date"]

        line_df = self.retrieve_line_from_date(previous_login_date)
        if line_df.empty:
            raise ValueError(f"No line found for date {previous_login_date}")

        # get the first match from the DataFrame
        new_line_number = line_df["Line"].iloc[0]

        # update driver data
        self.driver_repository.driver_data["line_number"] = new_line_number
        self.driver_repository.driver_data["previous_login_date"] = self.date_today

        print(f"line number updated to {new_line_number}")
        print(f"drivers previous login set to: {self.date_today}")

    def setup_new_driver(self, name, number, line_number):
        previous_login_date = current_login_date = self.date_today.strftime("%d/%m/%Y")
        self.driver_repository.driver_data = {
            "line_number": line_number,
            "previous_login_date": previous_login_date,
            "current_login_date": current_login_date,
            "driver_name": name,
            "driver_number": number
        }
        self.driver_repository.save_to_file()
