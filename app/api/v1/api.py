from fastapi import APIRouter
from app.api.v1.endpoints import (
    licenses,
    fields,
    wells,
    references
)

router = APIRouter()
router.include_router(licenses.router, prefix="/licenses", tags=["licenses"])
router.include_router(fields.router, prefix="/fields", tags=["fields"])
router.include_router(wells.router, prefix="/wells", tags=["wells"])
router.include_router(references.router, prefix="/references", tags=["references"])