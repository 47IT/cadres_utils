from datetime import datetime

import pandas as pd
from numpy import int64

VIEW_DATE_FORMAT = '%d.%m.%Y'
SERVER_DATE_FORMAT = '%Y-%m-%d'


def get_field_value(curr_row, field_name, is_float_to_int: bool = False, custom_date_format: str = None):
    if pd.notnull(curr_row[field_name]):
        if isinstance(curr_row[field_name], (datetime, pd.Timestamp)):
            date_format = '%d.%m.%Y'
            if custom_date_format:
                date_format = custom_date_format
            return date_to_str(curr_row[field_name], date_format)
        elif isinstance(curr_row[field_name], int64):
            return str(curr_row[field_name])
        elif is_float_to_int and isinstance(curr_row[field_name], float):
            return str(int(curr_row[field_name]))
        return curr_row[field_name]
    else:
        return None


def date_to_str(date: pd.Timestamp, date_format: str = '%d.%m.%Y') -> str | None:
    if date and pd.notnull(date) and (isinstance(date, pd.Timestamp) or isinstance(date, datetime)):
        return date.strftime(date_format)
    elif isinstance(date, str):
        return date
    return None
