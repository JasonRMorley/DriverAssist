import pandas as pd
from datetime import datetime
import json

class RosterRepository:
    def __init__(self):
        self.roster = pd.read_csv("Stagecoach_roster_38.csv")

    def get_line(self, number: str):
        return self.roster[self.roster["Line"] == number]

    def get_weeks(self, line_number: str, weeks: int):
        matches = self.roster.index[self.roster["Line"] == line_number].tolist()
        if not matches:
            raise ValueError(f"Line number {line_number} not found in roster")

        start_idx = matches[0]

        return self.roster.iloc[start_idx: start_idx + weeks]


class DutyRepository:
    def __init__(self):
        self.duties = pd.read_csv("duties_mon-wed.csv")

    def get_duty(self, duty_number):
        # normalise both sides to strings without leading zeros
        dn = str(duty_number).lstrip("0")
        return (
            self.duties[self.duties["Duty No."].astype(str).str.lstrip("0") == dn]
            .sort_values("Sign ON", ascending=True)  # earlier board first
        )

class DriverRepository:
    def __init__(self):

        try:
            self.driver_data = self.load_from_file()
        except:
            self.driver_data = None

    def load_from_file(self):
        with open("driver_data.json", "r") as f:
            loaded = json.load(f)
            loaded["previous_login_date"] = datetime.strptime(
                loaded["previous_login_date"], "%d/%m/%Y"
            ).date()
            loaded["current_login_date"] = datetime.strptime(
                loaded["current_login_date"], "%d/%m/%Y"
            ).date()
            self.driver_data = loaded
            print(f"loaded data: {loaded}")
            return loaded

    def save_to_file(self):

        with open("driver_data.json", "w") as f:
            json.dump(self.driver_data, f, indent=4)
            print(f"data saved to file: {self.driver_data}")
