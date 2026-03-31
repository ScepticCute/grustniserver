from sqlalchemy.orm import Session
from .models import Lab

def get_all_labs(db: Session):
    return db.query(Lab).all()

def get_lab_by_id(db: Session, lab_id: int):
    return db.query(Lab).filter(Lab.id == lab_id).first()