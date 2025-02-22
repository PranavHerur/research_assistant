"""
Script to import papers from CSV file and store them in the database.
"""

import csv
from pathlib import Path
import time
from typing import Generator, Optional

from research_assistant.db.config import get_db
from research_assistant.db.service import store_paper
from research_assistant.paper_search import check_paper_exists, search_paper


def read_papers_from_csv(csv_path: str) -> Generator[dict, None, None]:
    """
    Read papers from CSV file.

    Args:
        csv_path: Path to the CSV file

    Yields:
        dict: Paper information from CSV
    """
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Title"):  # Skip empty rows
                yield row


def import_papers(csv_path: str) -> None:
    """
    Import papers from CSV file and store them in the database.

    Args:
        csv_path: Path to the CSV file
    """
    db = next(get_db())
    try:
        total_papers = 0
        stored_papers = 0
        not_found_papers = []

        for paper_info in read_papers_from_csv(csv_path):
            total_papers += 1
            title = paper_info["Title"]
            print(f"\nProcessing paper {total_papers}: {title}")

            # Check if paper already exists in database
            existing_paper = check_paper_exists(db, title)
            if existing_paper:
                print(f"✗ Paper already exists in database: {title}")
                continue

            try:
                # Search for paper
                paper = search_paper(title)
            except Exception as e:
                print(f"✗ Error searching for paper: {e}")
                not_found_papers.append((title, "Search error"))
                continue

            # Sleep for 10 seconds to avoid hitting API rate limits
            print("Waiting 10 seconds before next request...")
            time.sleep(5)

            if paper:
                try:
                    db_paper = store_paper(db, paper)
                    stored_papers += 1
                    print(f"✓ Stored paper with ID: {db_paper.id}")
                    print(
                        f"  Authors: {', '.join(author.name for author in db_paper.authors)}"
                    )
                except Exception as e:
                    print(f"✗ Error storing paper: {e}")
                    not_found_papers.append((title, "Storage error"))
            else:
                print("✗ Paper not found in Semantic Scholar")
                not_found_papers.append((title, "Not found"))

        # Print summary
        print("\nImport Summary:")
        print(f"Total papers processed: {total_papers}")
        print(f"Successfully stored: {stored_papers}")
        print(f"Failed: {len(not_found_papers)}")

        if not_found_papers:
            # Write failed paper titles to failed_papers.csv with a column "Title"
            csv_path = Path(__file__).parent.parent / "data" / "failed_papers.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["Title"])
                writer.writeheader()
                for title, _ in not_found_papers:
                    writer.writerow({"Title": title})
            print(f"\nFailed papers have been written to {csv_path}")

    finally:
        db.close()


if __name__ == "__main__":
    # Get the absolute path to the CSV file
    csv_path = Path(__file__).parent.parent / "data" / "dl4h_papers.csv"
    import_papers(str(csv_path))
