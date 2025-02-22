from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime
from typing import Optional, List
from pydantic import BaseModel

from research_assistant.db.config import get_db
from research_assistant.db.models import DBPaper

router = APIRouter()


class Paper(BaseModel):
    id: int
    title: str
    abstract: Optional[str]
    url: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    citation_count: Optional[int]
    reference_count: Optional[int]
    is_open_access: Optional[bool]
    semantic_scholar_id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


@router.get("/papers", response_model=List[Paper])
def get_papers(db: Session = Depends(get_db)):
    return _query_papers(db)


@router.get("/papers/{paper_id}", response_model=Paper)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    return _query_paper(paper_id, db)


def _query_papers(db: Session):
    return db.query(DBPaper).all()


def _query_paper(paper_id: int, db: Session):
    return db.query(DBPaper).filter(DBPaper.id == paper_id).first()
