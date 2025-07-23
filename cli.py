"""
Command-line interface for the PubMed paper fetcher.
"""

import argparse
import logging
import sys
from typing import Optional

from colorama import Fore, init as colorama_init

from .company_detector import CompanyDetector
from .csv_writer import CSVWriter
from .pubmed_client import PubMedClient


def setup_logging(debug: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        debug: Whether to enable debug logging
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='get-papers-list',
        description='Fetch research papers from PubMed and identify pharmaceutical/biotech company affiliations.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  get-papers-list "cancer drug development"
  get-papers-list "COVID-19 vaccine" -f covid_papers.csv
  get-papers-list "alzheimer AND pharmaceutical" -d
  get-papers-list "diabetes[MeSH] AND clinical trial" --file diabetes_studies.csv
  
PubMed Query Syntax:
  Use standard PubMed search syntax:
  - AND, OR, NOT operators
  - MeSH terms with [MeSH] qualifier
  - Field searches like author[au], title[ti]
  - Date ranges with [dp] qualifier
  - etc.
        """
    )
    
    parser.add_argument(
        'query',
        help='Search query using PubMed syntax'
    )
    
    parser.add_argument(
        '-f', '--file',
        metavar='FILENAME',
        help='Specify filename to save results as CSV. If not provided, output to console.'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Print debug information during execution'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=100,
        metavar='N',
        help='Maximum number of papers to fetch (default: 100)'
    )
    
    parser.add_argument(
        '--email',
        metavar='EMAIL',
        help='Contact email for NCBI API usage (recommended for increased rate limits)'
    )
    
    parser.add_argument(
        '--api-key',
        metavar='KEY',
        help='NCBI API key for increased rate limits'
    )
    
    return parser


def print_status(message: str, color: str = Fore.CYAN) -> None:
    """Print colored status message."""
    print(f"{color}[INFO]{Fore.RESET} {message}")


def print_error(message: str) -> None:
    """Print colored error message."""
    print(f"{Fore.RED}[ERROR]{Fore.RESET} {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print colored success message."""
    print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} {message}")


def print_warning(message: str) -> None:
    """Print colored warning message."""
    print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} {message}")


def main() -> None:
    """Main entry point for the command-line interface."""
    # Initialize colorama for Windows support
    colorama_init(autoreset=True)
    
    # Parse command-line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        print_status(f"Searching PubMed for: {args.query}")
        
        pubmed_client = PubMedClient(email=args.email, api_key=args.api_key)
        company_detector = CompanyDetector()
        csv_writer = CSVWriter()
        
        # Search for papers
        if args.debug:
            print_status("Fetching paper IDs from PubMed...")
            
        paper_ids = pubmed_client.search_papers(args.query, args.max_results)
        
        if not paper_ids:
            print_warning("No papers found for the given query.")
            return
            
        print_status(f"Found {len(paper_ids)} papers")
        
        # Fetch detailed paper information
        if args.debug:
            print_status("Fetching detailed paper information...")
            
        papers = pubmed_client.fetch_paper_details(paper_ids)
        
        if not papers:
            print_warning("No detailed paper information could be retrieved.")
            return
            
        print_status(f"Retrieved details for {len(papers)} papers")
        
        # Filter papers with pharmaceutical/biotech company authors
        if args.debug:
            print_status("Filtering papers with company affiliations...")
            
        filtered_papers = company_detector.filter_papers_with_company_authors(papers)
        
        if not filtered_papers:
            print_warning("No papers found with pharmaceutical/biotech company authors.")
            print_status("This could mean:")
            print_status("- No papers in the results have industry authors")
            print_status("- Author affiliation data is not available")
            print_status("- Company detection patterns need refinement")
            return
            
        print_success(f"Found {len(filtered_papers)} papers with company affiliations")
        
        # Output results
        if args.file:
            if args.debug:
                print_status(f"Writing results to file: {args.file}")
                
            csv_writer.write_to_file(filtered_papers, args.file)
            print_success(f"Results saved to {args.file}")
            
            # Print summary of companies found
            all_companies = set()
            for paper in filtered_papers:
                all_companies.update(paper.get('company_affiliations', []))
                
            if all_companies:
                print_status("Companies found:")
                for company in sorted(all_companies):
                    print(f"  - {company}")
        else:
            if args.debug:
                print_status("Writing results to console...")
                
            csv_writer.write_to_console(filtered_papers)
            
    except KeyboardInterrupt:
        print_error("Operation cancelled by user")
        sys.exit(1)
        
    except Exception as e:
        logger.exception("Unexpected error occurred")
        print_error(f"An error occurred: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 