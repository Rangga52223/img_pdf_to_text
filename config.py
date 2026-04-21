from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    LANGUAGE_CONF=os.getenv("L_LIST")
    AI_CONF=os.getenv("API_LLM")