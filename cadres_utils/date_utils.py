from datetime import date, datetime


def get_date_value(date_val) -> date:
    if isinstance(date_val, datetime):
        return date_val.date()
    return date_val

