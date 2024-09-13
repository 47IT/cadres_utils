import io
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