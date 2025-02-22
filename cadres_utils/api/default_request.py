import logging
import os
import time
from urllib.parse import urljoin

import pandas as pd
from pandas import DataFrame

from cadres_utils.api.exception import ApiException
from cadres_utils.api.wapi_invoker import WapiInvoker


async def process_default_list(
        api: WapiInvoker, object_name: str, filters: dict, columns: list[str], date_fields: list[str] | None = None,
        new_column_names: list[str] | None = None,
) -> DataFrame:
    start_time = time.perf_counter()
    # logging.debug(f'Fetching data {object_name}')
    response = await api.post_request(
        # urljoin(object_name, 'List'),
        os.path.join(object_name, 'List'),
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
                df[field] = df[field].apply(lambda x: pd.to_datetime(x, format='ISO8601') if pd.notnull(x) else None)
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
