from fastapi.testclient import TestClient
from unittest.mock import patch

from research_assistant.db.models import DBPaper
from main import app

client = TestClient(app)


def test_get_papers_empty():
    # Test that the /papers endpoint returns an empty list when there are no papers
    with patch("api.papers._query_papers", return_value=[]):
        response = client.get("/papers")
        assert response.status_code == 200
        assert response.json() == []


def test_get_papers_with_data():
    # Create a fake paper instance that the patched _query_papers
    # function will return as a list containing one paper
    fake_paper = DBPaper(
        id=1,
        title="Test Paper",
        abstract="This is a test abstract",
        url="http://example.com",
        venue="Test Venue",
        year=2023,
        citation_count=10,
        reference_count=5,
        is_open_access=True,
        semantic_scholar_id="test_id",
    )

    # Patch the _query_papers function in api.papers so that it returns our fake paper
    with patch("api.papers._query_papers", return_value=[fake_paper]):
        response = client.get("/papers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        found = any(item["title"] == "Test Paper" for item in data)
        assert found
