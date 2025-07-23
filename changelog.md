# Changelog

## 01-Jun-2025 - Initial Development

### Added
- Complete PubMed Research Paper Fetcher implementation
- PubMed API client with XML parsing and rate limiting
- Pharmaceutical/biotech company detection system
- CSV output functionality with all required columns
- Command-line interface with full argument support
- Comprehensive test suite for all modules
- Poetry configuration for dependency management
- README.md with detailed documentation
- Git repository initialization
- .cursor directory setup for IDE configuration

### Features Implemented
- PubMed API integration using esearch and efetch
- Company detection for 50+ major pharmaceutical companies
- Pattern-based detection for biotech and pharma indicators
- Academic vs non-academic affiliation filtering
- CSV export with proper formatting and cleaning
- Console output option
- Debug mode with detailed logging
- Rate limiting and batch processing
- Email extraction from author affiliations
- Comprehensive error handling

### Technical Details
- Python 3.8+ compatibility
- Modular architecture with separate concerns
- Type hints and documentation throughout
- Test coverage for all core functionality
- Command-line executable via Poetry scripts
- Fallback requirements.txt for non-Poetry environments 