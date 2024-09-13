from datetime import datetime

import pandas as pd
from numpy import int64


def get_field_value(curr_row, field_name, is_float_to_int: bool = False):
    if pd.notnull(curr_row[field_name]):
        if isinstance(curr_row[field_name], (datetime, pd.Timestamp)):
            return date_to_str(curr_row[field_name])
        elif isinstance(curr_row[field_name], int64):
            return str(curr_row[field_name])
        elif is_float_to_int and isinstance(curr_row[field_name], float):
            return str(int(curr_row[field_name]))
        return curr_row[field_name]
    else:
        return None


def date_to_str(date: pd.Timestamp) -> str | None:
    if date and pd.notnull(date) and (isinstance(date, pd.Timestamp) or isinstance(date, datetime)):
        return date.strftime('%d.%m.%Y')
    elif isinstance(date, str):
        return date
    return None
