from datetime import datetime
import pandas as pd

def _format_file_timestamp(timestamp: float, include_time: bool = False):
    """
    Format file timestamp to a %Y-%m-%d string.

    Args:
        timestamp (float): timestamp in float
        include_time (bool): whether to include time in the formatted string

    Returns:
        str: formatted timestamp
    """
    try:
        if include_time:
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except Exception:
        return None

def create_metadata(text: str, file_name: str, label: str):
    """
    Create metadata for a given text document.

    Args:
        text (str): The content of the document.
        file_name (str): The name of the file.
        label (str): A label or category for the document.

    Returns:
        dict: A dictionary containing metadata about the document, including
              total characters, creation date, file name, and label.
    """
    metadata = {
        "total_characters": len(text),
        "creation_date": _format_file_timestamp(
            timestamp=datetime.now().timestamp(), include_time=True
        ),
        "file_name": str(file_name),
        "label": label,
    }
    return metadata

def save_metadata_to_xlsx(metadata: dict, xlsx_file_name: str):
    """
    Save metadata to an .xlsx file using pandas and openpyxl.

    Args:
        metadata (dict): The metadata dictionary to save.
        xlsx_file_name (str): The name of the .xlsx file to create.

    Returns:
        str: The path to the created .xlsx file.
    """
    df = pd.DataFrame([metadata])
    df.to_excel(xlsx_file_name, index=False, engine='openpyxl')
    return xlsx_file_name

if __name__ == "__main__":
    metadata = create_metadata("Hello, world!", "test.txt", "test")
    save_metadata_to_xlsx(metadata, "test.xlsx")
