import pytest
from unittest.mock import patch

from research_assistant.paper_search import search_paper


class DummyPaper:
    pass


class DummySemanticPaper:
    def __init__(self, title):
        self.title = title


def test_search_paper_returns_none_when_no_papers():
    title = "Some Paper Title"
    with patch(
        "research_assistant.paper_search.SemanticScholar.search_paper", return_value=[]
    ):
        result = search_paper(title)
    assert result is None


def test_search_paper_returns_none_when_similarity_low():
    # This test simulates returning a paper with a non-similar title
    title = "Some Paper Title"
    dummy_paper = DummySemanticPaper("Totally different title")
    with patch(
        "research_assistant.paper_search.SemanticScholar.search_paper",
        return_value=[dummy_paper],
    ):
        result = search_paper(title)
    assert result is None


def test_search_paper_returns_valid_paper():
    # This test simulates a valid paper result, where the titles are similar enough
    title = "Some Paper Title"
    dummy_paper = DummySemanticPaper("Some Paper Title")
    dummy_converted_paper = DummyPaper()
    with patch(
        "research_assistant.paper_search.SemanticScholar.search_paper",
        return_value=[dummy_paper],
    ), patch(
        "research_assistant.paper_search.Paper.from_semantic_scholar",
        return_value=dummy_converted_paper,
    ):
        result = search_paper(title)
    assert result == dummy_converted_paper
