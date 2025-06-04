from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.llms import OllamaLLM 

ollama_chat_model = ChatOllama(model="llama3.2")
ollama_model = OllamaLLM(model="llama3.2")