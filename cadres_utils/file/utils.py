import io
import zipfile
from dataclasses import dataclass
import os
import random
import string


@dataclass
class FileElement:
    file_name: str
    stream: io.BytesIO


def create_all_files_zip(file_list: list[FileElement]) -> io.BytesIO:
    # Create a new BytesIO object to store the ZIP file
    zip_buffer = io.BytesIO()

    saved_file_map = {}

    # Create a ZIP file
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        # Add each Excel file to the ZIP
        for single_file in file_list:
            save_file_name = single_file.file_name
            if save_file_name in saved_file_map:
                file_cnt = saved_file_map[save_file_name]
                file_cnt += 1
                saved_file_map[save_file_name] = file_cnt
                save_file_name = f"{os.path.splitext(single_file.file_name)[0]}_{file_cnt}{os.path.splitext(single_file.file_name)[1]}"
            else:
                saved_file_map[save_file_name] = 1
            # Reset the file pointer to the beginning
            excel_bytesio = single_file.stream
            excel_bytesio.seek(0)
            # Write the Excel file to the ZIP
            zip_file.writestr(save_file_name, excel_bytesio.getvalue())

    # Reset the file pointer to the beginning
    zip_buffer.seek(0)

    return zip_buffer


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))

    return result_str


def zip_io_streams(io_streams: dict[str, io.BytesIO]) -> io.BytesIO:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, io_stream in io_streams.items():
            zip_file.writestr(file_name, io_stream.getvalue())

    zip_buffer.seek(0)
    return zip_buffer


def get_file_list(base_file_path: str, base_file_name: str | None = None) -> list[str]:
    return [os.path.join(base_file_path, f) for f in os.listdir(base_file_path) if is_file_for_proc(base_file_path, f, base_file_name)]


def is_file_for_proc(base_file_path, file_name: str, base_file_name: str) -> bool:
    res = os.path.isfile(os.path.join(base_file_path, file_name))
    if base_file_name:
        res = res and (base_file_name in file_name)
    # res = res and 'попередні_періоди_служби' in file_name
    res = res and file_name[0] not in ['.', '~']
    res = res and file_name.endswith('.xlsx')

    return res
