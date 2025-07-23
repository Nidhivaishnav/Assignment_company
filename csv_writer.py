"""
CSV writer module for outputting research paper results.
"""

import csv
import sys
from io import StringIO
from typing import List, TextIO


class CSVWriter:
    """Writer for outputting research paper results to CSV format."""

    def __init__(self):
        """Initialize CSV writer."""
        self.headers = [
            "PubmedID",
            "Title", 
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email"
        ]

    def write_to_file(self, papers: List[dict], filename: str) -> None:
        """
        Write papers to CSV file.
        
        Args:
            papers: List of paper dictionaries
            filename: Output filename
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            self._write_papers(papers, csvfile)

    def write_to_console(self, papers: List[dict]) -> None:
        """
        Write papers to console output.
        
        Args:
            papers: List of paper dictionaries
        """
        self._write_papers(papers, sys.stdout)

    def get_csv_string(self, papers: List[dict]) -> str:
        """
        Get papers as CSV string.
        
        Args:
            papers: List of paper dictionaries
            
        Returns:
            CSV formatted string
        """
        output = StringIO()
        self._write_papers(papers, output)
        return output.getvalue()

    def _write_papers(self, papers: List[dict], output: TextIO) -> None:
        """
        Write papers to the given output stream.
        
        Args:
            papers: List of paper dictionaries
            output: Output stream to write to
        """
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        writer.writerow(self.headers)
        
        # Write paper data
        for paper in papers:
            row = self._format_paper_row(paper)
            writer.writerow(row)

    def _format_paper_row(self, paper: dict) -> List[str]:
        """
        Format a paper dictionary into a CSV row.
        
        Args:
            paper: Paper dictionary
            
        Returns:
            List of formatted values for CSV row
        """
        # Extract and format values
        pubmed_id = paper.get("pmid", "")
        title = self._clean_text(paper.get("title", ""))
        publication_date = paper.get("publication_date", "")
        
        # Format non-academic authors
        non_academic_authors = paper.get("non_academic_authors", [])
        authors_str = "; ".join(non_academic_authors) if non_academic_authors else ""
        
        # Format company affiliations
        company_affiliations = paper.get("company_affiliations", [])
        companies_str = "; ".join(company_affiliations) if company_affiliations else ""
        
        # Corresponding author email
        corresponding_email = paper.get("corresponding_email", "")
        
        return [
            pubmed_id,
            title,
            publication_date,
            authors_str,
            companies_str,
            corresponding_email
        ]

    def _clean_text(self, text: str) -> str:
        """
        Clean text for CSV output.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Remove excessive whitespace
        cleaned = " ".join(text.split())
        
        # Remove problematic characters that might break CSV
        cleaned = cleaned.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        # Truncate if too long (to prevent CSV issues)
        if len(cleaned) > 1000:
            cleaned = cleaned[:997] + "..."
            
        return cleaned 