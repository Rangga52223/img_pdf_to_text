import easyocr
from logger import app_logger
from config import Config
from base_response import error_response
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from LLM import call_llm

ocr_reader = easyocr.Reader(['id', 'en'], gpu=False)
#document_reader
def read_document(docs):
    try:
        return [res[1] for res in ocr_reader.readtext(docs)]
    except Exception as e:
        print(f"Error OCR: {e}")
        return None
#llm Reader
def llm_reader(raw_text):
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Berikan Informasi Apapun dari hasil OCR mentah dan harus berdasarkan data ocr_mentah nya."""),
            ("human", "Teks OCR Mentah:\n{raw_ocr_text}")
        ])
        parser = StrOutputParser()
        ocr_cleaning_chain = prompt | call_llm.llm | parser
        clean_info = ocr_cleaning_chain.invoke({
        "raw_ocr_text": raw_text
    })
        return clean_info
    
    except Exception as e:
        app_logger.critical(f"Error:{e}")
        return error_response(f"Error:{e}")
         