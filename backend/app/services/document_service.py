import os
import shutil
from fastapi import UploadFile

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))

class DocumentService:
    @staticmethod
    async def save_upload(file: UploadFile) -> str:
        """
        Saves the uploaded file to the data storage folder and returns the filepath.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        file_path = os.path.join(DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    @staticmethod
    def read_file_bytes(file_path: str) -> bytes:
        """
        Reads raw binary content of a file.
        """
        with open(file_path, "rb") as f:
            return f.read()
