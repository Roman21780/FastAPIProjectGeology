from fastapi import Query
from typing import Optional, List

class SortingParams:
    def __init__(
        self,
        sort_by: Optional[List[str]] = Query(None),
        sort_desc: Optional[List[bool]] = Query(None)
    ):
        self.sort_by = sort_by
        self.sort_desc = sort_desc