# Quick Start Guide

Get your web scraper running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Google Sheets Credentials

### Option A: Quick Setup (Recommended for Beginners)

1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable these APIs:
   - Google Sheets API
   - Google Drive API
4. Create a Service Account:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Download the JSON key file
   - Rename it to `credentials.json` and put it in this folder

### Option B: Detailed Setup

See the main [README.md](README.md#step-2-create-service-account-credentials) for detailed instructions.

## Step 3: Configure Your Scraper

```bash
# Copy the example config
cp config.example.py config.py
```

Edit `config.py` and change these settings:

```python
# The website you want to scrape
BASE_URL = "https://yourwebsite.com"

# Path to your credentials (from Step 2)
CREDENTIALS_FILE = "credentials.json"

# Name for your worksheet
WORKSHEET_NAME = "My Scraped Data"
```

## Step 4: Customize for Your Website

Open `web_scraper_template.py` and find the `parse_data()` method (around line 61).

**How to find the right selectors:**

1. Open your target website in Chrome
2. Right-click on the data you want → "Inspect"
3. Look for unique `class` or `id` attributes
4. Update the code:

```python
def parse_data(self, soup: BeautifulSoup) -> List[Dict]:
    data = []

    # Replace 'item' with your website's class
    items = soup.find_all('div', class_='product-card')  # ← Change this!

    for item in items:
        data.append({
            # Change these selectors to match your website
            'title': item.find('h2', class_='title').text.strip(),
            'price': item.find('span', class_='price').text.strip(),
            'scraped_at': datetime.now().isoformat()
        })

    return data
```

## Step 5: Share Your Spreadsheet (If Using Existing)

If you want to use an existing Google Sheet:

1. Open your Google Sheet
2. Click "Share"
3. Add the email from `credentials.json` (look for `client_email`)
4. Give it "Editor" access
5. Copy the spreadsheet ID from the URL and add to `config.py`:

```python
# From: https://docs.google.com/spreadsheets/d/ABC123XYZ/edit
SPREADSHEET_ID = "ABC123XYZ"
```

## Step 6: Run It!

```bash
python run_scraper.py
```

Or use the direct script:

```bash
python scrape_and_upload.py
```

## That's It!

You should see output like:

```
2024-01-15 10:30:15 - INFO - Fetching: https://example.com
2024-01-15 10:30:16 - INFO - Scraped 25 items
2024-01-15 10:30:17 - INFO - Data uploaded successfully

✓ Success! View your data at: https://docs.google.com/spreadsheets/d/...
```

## Common Issues

### "No module named 'config'"

Run: `cp config.example.py config.py`

### "File credentials.json not found"

Make sure you downloaded the credentials from Google Cloud Console (Step 2).

### "PERMISSION_DENIED"

Share your spreadsheet with the service account email from `credentials.json`.

### "No data scraped"

Your selectors might be wrong. Check Step 4 again and inspect the website's HTML structure.

## Next Steps

- Read the full [README.md](README.md) for advanced features
- Learn about pagination, multiple pages, and more
- Add error handling and scheduling

## Need Help?

1. Check the [README.md](README.md) Troubleshooting section
2. Review your logs in `scraper.log`
3. Open an issue on GitHub

Happy scraping! 🚀
