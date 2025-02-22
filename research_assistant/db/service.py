"""
Database service layer for paper and author operations.
"""

from typing import Optional

from sqlalchemy.orm import Session

from research_assistant.db.models import DBAuthor, DBPaper
from research_assistant.models import Paper


def get_or_create_author(db: Session, name: str) -> DBAuthor:
    """
    Get an existing author or create a new one.

    Args:
        db: Database session
        name: Author name

    Returns:
        DBAuthor: Author database model
    """
    author = db.query(DBAuthor).filter(DBAuthor.name == name).first()
    if not author:
        author = DBAuthor(name=name)
        db.add(author)
        db.flush()  # Get the ID without committing
    return author


def store_paper(
    db: Session, paper: Paper, semantic_scholar_id: Optional[str] = None
) -> DBPaper:
    """
    Store a paper and its authors in the database.

    Args:
        db: Database session
        paper: Paper dataclass instance
        semantic_scholar_id: Optional Semantic Scholar paper ID

    Returns:
        DBPaper: Stored paper database model
    """
    # Check if paper already exists by title
    existing_paper = db.query(DBPaper).filter(DBPaper.title == paper.title).first()
    if existing_paper:
        return existing_paper

    # Create new paper
    db_paper = DBPaper(
        title=paper.title,
        abstract=paper.abstract,
        url=paper.url,
        venue=paper.venue,
        year=paper.year,
        citation_count=paper.citation_count,
        reference_count=paper.reference_count,
        is_open_access=paper.is_open_access,
        semantic_scholar_id=semantic_scholar_id,
    )

    # Add authors
    for author in paper.authors:
        db_author = get_or_create_author(db, author.name)
        db_paper.authors.append(db_author)

    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)

    return db_paper
