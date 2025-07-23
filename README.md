# Assignment_company
# PubMed Research Paper Fetcher

A Python program to fetch research papers from PubMed and identify papers with at least one author affiliated with a pharmaceutical or biotech company.

## Features

- **PubMed Integration**: Fetch papers using the PubMed API with full query syntax support
- **Company Detection**: Automatically identify pharmaceutical and biotech company affiliations
- **Flexible Output**: Export results to CSV file or display in console
- **Command-line Interface**: Easy-to-use CLI with helpful options
- **Rate Limiting**: Respectful API usage with built-in rate limiting
- **Comprehensive Testing**: Full test suite with high coverage

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry for dependency management

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd assignment_backend
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

## Usage

The program provides an executable command `get-papers-list` that can be used after installation:

### Basic Usage

```bash
# Search for papers and display in console
get-papers-list "cancer drug development"

# Save results to CSV file
get-papers-list "COVID-19 vaccine" -f covid_papers.csv

# Enable debug mode for detailed information
get-papers-list "alzheimer AND pharmaceutical" -d
```

### Command-line Options

- **`query`**: Search query using PubMed syntax (required)
- **`-f, --file FILENAME`**: Specify filename to save results as CSV
- **`-d, --debug`**: Print debug information during execution
- **`-h, --help`**: Display usage instructions
- **`--max-results N`**: Maximum number of papers to fetch (default: 100)
- **`--email EMAIL`**: Contact email for NCBI API usage (recommended)
- **`--api-key KEY`**: NCBI API key for increased rate limits

### PubMed Query Syntax

The program supports the full PubMed search syntax:

```bash
# Boolean operators
get-papers-list "diabetes AND insulin"
get-papers-list "cancer OR tumor"
get-papers-list "drug NOT withdrawal"

# MeSH terms
get-papers-list "diabetes[MeSH] AND clinical trial"

# Field searches
get-papers-list "smith[author] AND cancer[title]"

# Date ranges
get-papers-list "COVID-19 AND 2020:2023[dp]"
```

### Examples

```bash
# Find cancer drug development papers
get-papers-list "cancer drug development" -f cancer_drugs.csv

# Search for COVID-19 vaccine papers with company involvement
get-papers-list "COVID-19 vaccine" --file covid_vaccines.csv --debug

# Find diabetes research with pharmaceutical companies
get-papers-list "diabetes[MeSH] AND pharmaceutical" -f diabetes_pharma.csv

# Use email for better API rate limits
get-papers-list "alzheimer drug" --email your.email@example.com -f alzheimer.csv
```

## Output Format

The program outputs a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| **PubmedID** | Unique identifier for the paper |
| **Title** | Title of the paper |
| **Publication Date** | Date the paper was published |
| **Non-academic Author(s)** | Names of authors affiliated with non-academic institutions |
| **Company Affiliation(s)** | Names of pharmaceutical/biotech companies |
| **Corresponding Author Email** | Email address of the corresponding author |

## Code Organization

### Project Structure

```
assignment_backend/
├── assignment_backend/          # Main package
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # Command-line interface
│   ├── pubmed_client.py        # PubMed API client
│   ├── company_detector.py     # Company detection logic
│   └── csv_writer.py           # CSV output functionality
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_pubmed_client.py   # PubMed client tests
│   ├── test_company_detector.py # Company detection tests
│   └── test_csv_writer.py      # CSV writer tests
├── .cursor/                    # Cursor IDE configuration
├── pyproject.toml              # Poetry configuration
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── .cursorignore              # Cursor ignore rules
```

### Core Modules

#### 1. PubMed Client (`pubmed_client.py`)
- Handles communication with the PubMed API
- Manages search queries and paper detail retrieval
- Implements rate limiting and error handling
- Parses XML responses into structured data

#### 2. Company Detector (`company_detector.py`)
- Identifies pharmaceutical and biotech companies
- Distinguishes between academic and non-academic affiliations
- Uses pattern matching and known company databases
- Filters papers with company-affiliated authors

#### 3. CSV Writer (`csv_writer.py`)
- Formats paper data for CSV output
- Handles console and file output
- Cleans and sanitizes text data
- Maintains consistent formatting

#### 4. Command-line Interface (`cli.py`)
- Processes command-line arguments
- Orchestrates the complete workflow
- Provides user feedback and error handling
- Supports various output options

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=assignment_backend

# Run specific test file
poetry run pytest tests/test_pubmed_client.py

# Run with verbose output
poetry run pytest -v
```

### Code Quality

```bash
# Format code with black
poetry run black assignment_backend/ tests/

# Check with flake8
poetry run flake8 assignment_backend/ tests/

# Type checking with mypy
poetry run mypy assignment_backend/
```

### Adding Dependencies

```bash
# Add a new dependency
poetry add package_name

# Add a development dependency
poetry add --group dev package_name
```

## API Rate Limits

The program implements responsible API usage:

- **Default Rate**: 3 requests per second (without API key)
- **With API Key**: 10 requests per second
- **Batch Processing**: Processes papers in batches of 200
- **Automatic Delays**: Built-in delays between batch requests

### Recommended Setup

For better performance, obtain a free NCBI API key:

1. Create an account at [NCBI](https://www.ncbi.nlm.nih.gov/account/)
2. Generate an API key from your account settings
3. Use the `--api-key` option or set environment variable

## Company Detection

The program identifies companies using multiple approaches:

### Known Companies Database
- Major pharmaceutical companies (Pfizer, Novartis, J&J, etc.)
- Biotech companies (Moderna, Genentech, Biogen, etc.)
- Continuously updated list of industry players

### Pattern Recognition
- Corporate suffixes (Inc, Corp, Ltd, LLC, etc.)
- Industry keywords (Pharmaceutical, Biotech, Therapeutics)
- Research indicators (R&D, Clinical Development)

### Academic Institution Filtering
- Universities and colleges
- Medical schools and hospitals
- Government research institutes
- Non-profit research organizations

## Troubleshooting

### Common Issues

**No papers found:**
- Check your query syntax
- Try broader search terms
- Verify PubMed has results for your query

**No company affiliations detected:**
- Author affiliation data may be limited
- Try different search queries
- Company detection patterns may need refinement

**API rate limiting:**
- Use the `--email` parameter
- Consider getting an NCBI API key
- Reduce `--max-results` for faster processing

**Network issues:**
- Check internet connectivity
- Verify PubMed API accessibility
- Try again later if servers are busy

### Debug Mode

Use the `-d` or `--debug` flag for detailed information:

```bash
get-papers-list "your query" -d
```

This provides:
- API request details
- Processing step information
- Error details and stack traces
- Performance metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is developed as part of an assignment and follows standard open-source practices.

## Support

For issues, questions, or feature requests, please create an issue in the repository or contact the development team. 
