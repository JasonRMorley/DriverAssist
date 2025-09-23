import pandas as pd
from datetime import date

roster = pd.read_csv("Stagecoach_roster_38.csv")
duties = pd.read_csv("duties_mon-wed.csv")

def get_column(columns: [str]):
    return roster[columns]


def get_line(line_number: str):
    return roster[roster["Line"] == line_number]


def get_weeks(line_number: str, weeks: int):
    # locate the index of the row with this line number
    start_idx = roster.index[roster["Line"] == line_number].tolist()

    start_idx = start_idx[0]

    # slice from that index forward
    return roster.iloc[start_idx: start_idx + weeks]


def get_line_from_date(today_date: date, target_date, current_line: str) -> str:
    delta = today_date - target_date
    weeks_passed = delta.days // 7
    return str(int(current_line) - weeks_passed)

def get_duty(duty_number):
    # normalise both sides to strings without leading zeros
    dn = str(duty_number).lstrip("0")
    return (
        duties[duties["Duty No."].astype(str).str.lstrip("0") == dn]
        .sort_values("Sign ON", ascending=True)  # earlier board first
    )
