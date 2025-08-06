from fastapi import APIRouter

router = APIRouter()

# Импортируем после создания router для избежания circular imports
from app.api.v1.endpoints import licenses, fields, wells, references

router.include_router(licenses.router)
router.include_router(fields.router)
router.include_router(wells.router)
router.include_router(references.router)