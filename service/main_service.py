from tools.main_tools import read_document, llm_reader
from pdf2image import convert_from_bytes
from base_response import succes_response, error_response
from logger import app_logger
import numpy as np

#MAIN_Process
def ocr_process(docs):
    try:
        print("Debug_old_process")
        data = read_document(docs)
        clean_text = [result[1] for result in data]
        return succes_response(message="OCR Berhasil", data=clean_text)
    except Exception as e:
        return error_response(message=e)

#Read PDF Service     
def main_service_img_process_pdf(docs):
    try:
        app_logger.info("data_masuk_pdf")
        images = convert_from_bytes(docs, dpi=200)
        raw_data = [{f"halaman_{i+1}": read_document(np.array(img))} for i, img in enumerate(images)]
        clean_info = llm_reader(raw_data)
        return succes_response(data=clean_info)
    except Exception as e:
        app_logger.critical(message=f"Error:{e}")
        return error_response(message=f"Error:{e}")

#Read IMG Service
def main_service_ocr_process_img(docs):
    try:
        app_logger.info("data_masuk_img")
        raw_data = read_document(docs)
        clean_info = llm_reader(raw_data)
        return succes_response(data=clean_info)
    except Exception as e:
        app_logger.info(f"Error:{e}")
        return error_response(message=f"Error:{e}")
