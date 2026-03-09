import logging
import os
import posixpath
import time
from datetime import datetime

import polars as pl
from polars import DataFrame

from cadres_utils.api.exception import ApiException
from cadres_utils.api.wapi_invoker import WapiInvoker


async def process_auth(
    api: WapiInvoker, object_name: str, request_data: list[dict]
):
    response = await api.post_request(
        object_operation=f'{object_name}',
        request_body={
            'Request': {
                object_name: request_data,
            }
        },
        response_headers=True
    )

    return response


async def process_default_ins_mod(
    api: WapiInvoker,
    object_name: str,
    operation_name: str,
    request_data: list[dict],
    params: dict = None,
) -> dict:
    request_body = {'Request': {object_name: request_data}}
    if params:
        request_body['Params'] = params

    response = await api.post_request(
        object_operation=f'{object_name}/{operation_name}',
        request_body=request_body
    )

    return response


async def process_default_list(
        api: WapiInvoker, object_name: str, filters: dict, columns: list[str], date_fields: list[str] | None = None,
        new_column_names: list[str] | None = None,
        operation_name: str = 'List',
        sorts: list[str] | None = None,
        params: dict | None = None,
) -> DataFrame:
    start_time = time.perf_counter()
    req_url = posixpath.join(object_name, operation_name)
    request_body = {
        'Page': -1,
        'Sorts': sorts,
        'Columns': columns,
        'Filters': filters,
    }
    if params:
        request_body['Params'] = params

    response = await api.post_request(
        req_url,
        request_body,
    )
    if response['ResponseCode'] != '000':
        raise ApiException(
            f'Request error: ResponseCode: {response["ResponseCode"]}. ResponseTest: {response["ResponseText"]}'
        )

    if response['Response'][object_name]:
        df = pl.DataFrame(response['Response'][object_name])
    else:
        df = pl.DataFrame(schema={col: pl.String for col in columns})

    for element in columns:
        if element not in df.columns:
            df = df.with_columns(pl.lit(None, dtype=pl.String).alias(element))

    if new_column_names:
        df = df.rename(dict(zip(columns, new_column_names)))

    if not df.is_empty() and date_fields:
        for field in date_fields:
            try:
                df = df.with_columns(pl.col(field).str.to_datetime(format=None))
            except pl.exceptions.ComputeError:
                __process_date_error(df, field, object_name)
            except Exception as e:
                logging.error(f'Error in field {field} of {object_name}')
                raise e

    end_time = time.perf_counter()
    logging.debug(f'{object_name}/List ({response["ResponseId"]}) DONE: {(end_time - start_time):.1f}s')
    return df


def __process_default_list_from_cache(file_path: str):
    if os.path.exists(file_path):
        return pl.read_parquet(file_path)
    else:
        raise ApiException(f'File not found: {file_path}')


def __process_date_error(src_df: DataFrame, field: str, object_name: str):
    logging.error(f'Error in field {field} of {object_name}')
    tmp_df = src_df.clone()
    try:
        tmp_df = tmp_df.with_columns(
            pl.col(field).map_elements(
                lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S').date() if x is not None else None,
                return_dtype=pl.Date,
            ).alias(field)
        )
    except ValueError as e:
        logging.error(f'Error in field {field} of {object_name}. Error: {e}')
    filter_date = datetime.strptime('2500-01-01', '%Y-%m-%d').date()
    tmp_df = tmp_df.filter(pl.col(field) >= filter_date)
    select_cols = [field]
    if 'ID' in tmp_df.columns:
        select_cols.append('ID')
    tmp_df = tmp_df.select(select_cols)
    tmp_dic = tmp_df.to_dicts()

    raise ApiException(f'Error in field {field} of {object_name}. {tmp_dic}')


api_auth = process_auth
api_ins_mod = process_default_ins_mod
api_list = process_default_list
