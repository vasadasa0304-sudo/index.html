"""
Complete Web Scraping and Google Sheets Upload Script
=====================================================
This script combines the web scraper template with Google Sheets uploader
to provide a complete solution for scraping and uploading data.
"""

from web_scraper_template import WebScraperTemplate
from google_sheets_uploader import GoogleSheetsUploader
import logging
from typing import Optional


class ScraperWithUpload(WebScraperTemplate):
    """
    Extended scraper class that includes Google Sheets upload functionality.
    """

    def __init__(self, base_url: str, credentials_file: str, headers: Optional[dict] = None):
        """
        Initialize the scraper with Google Sheets integration.

        Args:
            base_url: The base URL of the website to scrape
            credentials_file: Path to Google service account credentials JSON
            headers: Optional custom headers for requests
        """
        super().__init__(base_url, headers)
        self.uploader = GoogleSheetsUploader(credentials_file)

    def scrape_and_upload(self, spreadsheet_id: Optional[str] = None,
                         worksheet_name: str = 'Scraped Data',
                         mode: str = 'replace',
                         scrape_method: str = 'single',
                         **scrape_kwargs) -> str:
        """
        Scrape data and upload it to Google Sheets in one operation.

        Args:
            spreadsheet_id: ID of existing spreadsheet (creates new if None)
            worksheet_name: Name of the worksheet
            mode: 'replace' or 'append'
            scrape_method: 'single', 'multiple', or 'pagination'
            **scrape_kwargs: Additional arguments for the scraping method

        Returns:
            URL of the Google Spreadsheet
        """
        # Scrape data based on method
        if scrape_method == 'single':
            url = scrape_kwargs.get('url', self.base_url)
            soup = self.fetch_page(url)
            if soup:
                data = self.parse_data(soup)
            else:
                self.logger.error("Failed to fetch page")
                return ""

        elif scrape_method == 'multiple':
            urls = scrape_kwargs.get('urls', [])
            delay = scrape_kwargs.get('delay', 1.0)
            data = self.scrape_multiple_pages(urls, delay)

        elif scrape_method == 'pagination':
            start_page = scrape_kwargs.get('start_page', 1)
            max_pages = scrape_kwargs.get('max_pages', 10)
            page_param = scrape_kwargs.get('page_param', 'page')
            delay = scrape_kwargs.get('delay', 1.0)
            data = self.scrape_with_pagination(start_page, max_pages, page_param, delay)

        else:
            self.logger.error(f"Invalid scrape_method: {scrape_method}")
            return ""

        # Upload to Google Sheets
        if data:
            self.logger.info(f"Scraped {len(data)} items. Uploading to Google Sheets...")
            spreadsheet_url = self.uploader.upload_data(
                data=data,
                spreadsheet_id=spreadsheet_id,
                worksheet_name=worksheet_name,
                mode=mode
            )

            # Apply formatting
            if spreadsheet_url:
                try:
                    # Extract spreadsheet ID from URL
                    sheet_id = spreadsheet_url.split('/d/')[1].split('/')[0]
                    self.uploader.format_worksheet(sheet_id, worksheet_name)
                except Exception as e:
                    self.logger.warning(f"Could not apply formatting: {e}")

            return spreadsheet_url
        else:
            self.logger.warning("No data scraped. Nothing to upload.")
            return ""


def main():
    """
    Main function demonstrating usage.
    CUSTOMIZE THIS FOR YOUR SPECIFIC NEEDS.
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Configuration
    BASE_URL = "https://example.com"  # CHANGE THIS
    CREDENTIALS_FILE = "credentials.json"  # Path to your Google credentials
    SPREADSHEET_ID = None  # Set to existing spreadsheet ID or None to create new

    # Initialize scraper with Google Sheets integration
    scraper = ScraperWithUpload(BASE_URL, CREDENTIALS_FILE)

    # Example 1: Scrape single page and upload
    print("\n=== Example 1: Single Page Scrape ===")
    url = scraper.scrape_and_upload(
        spreadsheet_id=SPREADSHEET_ID,
        worksheet_name='Single Page Data',
        mode='replace',
        scrape_method='single',
        url=BASE_URL
    )
    if url:
        print(f"✓ Data uploaded to: {url}")

    # Example 2: Scrape multiple pages and upload
    # print("\n=== Example 2: Multiple Pages Scrape ===")
    # urls = [
    #     "https://example.com/page1",
    #     "https://example.com/page2",
    #     "https://example.com/page3"
    # ]
    # url = scraper.scrape_and_upload(
    #     spreadsheet_id=SPREADSHEET_ID,
    #     worksheet_name='Multiple Pages Data',
    #     mode='replace',
    #     scrape_method='multiple',
    #     urls=urls,
    #     delay=1.0
    # )
    # if url:
    #     print(f"✓ Data uploaded to: {url}")

    # Example 3: Scrape with pagination and upload
    # print("\n=== Example 3: Pagination Scrape ===")
    # url = scraper.scrape_and_upload(
    #     spreadsheet_id=SPREADSHEET_ID,
    #     worksheet_name='Paginated Data',
    #     mode='replace',
    #     scrape_method='pagination',
    #     start_page=1,
    #     max_pages=5,
    #     page_param='page',
    #     delay=1.0
    # )
    # if url:
    #     print(f"✓ Data uploaded to: {url}")


if __name__ == "__main__":
    main()
