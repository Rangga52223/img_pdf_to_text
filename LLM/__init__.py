from langchain_openai import ChatOpenAI
from config import Config
class call_llm:
    llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=str(Config.AI_CONF), 
    model_name="meta-llama/llama-3.1-8b-instruct", # Bisa diganti model gratis lainnya
    temperature=0.1, # Bagus untuk agent/RAG agar jawabannya faktual
    max_tokens=500
)