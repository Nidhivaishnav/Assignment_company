"""
PubMed API client for fetching research papers.
"""

import json
import logging
import re
import time
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import quote

import requests
import xmltodict


class PubMedClient:
    """Client for interacting with PubMed API."""

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize PubMed client.
        
        Args:
            email: Contact email for NCBI API usage
            api_key: NCBI API key for increased rate limits
        """
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.email = email
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def search_papers(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search for papers using PubMed query syntax.
        
        Args:
            query: Search query in PubMed format
            max_results: Maximum number of results to return
            
        Returns:
            List of PubMed IDs
        """
        url = f"{self.base_url}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "usehistory": "y"
        }
        
        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            id_list = data.get("esearchresult", {}).get("idlist", [])
            self.logger.info(f"Found {len(id_list)} papers for query: {query}")
            return id_list
            
        except requests.RequestException as e:
            self.logger.error(f"Error searching PubMed: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing search response: {e}")
            raise

    def fetch_paper_details(self, pubmed_ids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for a list of PubMed IDs.
        
        Args:
            pubmed_ids: List of PubMed IDs
            
        Returns:
            List of paper details
        """
        if not pubmed_ids:
            return []

        # Process in batches to avoid overwhelming the API
        batch_size = 200
        all_papers = []
        
        for i in range(0, len(pubmed_ids), batch_size):
            batch = pubmed_ids[i:i + batch_size]
            batch_papers = self._fetch_batch_details(batch)
            all_papers.extend(batch_papers)
            
            # Rate limiting - be respectful to NCBI servers
            if i + batch_size < len(pubmed_ids):
                time.sleep(0.5)
                
        return all_papers

    def _fetch_batch_details(self, pubmed_ids: List[str]) -> List[Dict]:
        """Fetch details for a batch of PubMed IDs."""
        url = f"{self.base_url}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "retmode": "xml",
            "rettype": "abstract"
        }
        
        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            data = xmltodict.parse(response.content)
            articles = data.get("PubmedArticleSet", {}).get("PubmedArticle", [])
            
            # Handle single article case
            if isinstance(articles, dict):
                articles = [articles]
                
            papers = []
            for article in articles:
                paper = self._parse_article(article)
                if paper:
                    papers.append(paper)
                    
            return papers
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching paper details: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error parsing paper details: {e}")
            raise

    def _parse_article(self, article: Dict) -> Optional[Dict]:
        """Parse a single article from PubMed XML."""
        try:
            medline_citation = article.get("MedlineCitation", {})
            pubmed_data = article.get("PubmedData", {})
            
            # Extract basic information
            pmid = medline_citation.get("PMID", {}).get("#text", "")
            if isinstance(pmid, dict):
                pmid = pmid.get("#text", "")
                
            article_info = medline_citation.get("Article", {})
            title = article_info.get("ArticleTitle", "")
            if isinstance(title, dict):
                title = title.get("#text", "")
                
            # Extract publication date
            pub_date = self._extract_publication_date(article_info)
            
            # Extract authors and affiliations
            authors = self._extract_authors(article_info)
            
            # Extract corresponding author email
            corresponding_email = self._extract_corresponding_email(article_info)
            
            return {
                "pmid": pmid,
                "title": title,
                "publication_date": pub_date,
                "authors": authors,
                "corresponding_email": corresponding_email
            }
            
        except Exception as e:
            self.logger.warning(f"Error parsing article: {e}")
            return None

    def _extract_publication_date(self, article_info: Dict) -> str:
        """Extract publication date from article info."""
        try:
            journal = article_info.get("Journal", {})
            issue = journal.get("JournalIssue", {})
            pub_date = issue.get("PubDate", {})
            
            year = pub_date.get("Year", "")
            month = pub_date.get("Month", "")
            day = pub_date.get("Day", "")
            
            if year:
                date_parts = [year]
                if month:
                    date_parts.append(month)
                    if day:
                        date_parts.append(day)
                return "-".join(date_parts)
            
            # Fallback to medline date
            medline_date = pub_date.get("MedlineDate", "")
            if medline_date:
                # Extract year from medline date (format like "2023 Jan-Feb")
                year_match = re.search(r"\b(19|20)\d{2}\b", medline_date)
                if year_match:
                    return year_match.group(0)
                    
            return ""
            
        except Exception:
            return ""

    def _extract_authors(self, article_info: Dict) -> List[Dict]:
        """Extract authors and their affiliations."""
        try:
            author_list = article_info.get("AuthorList", {}).get("Author", [])
            if isinstance(author_list, dict):
                author_list = [author_list]
                
            authors = []
            for author in author_list:
                # Extract author name
                last_name = author.get("LastName", "")
                first_name = author.get("ForeName", "")
                initials = author.get("Initials", "")
                
                name = f"{first_name} {last_name}".strip()
                if not name and initials and last_name:
                    name = f"{initials} {last_name}".strip()
                    
                # Extract affiliations
                affiliations = []
                affiliation_info = author.get("AffiliationInfo", [])
                if isinstance(affiliation_info, dict):
                    affiliation_info = [affiliation_info]
                    
                for aff in affiliation_info:
                    affiliation = aff.get("Affiliation", "")
                    if affiliation:
                        affiliations.append(affiliation)
                
                if name:
                    authors.append({
                        "name": name,
                        "affiliations": affiliations
                    })
                    
            return authors
            
        except Exception:
            return []

    def _extract_corresponding_email(self, article_info: Dict) -> str:
        """Extract corresponding author email if available."""
        try:
            author_list = article_info.get("AuthorList", {}).get("Author", [])
            if isinstance(author_list, dict):
                author_list = [author_list]
                
            for author in author_list:
                # Look for email in affiliation info
                affiliation_info = author.get("AffiliationInfo", [])
                if isinstance(affiliation_info, dict):
                    affiliation_info = [affiliation_info]
                    
                for aff in affiliation_info:
                    affiliation = aff.get("Affiliation", "")
                    if affiliation:
                        # Extract email using regex
                        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', affiliation)
                        if email_match:
                            return email_match.group(0)
                            
            return ""
            
        except Exception:
            return "" 