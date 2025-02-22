from pathlib import Path
from research_assistant.db.config import get_db
from research_assistant.import_papers import read_papers_from_csv
from research_assistant.paper_search import check_paper_exists


def find_missing_papers(csv_path: str) -> list[str]:
    """
    Read through a CSV file and find papers that are not in the database.

    Args:
        csv_path: Path to the CSV file

    Returns:
        list[str]: List of paper titles that are not in the database
    """
    db = next(get_db())
    missing_papers = []

    try:
        for paper_info in read_papers_from_csv(csv_path):
            title = paper_info["Title"]
            existing_paper = check_paper_exists(db, title)

            if not existing_paper:
                missing_papers.append(title)

    finally:
        db.close()

    return missing_papers


if __name__ == "__main__":
    csv_path = Path(__file__).parent.parent / "data" / "dl4h_papers.csv"
    missing_papers = find_missing_papers(str(csv_path))
    print(f"Found {len(missing_papers)} missing papers")
    for paper in missing_papers:
        print(paper)
