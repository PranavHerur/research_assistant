"""
Module for searching academic papers using various APIs.
"""

from difflib import SequenceMatcher
from typing import Optional

from semanticscholar import SemanticScholar

from research_assistant.models import Paper


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


def search_paper(title: str) -> Optional[Paper]:
    """
    Search for a paper by its title and return its details.

    Args:
        title (str): The title of the paper to search for

    Returns:
        Optional[Paper]: Paper object if found, None otherwise
    """
    sch = SemanticScholar()

    # Search for the paper
    papers = sch.search_paper(title)

    if not papers:
        return None

    similarity = _get_title_similarity(title, papers[0].title)
    print(
        f"Search title: {title} Found title: {papers[0].title} Title similarity: {similarity}"
    )
    if similarity < 0.8:
        return None

    # Get the first (most relevant) result and convert to our Paper class
    return Paper.from_semantic_scholar(papers[0], search_title=title)
