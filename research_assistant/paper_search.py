"""
Module for searching academic papers using various APIs.
"""

import logging
from difflib import SequenceMatcher
from typing import Optional

from semanticscholar import SemanticScholar
from semanticscholar.Paper import Paper as SemanticScholarPaper
from sqlalchemy.orm import Session
from sqlalchemy import func

from research_assistant.db.models import DBPaper
from research_assistant.models import Paper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_title_similarity(title1: str, title2: str) -> float:
    """
    Calculate the similarity ratio between two titles.

    Args:
        title1 (str): First title
        title2 (str): Second title

    Returns:
        float: Similarity ratio between 0 and 1
    """
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()


def check_paper_exists(db: Session, title: str) -> Optional[DBPaper]:
    """
    Check if a paper already exists in the database, using a case-insensitive title comparison.

    Args:
        db: Database session
        title: Paper title to check

    Returns:
        Optional[DBPaper]: Existing paper if found, None otherwise
    """
    # Remove all punctuation from the title
    return db.query(DBPaper).filter(func.lower(DBPaper.title) == title.lower()).first()


def search_paper(title: str) -> Optional[Paper]:
    """
    Search for a paper by its title and return its details.
    First checks the local database, then falls back to Semantic Scholar.

    Args:
        title (str): The title of the paper to search for

    Returns:
        Optional[Paper]: Paper object if found, None otherwise
    """

    sch = SemanticScholar()
    papers = sch.search_paper(title)

    if not papers:
        return None

    paper: SemanticScholarPaper = papers[0]
    similarity = _get_title_similarity(title, paper.title)
    logger.info(
        f"Search title: {title}\nFound title: {paper.title}\nTitle similarity: {similarity * 100}%"
    )
    if similarity < 0.8:
        return None

    for k in paper.__dict__.keys():
        print(f"{k}: {paper.__dict__[k]}")

    # Get the first (most relevant) result and convert to our Paper class
    return Paper.from_semantic_scholar(papers[0], search_title=title)
