import os
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.llms import OllamaLLM 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


ollama_chat_model = ChatOllama(model="llama3.2")
ollama_model = OllamaLLM(model="llama3.2")
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)