from pydantic import BaseModel
from datetime import datetime


class RamUsageRequest(BaseModel):
    total: int
    free: int
    used: int
    time: datetime
