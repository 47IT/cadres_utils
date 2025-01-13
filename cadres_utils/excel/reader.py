from datetime import datetime

import pandas as pd
from pandas import DataFrame

from cadres_utils.excel.excel_data_source import ExcelDataSource


def proc_date_field_default(x):
    return __proc_date_field_internal(x)

def proc_date_field_with_validation(x):
    return __proc_date_field_internal(x, is_error_on_bad_date_format=True)

def __proc_date_field_internal(x, is_error_on_bad_date_format: bool = False):
    if isinstance(x, (int, float)):
        try:
            val = pd.to_datetime(x, origin='1899-12-30', unit='D')
        except ValueError:
            val = None
        return val
    elif isinstance(x, (pd.Timestamp, datetime)):
        return x
    elif isinstance(x, str):
        if pd.isnull(x):
            return None
        translation_table = str.maketrans(',ю/Ю\\', '.....')
        new_string = x.translate(translation_table)
        lst = new_string.split('.')
        if len(lst) == 3:
            try:
                lst = [int(i) for i in lst]
                if lst[1] > 12 >= lst[0]:
                    date_str = f'{lst[1]}.{lst[0]}.{lst[2]}'
                elif lst[0] > 12 >= lst[1]:
                    date_str = f'{lst[0]}.{lst[1]}.{lst[2]}'
                elif '.' in x:  # якщо дата була без точок, то не зрозуміло що з них місяць, а що день
                    date_str = x
                else:
                    date_str = ''

                if date_str:
                    return pd.to_datetime(date_str, format='%d.%m.%Y')
                else:
                    return None
            except ValueError:
                if is_error_on_bad_date_format:
                    raise ValueError(f'Bad date format: {x}')
                else:
                    return None
        else:
            if is_error_on_bad_date_format:
                raise ValueError(f'Bad date format: {x}')
            else:
                return None
    else:
        return None


def read_data_from_excel(source: ExcelDataSource) -> DataFrame:
    skip_rows_val = None
    if source.skip_rows:
        skip_rows_val = source.skip_rows

    # noinspection PyTypeChecker
    df = pd.read_excel(
        source.file_path,
        sheet_name=source.sheet_name,
        usecols=source.fields,
        skiprows=skip_rows_val,
    )

    if source.new_column_names:
        if isinstance(source.fields, list):
            src_lst = source.fields
        else:
            src_lst = df.columns
        df.rename(columns=dict(zip(src_lst, source.new_column_names)), inplace=True)
    if source.date_fields_to_convert:
        for field in source.date_fields_to_convert:
            if source.error_on_invalid_date:
                df[field] = df[field].apply(proc_date_field_with_validation)
            else:
                df[field] = df[field].apply(proc_date_field_default)

    df_obj = df.select_dtypes(['object'])
    if source.not_prepare_str_fields:
        for col in df_obj.columns:
            if col not in source.not_prepare_str_fields:
                df[col] = df[col].str.strip()
    else:
        for col in df_obj.columns:
            df[col] = df_obj[col].apply(lambda x: x.strip() if pd.notnull(x) and isinstance(x, str) else x)
    # df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip() if pd.notnull(x) else x)

    return df
