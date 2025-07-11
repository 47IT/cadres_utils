import io
import os
import random
import string
import zipfile


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
