import io
import zipfile
from dataclasses import dataclass


@dataclass
class FileElement:
    file_name: str
    stream: io.BytesIO


def create_all_files_zip(file_list: list[FileElement]) -> io.BytesIO:
    # Create a new BytesIO object to store the ZIP file
    zip_buffer = io.BytesIO()

    # Create a ZIP file
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        # Add each Excel file to the ZIP
        for single_file in file_list:
            # Reset the file pointer to the beginning
            excel_bytesio = single_file.stream
            excel_bytesio.seek(0)
            # Write the Excel file to the ZIP
            zip_file.writestr(single_file.file_name, excel_bytesio.getvalue())

    # Reset the file pointer to the beginning
    zip_buffer.seek(0)

    return zip_buffer