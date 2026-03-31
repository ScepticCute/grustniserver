from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    difficulty = Column(Integer, nullable=False)         
    estimated_time = Column(Integer, nullable=False)     
    description = Column(Text, nullable=False)
    docker_image = Column(String, nullable=True)          