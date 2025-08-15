from dataclasses import dataclass
from typing import List
from pandas._typing import DtypeArg


@dataclass(frozen=True, slots=True)
class ExcelDataSource:
    file_path: str
    sheet_name: str | int
    fields: List[str] | str = None
    new_column_names: List[str] = None
    date_fields_to_convert: List[str] = None
    not_prepare_str_fields: List[str] = None
    skip_rows: int = None
    error_on_invalid_date: bool = False
    dtype: DtypeArg | None = None
