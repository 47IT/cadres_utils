from cadres_utils.api.default_request import process_default_list
from cadres_utils.api.wapi_invoker import WapiInvoker
from cadres_utils.field_utils import get_field_value


async def get_config_params(api: WapiInvoker, param_list: list) -> dict:
    df = await process_default_list(
        api=api,
        object_name='App_CadresIni',
        filters={'Variable': param_list},
        columns=['Variable', 'Value'],
    )

    res = {}
    for _, row in df.iterrows():
        variable = get_field_value(row, 'Variable')
        value = get_field_value(row, 'Value')
        res[variable] = value

    return res