import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from datetime import datetime
from utils import _format_file_timestamp
from langgraph.prebuilt import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from config.llm import ollama_chat_model

@tool
def create_metadata(text: str, file_name: str, label: str):
    """
    Create a metadata dictionary for a given text document.

    Args:
        text (str): The content of the document.
        file_name (str): The name of the file.
        label (str): A label categorizing the document.

    Returns:
        dict: A dictionary containing metadata such as total characters, creation date, file name, and label.
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

@tool
def save_metadata_to_xlsx(metadata: dict, xlsx_file_name: str, folder_dir: str = "Metadata"):
    """
    Save metadata to an Excel (.xlsx) file.

    Args:
        metadata (dict): The metadata dictionary to be saved.
        xlsx_file_name (str): The name of the Excel file to save the metadata.
        folder_dir (str, optional): The directory where the Excel file will be saved. Defaults to "Metadata".

    Returns:
        str: The path to the saved Excel file.
    """
    df = pd.DataFrame([metadata])
    path = os.path.join(folder_dir, xlsx_file_name)
    df.to_excel(path, index=False, engine='openpyxl')
    return path

def create_metadata_agent():
    """
    Create an agent for generating metadata for a given text document.
    """
    prompt = "You are an agent specialized in creating metadata for documents. Use the provided information to\
    generate metadata."
    agent = create_react_agent(
        tools=[create_metadata],
        model=ollama_chat_model,
        prompt=prompt,
        name="Metadata Agent"
    )
    return agent

def save_metadata_to_xlsx_agent():
    """
    Create an agent for saving metadata to an .xlsx file.
    """


    prompt = "You are an agent specialized in saving metadata to an .xlsx file. Use the provided metadata to create the file."

    agent = create_react_agent(
        tools=[save_metadata_to_xlsx],
        model=ollama_chat_model,
        prompt=prompt,
        name="Save Metadata to XLSX Agent"
    )
    return agent


if __name__ == "__main__":
    metadata_agent = save_metadata_to_xlsx_agent()
    result = metadata_agent.invoke(
        {
            "messages": (
                "Please export the Excel file containing the following metadata:\n"
                "- File Name: Chain_of_thought.pdf\n"
                "- Label: Chain of Thought\n"
                "- Text: This is a document about the chain of thought. The document is a PDF file."
                "And the file name to save is Chain_of_thought.xlsx"
            )
        },
        config={"recursion_limit": 50}
    )
    for message in result["messages"]:
        print(message.content)
