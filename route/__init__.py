from fastapi import APIRouter
test = APIRouter(
    prefix="",
    tags=["test"]
)
uploads = APIRouter(
    prefix="/api/v1/upload-gambar",
    tags=["uplad"]
)