from pydantic import BaseModel
from typing import Optional

class LabList(BaseModel):
    id: int
    name: str
    difficulty: int
    estimated_time: int

class LabDetail(BaseModel):
    id: int
    name: str
    difficulty: int
    estimated_time: int
    description: str
    docker_image: Optional[str]
    status: str = "not_launched"   # not_launched / deploying / running / error