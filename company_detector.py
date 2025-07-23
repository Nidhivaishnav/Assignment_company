"""
Company detection module for identifying pharmaceutical and biotech companies.
"""

import re
from typing import List, Set, Tuple


class CompanyDetector:
    """Detector for pharmaceutical and biotech companies in author affiliations."""

    def __init__(self):
        """Initialize the company detector with known company patterns."""
        # Major pharmaceutical companies
        self.pharma_companies = {
            "pfizer", "johnson & johnson", "j&j", "janssen", "roche", "genentech",
            "novartis", "merck", "msd", "bristol-myers squibb", "bms", "abbvie",
            "sanofi", "glaxosmithkline", "gsk", "astrazeneca", "boehringer ingelheim",
            "takeda", "eli lilly", "lilly", "bayer", "biogen", "celgene",
            "amgen", "gilead", "regeneron", "vertex", "moderna", "biontech",
            "alexion", "shire", "allergan", "teva", "mylan", "sandoz",
            "hospira", "watson", "actavis", "valeant", "mallinckrodt",
            "endo", "purdue pharma", "otsuka", "daiichi sankyo", "astellas",
            "eisai", "sumitomo dainippon", "mitsubishi tanabe", "chugai",
            "kyowa kirin", "ono pharmaceutical", "shionogi", "tsumura"
        }
        
        # Biotech companies
        self.biotech_companies = {
            "genentech", "amgen", "biogen", "celgene", "regeneron", "vertex",
            "moderna", "biontech", "alexion", "incyte", "bluebird bio",
            "crispr therapeutics", "editas medicine", "intellia therapeutics",
            "sangamo therapeutics", "precision biosciences", "beam therapeutics",
            "prime medicine", "mammoth biosciences", "caribou biosciences",
            "allogene therapeutics", "car-t", "juno therapeutics", "kite pharma",
            "novartis gene therapies", "bluerock therapeutics", "fate therapeutics",
            "cellular biomedicine", "celularity", "cellectis", "celyad",
            "oxford biomedica", "orchard therapeutics", "uniqure", "spark therapeutics",
            "avexis", "zolgensma", "luxturna", "kymriah", "yescarta", "tecartus",
            "abecma", "breyanzi", "carvykti", "roctavian", "hemgenix", "casgevy"
        }
        
        # Generic pharmaceutical/biotech indicators
        self.company_indicators = {
            "pharmaceutical", "pharmaceuticals", "pharma", "biotech", "biotechnology",
            "biopharmaceutical", "biopharmaceuticals", "therapeutics", "medicines",
            "drug", "drugs", "vaccines", "biologics", "biosimilar", "biosimilars",
            "clinical research", "clinical development", "r&d", "research and development",
            "medical affairs", "global medical", "regulatory affairs"
        }
        
        # Corporate suffixes
        self.corporate_suffixes = {
            "inc", "incorporated", "corp", "corporation", "ltd", "limited", "llc",
            "plc", "ag", "sa", "bv", "nv", "gmbh", "co", "company", "companies",
            "group", "holdings", "international", "global", "worldwide", "usa",
            "america", "europe", "asia", "japan", "china", "uk", "germany", "france"
        }

    def detect_companies(self, affiliations: List[str]) -> List[str]:
        """
        Detect pharmaceutical/biotech companies from author affiliations.
        
        Args:
            affiliations: List of affiliation strings
            
        Returns:
            List of detected company names
        """
        detected_companies = set()
        
        for affiliation in affiliations:
            if self._is_non_academic(affiliation):
                companies = self._extract_company_names(affiliation)
                detected_companies.update(companies)
                
        return list(detected_companies)

    def _is_non_academic(self, affiliation: str) -> bool:
        """Check if an affiliation is non-academic (corporate)."""
        affiliation_lower = affiliation.lower()
        
        # Academic institution indicators
        academic_indicators = {
            "university", "college", "school", "institute", "hospital",
            "medical center", "health center", "clinic", "academic",
            "department", "faculty", "laboratory", "lab", "center for",
            "national institutes", "nih", "nsf", "research center",
            "medical school", "graduate school", "postdoctoral",
            "graduate student", "undergraduate", "phd", "md", "dvm"
        }
        
        # Check for academic indicators
        for indicator in academic_indicators:
            if indicator in affiliation_lower:
                return False
                
        # Check for corporate indicators
        for indicator in self.company_indicators:
            if indicator in affiliation_lower:
                return True
                
        # Check for known companies
        for company in self.pharma_companies.union(self.biotech_companies):
            if company in affiliation_lower:
                return True
                
        # Check for corporate structure indicators
        for suffix in self.corporate_suffixes:
            if f" {suffix}" in affiliation_lower or f" {suffix}." in affiliation_lower:
                return True
                
        return False

    def _extract_company_names(self, affiliation: str) -> Set[str]:
        """Extract company names from affiliation string."""
        companies = set()
        affiliation_lower = affiliation.lower()
        
        # Check for exact matches with known companies
        for company in self.pharma_companies.union(self.biotech_companies):
            if company in affiliation_lower:
                companies.add(self._standardize_company_name(company))
                
        # Extract potential company names using patterns
        company_patterns = [
            # Company name followed by corporate suffix
            r'([A-Z][A-Za-z\s&-]+(?:Inc|Corp|Ltd|LLC|PLC|AG|SA|BV|NV|GmbH)\.?)',
            # Company name with pharmaceutical/biotech indicators
            r'([A-Z][A-Za-z\s&-]+(?:Pharmaceutical|Pharma|Biotech|Therapeutics)s?)',
            # General company patterns
            r'([A-Z][A-Za-z\s&-]+(?:Company|Group|Holdings|International|Global))',
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, affiliation, re.IGNORECASE)
            for match in matches:
                clean_name = self._clean_company_name(match)
                if clean_name and len(clean_name) > 3:  # Filter out very short names
                    companies.add(clean_name)
                    
        return companies

    def _standardize_company_name(self, company_name: str) -> str:
        """Standardize company name capitalization."""
        # Convert to title case but preserve common abbreviations
        words = company_name.split()
        standardized = []
        
        abbreviations = {"j&j", "bms", "gsk", "msd", "r&d"}
        
        for word in words:
            if word.lower() in abbreviations:
                standardized.append(word.upper())
            elif word.lower() == "&":
                standardized.append("&")
            else:
                standardized.append(word.capitalize())
                
        return " ".join(standardized)

    def _clean_company_name(self, company_name: str) -> str:
        """Clean and standardize extracted company name."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', company_name.strip())
        
        # Remove trailing punctuation
        cleaned = re.sub(r'[.,;:]+$', '', cleaned)
        
        # Standardize case
        cleaned = self._standardize_company_name(cleaned)
        
        return cleaned

    def filter_papers_with_company_authors(self, papers: List[dict]) -> List[dict]:
        """Filter papers that have at least one author from a pharmaceutical/biotech company."""
        filtered_papers = []
        
        for paper in papers:
            authors = paper.get("authors", [])
            non_academic_authors = []
            company_affiliations = set()
            
            for author in authors:
                affiliations = author.get("affiliations", [])
                author_companies = self.detect_companies(affiliations)
                
                if author_companies:
                    non_academic_authors.append(author["name"])
                    company_affiliations.update(author_companies)
            
            if non_academic_authors:
                paper["non_academic_authors"] = non_academic_authors
                paper["company_affiliations"] = list(company_affiliations)
                filtered_papers.append(paper)
                
        return filtered_papers 