# Python Web Scraper Template with Google Sheets Integration

A flexible and reusable Python template for scraping websites without APIs and automatically uploading the data to Google Sheets.

## Features

- **Flexible Web Scraping**: Template-based scraper that can be customized for any website
- **Google Sheets Integration**: Automatic upload of scraped data to Google Sheets
- **Multiple Scraping Modes**: Single page, multiple pages, or pagination support
- **Respectful Scraping**: Built-in delays and proper headers to be respectful to servers
- **Error Handling**: Comprehensive logging and error handling
- **Data Export**: Save to CSV, JSON, or Google Sheets
- **Batch Operations**: Upload to multiple worksheets in one operation
- **Auto-formatting**: Automatic header formatting and freezing in Google Sheets

## Project Structure

```
.
├── web_scraper_template.py      # Base web scraper class
├── google_sheets_uploader.py    # Google Sheets integration
├── scrape_and_upload.py         # Combined scraper + uploader
├── requirements.txt             # Python dependencies
├── config.example.py            # Example configuration
└── README.md                    # This file
```

## Prerequisites

- Python 3.7 or higher
- Google Cloud Project with Sheets API enabled
- Google Service Account credentials

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Google Sheets API

#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API" and enable it
   - Search for "Google Drive API" and enable it

#### Step 2: Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details and click "Create"
4. Skip the optional steps and click "Done"
5. Click on the created service account
6. Go to the "Keys" tab
7. Click "Add Key" > "Create New Key"
8. Choose JSON format and click "Create"
9. Save the downloaded JSON file as `credentials.json` in your project directory

#### Step 3: Share Your Spreadsheet

If you're uploading to an existing spreadsheet:
1. Open your Google Spreadsheet
2. Click the "Share" button
3. Add the service account email (found in `credentials.json` under `client_email`)
4. Give it "Editor" permissions

## Usage

### Quick Start

1. **Customize the scraper for your target website**

Edit the `parse_data()` method in `web_scraper_template.py` or `scrape_and_upload.py`:

```python
def parse_data(self, soup: BeautifulSoup) -> List[Dict]:
    data = []

    # Change these selectors to match your target website
    items = soup.find_all('div', class_='your-item-class')

    for item in items:
        data.append({
            'title': item.find('h2').text.strip(),
            'price': item.find('span', class_='price').text.strip(),
            'link': item.find('a')['href'],
            'scraped_at': datetime.now().isoformat()
        })

    return data
```

2. **Run the scraper**

```bash
python scrape_and_upload.py
```

### Examples

#### Example 1: Scrape a Single Page

```python
from scrape_and_upload import ScraperWithUpload

scraper = ScraperWithUpload(
    base_url="https://example.com",
    credentials_file="credentials.json"
)

url = scraper.scrape_and_upload(
    worksheet_name='My Data',
    mode='replace',
    scrape_method='single'
)

print(f"Data uploaded to: {url}")
```

#### Example 2: Scrape Multiple Pages

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

url = scraper.scrape_and_upload(
    worksheet_name='Multiple Pages',
    mode='replace',
    scrape_method='multiple',
    urls=urls,
    delay=1.0  # 1 second delay between requests
)
```

#### Example 3: Scrape with Pagination

```python
url = scraper.scrape_and_upload(
    worksheet_name='Paginated Data',
    mode='replace',
    scrape_method='pagination',
    start_page=1,
    max_pages=10,
    page_param='page',  # URL parameter for pagination
    delay=1.0
)
```

#### Example 4: Append to Existing Spreadsheet

```python
# Get spreadsheet ID from the URL:
# https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
spreadsheet_id = "your-spreadsheet-id-here"

url = scraper.scrape_and_upload(
    spreadsheet_id=spreadsheet_id,
    worksheet_name='Sheet1',
    mode='append',  # Append instead of replace
    scrape_method='single'
)
```

### Using Individual Components

#### Web Scraper Only (Save to CSV/JSON)

```python
from web_scraper_template import WebScraperTemplate

scraper = WebScraperTemplate("https://example.com")
soup = scraper.fetch_page("https://example.com")
data = scraper.parse_data(soup)

# Save to CSV
scraper.save_to_csv(data, 'output.csv')

# Save to JSON
scraper.save_to_json(data, 'output.json')
```

#### Google Sheets Uploader Only

```python
from google_sheets_uploader import GoogleSheetsUploader

uploader = GoogleSheetsUploader('credentials.json')

data = [
    {'name': 'Item 1', 'price': '$10'},
    {'name': 'Item 2', 'price': '$20'}
]

url = uploader.upload_data(
    data=data,
    worksheet_name='Products',
    mode='replace'
)
```

## Customization Guide

### 1. Customizing the Scraper

The most important method to customize is `parse_data()`. This is where you define what data to extract:

```python
def parse_data(self, soup: BeautifulSoup) -> List[Dict]:
    data = []

    # Find all product containers
    products = soup.find_all('div', class_='product-card')

    for product in products:
        try:
            # Extract specific fields
            title = product.find('h3', class_='product-title')
            price = product.find('span', class_='price')
            rating = product.find('div', class_='rating')

            data.append({
                'title': title.text.strip() if title else '',
                'price': price.text.strip() if price else '',
                'rating': rating.text.strip() if rating else '',
                'scraped_at': datetime.now().isoformat()
            })
        except Exception as e:
            self.logger.warning(f"Error parsing product: {e}")
            continue

    return data
```

### 2. Handling Different HTML Structures

Use Chrome DevTools or Firefox Inspector to find the right selectors:

1. Right-click on the element you want to scrape
2. Select "Inspect" or "Inspect Element"
3. Look at the HTML structure and identify unique classes or IDs
4. Use BeautifulSoup methods to extract data:
   - `find()` - finds the first matching element
   - `find_all()` - finds all matching elements
   - `select()` - uses CSS selectors
   - `select_one()` - finds first element matching CSS selector

### 3. Handling Pagination

If the website uses URL parameters for pagination:

```python
# Format: https://example.com?page=1
data = scraper.scrape_with_pagination(
    start_page=1,
    max_pages=10,
    page_param='page'
)
```

If pagination uses different URLs:

```python
urls = [f"https://example.com/products/page/{i}" for i in range(1, 11)]
data = scraper.scrape_multiple_pages(urls)
```

### 4. Custom Headers

Some websites require specific headers:

```python
custom_headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://example.com'
}

scraper = ScraperWithUpload(
    base_url="https://example.com",
    credentials_file="credentials.json",
    headers=custom_headers
)
```

## Best Practices

### Ethical Scraping

1. **Check robots.txt**: Always check `https://example.com/robots.txt` to see what's allowed
2. **Use delays**: Add delays between requests to avoid overwhelming servers
3. **Respect rate limits**: Don't make too many requests in a short time
4. **Identify yourself**: Use a proper User-Agent header
5. **Check Terms of Service**: Make sure scraping is allowed

### Error Handling

The template includes logging by default. Check the logs for errors:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scraper.log'  # Save to file
)
```

### Performance

- Use `scrape_multiple_pages()` for known URLs
- Adjust the `delay` parameter based on server response
- Consider using threading for large-scale scraping (not included in template)

## Troubleshooting

### Google Sheets Authentication Error

**Error**: `google.auth.exceptions.DefaultCredentialsError`

**Solution**: Make sure `credentials.json` is in the correct location and properly formatted.

### Permission Denied on Spreadsheet

**Error**: `gspread.exceptions.APIError: PERMISSION_DENIED`

**Solution**: Share the spreadsheet with the service account email found in `credentials.json`.

### No Data Scraped

**Possible causes**:
1. Website structure changed - update your selectors in `parse_data()`
2. Website requires JavaScript - consider using Selenium instead
3. Website blocks bots - try different User-Agent headers

### Rate Limiting

**Error**: `429 Too Many Requests`

**Solution**: Increase the `delay` parameter between requests.

## Advanced Features

### Using Selenium for JavaScript-Heavy Sites

For websites that load content with JavaScript, you'll need Selenium:

```bash
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://example.com")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.quit()
```

### Scheduling with Cron (Linux/Mac)

To run the scraper automatically:

```bash
# Edit crontab
crontab -e

# Run every day at 9 AM
0 9 * * * cd /path/to/project && /usr/bin/python3 scrape_and_upload.py
```

### Scheduling with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, weekly, etc.)
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `scrape_and_upload.py`
7. Start in: Your project directory

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use this template for your projects.

## Disclaimer

This tool is for educational purposes. Always ensure you have permission to scrape a website and comply with their terms of service and robots.txt file. The authors are not responsible for any misuse of this tool.

## Support

For issues and questions:
1. Check the Troubleshooting section above
2. Review the code comments in the source files
3. Open an issue on GitHub

## Changelog

### Version 1.0.0
- Initial release
- Basic web scraping functionality
- Google Sheets integration
- Support for single page, multiple pages, and pagination
- CSV and JSON export options
