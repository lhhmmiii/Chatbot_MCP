from config.llm import ollama_model
from config.prompt_template import file_classification_template
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import asyncio


async def classify_file(file_name: str, file_content: str) -> str:
    prompt = PromptTemplate(template = file_classification_template, input_variables = ["filename", "file_content"])
    chain = prompt | ollama_model | StrOutputParser()
    text = chain.invoke({"filename": file_name, "file_content": file_content})
    return text


if __name__ == "__main__":
    file_name = "test.txt"
    file_content = "This is a test file."
    print(asyncio.run(classify_file(file_name, file_content)))







