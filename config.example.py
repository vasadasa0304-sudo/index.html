"""
Configuration Example File
==========================
Copy this file to config.py and customize it for your scraping needs.
DO NOT commit config.py with actual credentials to version control!
"""

# ========================================
# WEBSITE CONFIGURATION
# ========================================

# Base URL of the website to scrape
BASE_URL = "https://example.com/products"

# Custom headers (optional)
# Some websites require specific headers to work properly
CUSTOM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    # Add more headers if needed
}

# ========================================
# SCRAPING CONFIGURATION
# ========================================

# Delay between requests (in seconds) - be respectful!
REQUEST_DELAY = 1.0

# Scraping method: 'single', 'multiple', or 'pagination'
SCRAPE_METHOD = 'single'

# For multiple pages method
URLS_TO_SCRAPE = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

# For pagination method
PAGINATION_CONFIG = {
    'start_page': 1,
    'max_pages': 10,
    'page_param': 'page'  # URL parameter name (e.g., ?page=1)
}

# ========================================
# GOOGLE SHEETS CONFIGURATION
# ========================================

# Path to your Google service account credentials JSON file
CREDENTIALS_FILE = "credentials.json"

# Existing spreadsheet ID (leave None to create a new one)
# Get this from the URL: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
SPREADSHEET_ID = None  # Or "your-spreadsheet-id-here"

# Worksheet name
WORKSHEET_NAME = "Scraped Data"

# Upload mode: 'replace' or 'append'
UPLOAD_MODE = "replace"

# Email to share the spreadsheet with (optional)
SHARE_WITH_EMAIL = None  # Or "your-email@example.com"

# ========================================
# HTML SELECTORS
# ========================================
# Customize these based on the website structure
# Use Chrome DevTools (F12) to inspect elements and find the right selectors

SELECTORS = {
    # Main container for each item
    'item_container': {
        'tag': 'div',
        'class': 'product-card'
    },

    # Individual fields to extract
    'title': {
        'tag': 'h2',
        'class': 'product-title'
    },

    'price': {
        'tag': 'span',
        'class': 'price'
    },

    'description': {
        'tag': 'p',
        'class': 'description'
    },

    'image': {
        'tag': 'img',
        'class': 'product-image',
        'attribute': 'src'  # Extract the src attribute
    },

    'link': {
        'tag': 'a',
        'class': 'product-link',
        'attribute': 'href'
    },

    'rating': {
        'tag': 'span',
        'class': 'rating'
    }
}

# ========================================
# DATA PROCESSING
# ========================================

# Fields to include in the output (in order)
OUTPUT_FIELDS = [
    'title',
    'price',
    'description',
    'rating',
    'link',
    'scraped_at'
]

# Save local copies?
SAVE_CSV = True
SAVE_JSON = True

# Output filenames
CSV_FILENAME = "scraped_data.csv"
JSON_FILENAME = "scraped_data.json"

# ========================================
# LOGGING CONFIGURATION
# ========================================

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Log to file?
LOG_TO_FILE = True
LOG_FILENAME = "scraper.log"
