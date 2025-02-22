"""
Research Assistant package for academic paper search and analysis.

This package provides tools for searching and analyzing academic papers
using various academic APIs and data sources.
"""

from research_assistant.models import Author, Paper
from research_assistant.paper_search import search_paper

__version__ = "0.1.0"
__author__ = "Research Assistant Team"

__all__ = ["Author", "Paper", "search_paper"]
