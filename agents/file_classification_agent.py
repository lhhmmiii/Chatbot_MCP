import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.llm import ollama_chat_model, ollama_model
from config.prompt_template import file_classification_template
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool


@tool
def classify_file_tool(file_content: str) -> str:
    """Classify the type or category of a file based on its name and content."""
    prompt = PromptTemplate(
        template=file_classification_template,
        input_variables=["file_content"]
    )
    chain = prompt | ollama_model | StrOutputParser()
    result = chain.invoke({"file_content": file_content})
    return result


def create_file_classification_agent():
    transfer_to_metadata_agent = create_handoff_tool(
        agent_name="Metadata Agent",
        description="Transfer to Metadata Agent"
    )
    prompt = "Bạn là một tác nhân chuyên phân loại các tập tin dựa trên nội dung của chúng\
    Chỉ đưa ra kết quả phân loại, không đưa ra bất kỳ lời giải thích nào."
    agent = create_react_agent(
        model=ollama_chat_model,
        tools=[classify_file_tool, transfer_to_metadata_agent],
        prompt=prompt,
        name="File Classification Agent"
    )
    return agent

if __name__ == "__main__":
    agent = create_file_classification_agent()
    result = agent.invoke(
        {
            "messages": "Phân loại tệp theo nội dung: Đây là tài liệu về chuỗi suy nghĩ."
        },
        config={"recursion_limit": 50}  
    )
    for message in result["messages"]:
        print(message.content)


