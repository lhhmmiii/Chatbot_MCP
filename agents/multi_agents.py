import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph_swarm import create_swarm, create_handoff_tool
from file_classification_agent import create_file_classification_agent
from text_extraction_agent import create_text_extraction_agent
from document_search_agent import create_document_search_agent
from metadata_agent import create_metadata_agent, save_metadata_to_xlsx_agent
from langgraph.graph import StateGraph, START, MessagesState

async def main():
    # Agent
    document_search_agent = await create_document_search_agent()
    text_extraction_agent = create_text_extraction_agent()
    file_classification_agent = create_file_classification_agent()
    metadata_agent = create_metadata_agent()
    save_metadata_agent = save_metadata_to_xlsx_agent()

    # Define multi-agent graph
    multi_agent_graph = (
        StateGraph(MessagesState)
        .add_node("text_extraction_agent", text_extraction_agent)
        .add_node("file_classification_agent", file_classification_agent)
        .add_node("metadata_agent", metadata_agent)
        .add_node("save_metadata_agent", save_metadata_agent)
        .add_edge(START, "text_extraction_agent")
        .add_edge("text_extraction_agent", "file_classification_agent")
        .add_edge("file_classification_agent", "metadata_agent")
        .add_edge("metadata_agent", "save_metadata_agent")
        .compile()
    )


    # Run the multi-agent graph
    print(1111111111111111111111111)
    for chunk in multi_agent_graph.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Extract text from the file at path: D:/Project/Chatbot_CNM/data/Chain_of_thought.pdf\
                                and export metadata to xlsx file"
                }
            ]
        }
    ):
        print(chunk)
        print("\n")
    print(2222222222222222222222222)
            
if __name__ == "__main__":
    asyncio.run(main())
    

    


    

if __name__ == "__main__":
    asyncio.run(main())
