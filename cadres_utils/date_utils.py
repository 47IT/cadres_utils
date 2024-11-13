from datetime import date, datetime

import pandas as pd


def get_date_value(date_val) -> date:
    if isinstance(date_val, datetime):
        return date_val.date()
    return date_val


def date_to_api_str(input_date: date | pd.Timestamp, custom_date_format: str = None) -> str | None:
    if input_date and pd.notnull(input_date) and (isinstance(input_date, pd.Timestamp) or isinstance(input_date, datetime)):
        if custom_date_format:
            date_format = custom_date_format
        else:
            date_format = '%Y-%m-%d'
        return input_date.strftime(date_format)
    elif isinstance(input_date, str):
        return input_date
    return None
