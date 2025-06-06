import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import PyPDF2
from docx import Document
from pptx import Presentation
from langchain_core.tools import tool
from langchain.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool
from config.llm import ollama_chat_model
# ---------------------- TOOLS ----------------------

@tool("extract_text_from_pdf")
def extract_text_from_pdf(pdf_path: str) -> str:
    """Use this tool to extract text from a PDF file. Input is a string path to a .pdf file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text if text else "No extractable text found in PDF."
    except Exception as e:
        return f"Error extracting PDF: {e}"

@tool("extract_text_from_word")
def extract_text_from_word(word_path: str) -> str:
    """Use this tool to extract text from a Word (.docx) file. Input is a string path to a .docx file."""
    try:
        doc = Document(word_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text else "No text found in Word document."
    except Exception as e:
        return f"Error extracting Word: {e}"

@tool("extract_text_from_powerpoint")
def extract_text_from_powerpoint(ppt_path: str) -> str:
    """Use this tool to extract text from a PowerPoint (.pptx) file. Input is a string path to a .pptx file."""
    try:
        prs = Presentation(ppt_path)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text if text else "No text found in PowerPoint slides."
    except Exception as e:
        return f"Error extracting PowerPoint: {e}"

# ---------------------- AGENT SETUP ----------------------

def create_text_extraction_agent():
    """Create a ReAct agent for text extraction."""
    prompt = """
    You are a document assistant that extracts text from files.
    Use the appropriate tool to extract text from PDF, Word, or PowerPoint documents.
    Respond only with the text content extracted.
    """
    transfer_to_file_classification_agent = create_handoff_tool(
        agent_name="File Classification Agent",
        description="Transfer to File Classification Agent"
    )
    tools = [
        extract_text_from_pdf,
        extract_text_from_word,
        extract_text_from_powerpoint,
        transfer_to_file_classification_agent
    ]
    agent = create_react_agent(
        tools=tools,
        model=ollama_chat_model,
        prompt=prompt,
        name="Text Extraction Agent"
    )
    return agent

# ---------------------- RUN TEST ----------------------

if __name__ == "__main__":
    agent = create_text_extraction_agent()
    result = agent.invoke(
        {
            "messages": "Extract text from the file at path: D:/Project/Chatbot_CNM/data/Chain_of_thought.pdf"
        },
        config={"recursion_limit": 50}
    )

    # In toàn bộ message để debug nếu cần
    for msg in result["messages"]:
        print(msg.content)
