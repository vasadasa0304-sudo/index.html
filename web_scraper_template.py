"""
Web Scraper Template with Google Sheets Integration
=====================================================
This template provides a flexible foundation for scraping websites without APIs
and uploading the data to Google Sheets.

Author: Web Scraping Template
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json


class WebScraperTemplate:
    """
    A flexible web scraper template that can be customized for different websites.
    """

    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """
        Initialize the web scraper.

        Args:
            base_url: The base URL of the website to scrape
            headers: Optional custom headers for requests
        """
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url: str, delay: float = 1.0) -> Optional[BeautifulSoup]:
        """
        Fetch a webpage and return BeautifulSoup object.

        Args:
            url: URL to fetch
            delay: Delay between requests (in seconds) to be respectful

        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            time.sleep(delay)  # Be respectful to the server
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def parse_data(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse data from the BeautifulSoup object.
        THIS METHOD SHOULD BE CUSTOMIZED FOR YOUR SPECIFIC WEBSITE.

        Args:
            soup: BeautifulSoup object containing the page HTML

        Returns:
            List of dictionaries containing scraped data
        """
        # EXAMPLE IMPLEMENTATION - CUSTOMIZE THIS FOR YOUR NEEDS
        data = []

        # Example: Scraping a list of items
        # Change the selector based on your target website
        items = soup.find_all('div', class_='item')

        for item in items:
            try:
                # Example data extraction - CUSTOMIZE THESE SELECTORS
                title = item.find('h2', class_='title')
                description = item.find('p', class_='description')
                price = item.find('span', class_='price')
                link = item.find('a', class_='link')

                data.append({
                    'title': title.text.strip() if title else '',
                    'description': description.text.strip() if description else '',
                    'price': price.text.strip() if price else '',
                    'link': link.get('href') if link else '',
                    'scraped_at': datetime.now().isoformat()
                })
            except Exception as e:
                self.logger.warning(f"Error parsing item: {e}")
                continue

        return data

    def scrape_multiple_pages(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        Scrape multiple pages and combine the results.

        Args:
            urls: List of URLs to scrape
            delay: Delay between requests

        Returns:
            Combined list of scraped data from all pages
        """
        all_data = []

        for url in urls:
            soup = self.fetch_page(url, delay)
            if soup:
                page_data = self.parse_data(soup)
                all_data.extend(page_data)
                self.logger.info(f"Scraped {len(page_data)} items from {url}")
            else:
                self.logger.warning(f"Failed to scrape {url}")

        return all_data

    def scrape_with_pagination(self, start_page: int = 1, max_pages: int = 10,
                               page_param: str = 'page', delay: float = 1.0) -> List[Dict]:
        """
        Scrape pages with pagination.

        Args:
            start_page: Starting page number
            max_pages: Maximum number of pages to scrape
            page_param: Query parameter name for pagination (e.g., 'page', 'p')
            delay: Delay between requests

        Returns:
            Combined list of scraped data from all pages
        """
        all_data = []

        for page_num in range(start_page, start_page + max_pages):
            url = f"{self.base_url}?{page_param}={page_num}"
            soup = self.fetch_page(url, delay)

            if soup:
                page_data = self.parse_data(soup)
                if not page_data:  # Stop if no more data found
                    self.logger.info(f"No data found on page {page_num}. Stopping.")
                    break
                all_data.extend(page_data)
                self.logger.info(f"Scraped {len(page_data)} items from page {page_num}")
            else:
                self.logger.warning(f"Failed to scrape page {page_num}")

        return all_data

    def save_to_csv(self, data: List[Dict], filename: str = 'scraped_data.csv'):
        """
        Save scraped data to CSV file.

        Args:
            data: List of dictionaries containing scraped data
            filename: Output filename
        """
        if not data:
            self.logger.warning("No data to save")
            return

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        self.logger.info(f"Data saved to {filename}")

    def save_to_json(self, data: List[Dict], filename: str = 'scraped_data.json'):
        """
        Save scraped data to JSON file.

        Args:
            data: List of dictionaries containing scraped data
            filename: Output filename
        """
        if not data:
            self.logger.warning("No data to save")
            return

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Data saved to {filename}")


def example_usage():
    """
    Example usage of the WebScraperTemplate class.
    CUSTOMIZE THIS FOR YOUR SPECIFIC SCRAPING NEEDS.
    """
    # Example configuration
    base_url = "https://example.com/products"

    # Initialize scraper
    scraper = WebScraperTemplate(base_url)

    # Option 1: Scrape a single page
    soup = scraper.fetch_page(base_url)
    if soup:
        data = scraper.parse_data(soup)
        scraper.save_to_csv(data)

    # Option 2: Scrape multiple specific URLs
    # urls = [
    #     "https://example.com/page1",
    #     "https://example.com/page2",
    #     "https://example.com/page3"
    # ]
    # data = scraper.scrape_multiple_pages(urls, delay=1.0)
    # scraper.save_to_csv(data)

    # Option 3: Scrape with pagination
    # data = scraper.scrape_with_pagination(
    #     start_page=1,
    #     max_pages=5,
    #     page_param='page',
    #     delay=1.0
    # )
    # scraper.save_to_csv(data)


if __name__ == "__main__":
    example_usage()
