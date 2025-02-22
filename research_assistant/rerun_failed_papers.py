import csv
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import func

# Make sure to adjust this import according to your project's structure.
from research_assistant.db.config import get_db
from research_assistant.db.models import DBPaper
from research_assistant.import_papers import import_papers, read_papers_from_csv
from research_assistant.paper_search import check_paper_exists, search_paper


def retry_failed_imports(file_path: str) -> None:
    """
    Rerun the import process for papers listed in a CSV file of failed imports.

    The CSV file should contain headers corresponding to the fields required
    to create a DBPaper (for example: title, authors, year, etc.).

    Args:
        file_path (str): Path to the CSV file with failed paper data.
    """
    import_papers(file_path)


if __name__ == "__main__":
    csv_path = Path(__file__).parent.parent / "data" / "failed_papers.csv"
    retry_failed_imports(str(csv_path))
