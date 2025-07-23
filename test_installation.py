#!/usr/bin/env python3
"""
Simple test script to verify the installation works correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import requests
        import xmltodict
        import colorama
        print("✓ Core dependencies imported successfully")
        
        from assignment_backend.pubmed_client import PubMedClient
        from assignment_backend.company_detector import CompanyDetector
        from assignment_backend.csv_writer import CSVWriter
        from assignment_backend.cli import main
        print("✓ All modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of core components."""
    try:
        from assignment_backend.pubmed_client import PubMedClient
        from assignment_backend.company_detector import CompanyDetector
        from assignment_backend.csv_writer import CSVWriter
        
        # Test PubMed client initialization
        client = PubMedClient()
        print("✓ PubMed client initialized")
        
        # Test company detector
        detector = CompanyDetector()
        affiliations = ["Pfizer Inc, New York, NY"]
        companies = detector.detect_companies(affiliations)
        print(f"✓ Company detector working: found {len(companies)} companies")
        
        # Test CSV writer
        writer = CSVWriter()
        test_papers = [{
            "pmid": "12345",
            "title": "Test Paper",
            "publication_date": "2023",
            "non_academic_authors": ["Test Author"],
            "company_affiliations": ["Test Company"],
            "corresponding_email": "test@example.com"
        }]
        csv_output = writer.get_csv_string(test_papers)
        print("✓ CSV writer working")
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Assignment Backend Installation...")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_basic_functionality()
    
    print("=" * 50)
    if success:
        print("✓ All tests passed! Installation is working correctly.")
        print("\nTry running:")
        print("  python -m assignment_backend.cli --help")
    else:
        print("✗ Some tests failed. Please check the installation.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 