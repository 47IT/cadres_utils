import logging
import os
import posixpath
import time
from datetime import datetime

import pandas as pd
from pandas import DataFrame
from pandas._libs import OutOfBoundsDatetime

from cadres_utils.api.exception import ApiException
from cadres_utils.api.wapi_invoker import WapiInvoker


async def process_default_list(
        api: WapiInvoker, object_name: str, filters: dict, columns: list[str], date_fields: list[str] | None = None,
        new_column_names: list[str] | None = None,
) -> DataFrame:
    start_time = time.perf_counter()
    req_url = posixpath.join(object_name, 'List')
    response = await api.post_request(
        req_url,
        {
            'Page': -1,
            'Columns': columns,
            'Filters': filters,
        }
    )
    if response['ResponseCode'] != '000':
        raise ApiException(
            f'Request error: ResponseCode: {response["ResponseCode"]}. ResponseTest: {response["ResponseText"]}'
        )

    if response['Response'][object_name]:
        df = DataFrame(response['Response'][object_name])
    else:
        df = DataFrame(columns=columns)

    for element in columns:
        if element not in df.columns:
            df[element] = None

    if new_column_names:
        df.rename(columns=dict(zip(columns, new_column_names)), inplace=True)

    if not df.empty and date_fields:
        for field in date_fields:
            try:
                df[field] = pd.to_datetime(df[field], format='ISO8601')
                # df[field] = df[field].apply(lambda x: pd.to_datetime(x, format='ISO8601') if pd.notnull(x) else None)
                # df[field] = pd.to_datetime(df[field], format='ISO8601', errors='coerce')
            except OutOfBoundsDatetime:
                __process_date_error(df, field, object_name)
            except Exception as e:
                logging.error(f'Error in field {field} of {object_name}')
                raise e

    end_time = time.perf_counter()
    logging.debug(f'Finish fetching data {object_name} - work time: {end_time - start_time} sec')
    return df


def __process_default_list_from_cache(file_path: str):
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    else:
        raise ApiException(f'File not found: {file_path}')


def __process_date_error(src_df: DataFrame, field: str, object_name: str):
    logging.error(f'Error in field {field} of {object_name}')
    tmp_df = src_df.copy()
    try:
        tmp_df[field] = tmp_df[field].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S').date() if pd.notnull(x) else None)
    except ValueError as e:
        logging.error(f'Error in field {field} of {object_name}. Error: {e}')
    filter_date = datetime.strptime('2500-01-01', '%Y-%m-%d').date()
    tmp_df = tmp_df[tmp_df[field] >= filter_date]
    columns = [field]
    if 'ID' in tmp_df.columns:
        columns.append('ID')
    tmp_df = tmp_df[columns]
    tmp_dic = tmp_df.to_dict(orient='records')

    raise ApiException(f'Error in field {field} of {object_name}. {tmp_dic}')
