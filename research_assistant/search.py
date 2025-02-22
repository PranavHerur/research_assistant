from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from research_assistant.db.models import DBPaper
from research_assistant.db.config import engine, SessionLocal


def search_papers(query: str, session: Session) -> List[DBPaper]:
    """
    Search the database for papers whose title or abstract match the given query text.
    Performs a case-insensitive 'LIKE' search on both fields.

    :param query: The text to search for.
    :param session: SQLAlchemy session for database connection.
    :return: List of matching DBPaper objects.
    """
    return (
        session.query(DBPaper)
        .filter(
            or_(DBPaper.title.ilike(f"%{query}%"), DBPaper.abstract.ilike(f"%{query}%"))
        )
        .all()
    )


if __name__ == "__main__":
    # Example usage (requires proper database setup):
    session = SessionLocal()

    query_text = "machine learning"
    results = search_papers(query_text, session)
    for paper in results:
        print(paper)
