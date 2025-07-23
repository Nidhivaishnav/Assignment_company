#!/usr/bin/env python3
"""
Demo script showing how to use the assignment_backend programmatically.
This demonstrates the core functionality without requiring a live API call.
"""

import sys
import os

# Add the current directory to Python path for local import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assignment_backend.pubmed_client import PubMedClient
from assignment_backend.company_detector import CompanyDetector
from assignment_backend.csv_writer import CSVWriter

def demo_company_detection():
    """Demonstrate company detection functionality."""
    print("=" * 60)
    print("DEMO: Company Detection")
    print("=" * 60)
    
    detector = CompanyDetector()
    
    # Example affiliations
    test_affiliations = [
        "Harvard Medical School, Boston, MA",
        "Pfizer Inc, New York, NY, USA",
        "University of California, San Francisco",
        "Novartis Pharmaceuticals, Basel, Switzerland",
        "Mayo Clinic, Rochester, MN",
        "Johnson & Johnson, New Brunswick, NJ",
        "Moderna Therapeutics, Cambridge, MA",
        "Stanford University School of Medicine"
    ]
    
    print("Testing affiliations:")
    for affiliation in test_affiliations:
        is_company = detector._is_non_academic(affiliation)
        companies = detector._extract_company_names(affiliation)
        
        print(f"\nAffiliation: {affiliation}")
        print(f"  Is company: {'✓' if is_company else '✗'}")
        if companies:
            print(f"  Detected companies: {', '.join(companies)}")

def demo_csv_output():
    """Demonstrate CSV output functionality."""
    print("\n" + "=" * 60)
    print("DEMO: CSV Output")
    print("=" * 60)
    
    # Sample paper data
    sample_papers = [
        {
            "pmid": "12345678",
            "title": "Novel Drug Development for Cancer Treatment",
            "publication_date": "2023-01-15",
            "non_academic_authors": ["John Smith", "Jane Doe"],
            "company_affiliations": ["Pfizer Inc", "Novartis AG"],
            "corresponding_email": "john.smith@pfizer.com"
        },
        {
            "pmid": "87654321", 
            "title": "COVID-19 Vaccine Efficacy Study",
            "publication_date": "2023-02",
            "non_academic_authors": ["Dr. Wilson Brown"],
            "company_affiliations": ["Moderna Therapeutics"],
            "corresponding_email": ""
        }
    ]
    
    writer = CSVWriter()
    csv_output = writer.get_csv_string(sample_papers)
    
    print("Generated CSV output:")
    print("-" * 40)
    print(csv_output)

def demo_full_workflow():
    """Demonstrate the complete workflow (without API calls)."""
    print("\n" + "=" * 60)
    print("DEMO: Complete Workflow")
    print("=" * 60)
    
    # Simulate paper data as it would come from PubMed
    raw_papers = [
        {
            "pmid": "33456789",
            "title": "Alzheimer's Disease Drug Development: A Collaborative Approach",
            "publication_date": "2023-03-10",
            "authors": [
                {
                    "name": "Dr. Alice Johnson",
                    "affiliations": ["Harvard Medical School, Boston, MA"]
                },
                {
                    "name": "Robert Chen",
                    "affiliations": ["Biogen Inc, Cambridge, MA", "MIT, Cambridge, MA"]
                },
                {
                    "name": "Maria Rodriguez",
                    "affiliations": ["Eli Lilly and Company, Indianapolis, IN"]
                }
            ],
            "corresponding_email": "robert.chen@biogen.com"
        }
    ]
    
    print("Processing papers through complete workflow...")
    
    # Initialize components
    detector = CompanyDetector()
    writer = CSVWriter()
    
    # Filter papers with company authors
    filtered_papers = detector.filter_papers_with_company_authors(raw_papers)
    
    print(f"✓ Filtered {len(filtered_papers)} papers with company affiliations")
    
    if filtered_papers:
        print(f"✓ Found companies: {', '.join(filtered_papers[0]['company_affiliations'])}")
        print(f"✓ Non-academic authors: {', '.join(filtered_papers[0]['non_academic_authors'])}")
        
        # Generate CSV
        csv_output = writer.get_csv_string(filtered_papers)
        print("\nGenerated CSV:")
        print("-" * 40)
        print(csv_output)

def main():
    """Run all demos."""
    print("Assignment Backend - Demo Script")
    print("This demonstrates the core functionality without API calls")
    
    try:
        demo_company_detection()
        demo_csv_output()
        demo_full_workflow()
        
        print("\n" + "=" * 60)
        print("✓ Demo completed successfully!")
        print("\nTo use with real PubMed data, run:")
        print('  python -m assignment_backend.cli "your search query" -f output.csv')
        print("\nFor help:")
        print('  python -m assignment_backend.cli --help')
        
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 