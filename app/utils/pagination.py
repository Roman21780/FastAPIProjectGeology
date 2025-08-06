from fastapi import Query
from typing import Optional

class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000)
    ):
        self.skip = skip
        self.limit = limit