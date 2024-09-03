# schemas_profile.py
from pydantic import BaseModel # type: ignore
from datetime import datetime


class MonitoringBase(BaseModel):
    mon_dataHorario: datetime

class MonitoringEdit(MonitoringBase):
    mon_sintomasId: int
    mon_perfilId: int

    class Config:
        orm_mode = True
        from_attributes = True