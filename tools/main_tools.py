import easyocr
from logger import app_logger
from config import Config
from base_response import error_response
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import fitz  # PyMuPDF
import asyncio
from LLM import call_llm
import numpy as np
import cv2

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
            ("system", """Bersihkan dan beri beberapa paragraf untuk melihat CV nya, dan deskripsikan tentang CV nya. CV ada di text OCR, ouput Markdown"""),
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
    
def pdf_converter(pdf_byte):
    try:
        # Buka PDF dari bytes
        doc = fitz.open(stream=pdf_byte, filetype="pdf")
        all_images = [] # Gunakan list untuk menampung gambar dari SEMUA halaman

        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(dpi=150) 
            
            # Ubah raw data ke numpy array
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            
            # Konversi semua format warna ke BGR (standar OpenCV yang diharapkan EasyOCR)
            if pix.n == 4: # RGBA
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            elif pix.n == 3: # RGB (Paling sering muncul)
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            elif pix.n == 1: # Grayscale
                img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
            
            # Tambahkan gambar halaman ini ke dalam list, JANGAN di-return dulu
            all_images.append(img_array)
            
        # Setelah semua halaman selesai diproses, kembalikan list-nya
        return all_images
        
    except Exception as e:
        app_logger.error(message=f"Error:{e}")
        return error_response(message=f"Error:{e}")