"""
Models for representing academic papers and related entities.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Author:
    """Represents an author of a paper."""

    name: str
    affiliations: Optional[List[str]] = None


@dataclass
class Paper:
    """
    Represents an academic paper with its metadata.
    """

    title: str
    authors: List[Author]
    abstract: Optional[str] = None
    url: Optional[str] = None
    venue: Optional[str] = None
    year: Optional[int] = None
    title_similarity: Optional[float] = None
    citation_count: Optional[int] = None
    reference_count: Optional[int] = None
    is_open_access: Optional[bool] = None
    semantic_scholar_id: Optional[str] = None

    @classmethod
    def from_semantic_scholar(cls, paper, search_title: str = None) -> "Paper":
        """
        Create a Paper instance from a SemanticScholar paper object.

        Args:
            paper: SemanticScholar paper object
            search_title: Optional original search title for similarity calculation

        Returns:
            Paper: New Paper instance
        """

        # Convert SemanticScholar authors to our Author objects
        authors = [
            Author(name=author.name, affiliations=getattr(author, "affiliations", None))
            for author in paper.authors
        ]

        return cls(
            title=paper.title,
            authors=authors,
            abstract=paper.abstract,
            url=paper.url,
            venue=paper.venue,
            year=paper.year,
            citation_count=getattr(paper, "citationCount", None),
            reference_count=getattr(paper, "referenceCount", None),
            is_open_access=getattr(paper, "isOpenAccess", None),
            semantic_scholar_id=getattr(paper, "paperId", None),
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of the paper."""
        authors_str = ", ".join(author.name for author in self.authors)
        return f"{self.title} ({self.year}) by {authors_str}"
