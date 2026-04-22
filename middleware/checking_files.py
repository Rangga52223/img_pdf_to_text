from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request

class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        # Kita hanya memeriksa method yang biasanya mengirim payload besar
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            
            if content_length:
                if int(content_length) > self.max_upload_size:
                    return JSONResponse(
                        status_code=413, # Payload Too Large
                        content={
                            "status": "error",
                            "message": f"Ukuran file terlalu besar. Maksimal: {self.max_upload_size / (1024 * 1024):.1f} MB"
                        }
                    )
        
        # Jika aman, lanjutkan ke router/endpoint
        return await call_next(request)