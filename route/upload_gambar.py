from fastapi import FastAPI, File, UploadFile
from pdf2image import convert_from_bytes
from service.main_service import ocr_process, main_service_img_process_pdf, main_service_ocr_process_img
from tools.main_tools import read_document
from base_response import succes_response, error_response
from logger import app_logger
from route import uploads
import asyncio
import numpy as np
import cv2

@uploads.post("/service")
async def uploads_ocr_gambar(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        
        if file.content_type == "application/pdf":
            images = convert_from_bytes(file_bytes, dpi=200)
            full_text = [{f"halaman_{i+1}": read_document(np.array(img))} for i, img in enumerate(images)]
            return succes_response(data=full_text)
            
        elif file.content_type in ["image/jpeg", "image/png"]:
            return succes_response(data=read_document(file_bytes))
            
        else:
            return error_response(message="Format file tidak didukung. Gunakan PDF, JPG, atau PNG.")
            
    except Exception as e:
        return error_response(message=f"Terjadi kesalahan sistem: {str(e)}")
    
    # print("DEBUG:Prefix")
    # contents = await file.read()
    # nparr = np.frombuffer(contents, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # return ocr_process(img)

@uploads.post("/")
async def uploads_all_route(file: UploadFile = File(...)):
    try:
        app_logger.info(f"Menerima file: {file.filename} dengan tipe: {file.content_type}")
        file_bytes = await file.read()
        
        if file.content_type == "application/pdf":
            # 1. LEMPAR PROSES BERAT KE THREAD
            result = await asyncio.to_thread(main_service_img_process_pdf, file_bytes)
            return result
            
        elif file.content_type in ["image/jpeg", "image/png", "image/jpg"]: # Tambahkan image/jpg untuk jaga-jaga
            # 2. LEMPAR PROSES BERAT KE THREAD
            result = await asyncio.to_thread(main_service_ocr_process_img, file_bytes)
            return result
            
        else:
            return error_response(message="Format file tidak didukung. Gunakan PDF, JPG, atau PNG.")
            
    except Exception as e:
        app_logger.critical(f"Error di endpoint uploads: {e}")
        return error_response(message=f"Terjadi kesalahan internal server. Detail: {e}")
        