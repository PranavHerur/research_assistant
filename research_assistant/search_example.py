"""
Example script to demonstrate paper search functionality.
"""

from research_assistant.paper_search import search_paper


def main():
    search_title = (
        "Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings"
    )
    paper = search_paper(search_title)

    if paper:
        print("\nPaper found!")
        print(f"Search title: {search_title}")
        print(f"Found title: {paper.title}")
        print(f"\nAuthors: {', '.join(author.name for author in paper.authors)}")

        if paper.year:
            print(f"Year: {paper.year}")
        if paper.venue:
            print(f"Venue: {paper.venue}")
        if paper.citation_count:
            print(f"Citations: {paper.citation_count}")
        if paper.reference_count:
            print(f"References: {paper.reference_count}")

        print(f"\nURL: {paper.url}")
        if paper.pdf_url:
            print(f"PDF URL: {paper.pdf_url}")
        if paper.is_open_access:
            print("This paper is Open Access!")

        if paper.abstract:
            print(f"\nAbstract: {paper.abstract}")

        # Show the string representation of the paper
        print("\nCitation:")
        print(str(paper))
    else:
        print("Paper not found.")


if __name__ == "__main__":
    main()
