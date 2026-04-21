import uvicorn # Tambahkan import ini di atas
from fastapi import FastAPI
from route.test_route import test
from route.upload_gambar import uploads
# from app.route.ai_route import ai

app = FastAPI(
    title="OCR_Scan_Docs",
    version="Alpha 1.0.0",
    description="OCR Apps Clasification",
    openapi_url=None,
    docs_url=None,         
    redoc_url=None         
)

app.include_router(test)
app.include_router(uploads)
if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)