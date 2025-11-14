"""
Simple Runner Script Using Configuration File
==============================================
This script uses settings from config.py to run the scraper.
1. Copy config.example.py to config.py
2. Customize config.py for your needs
3. Run this script: python run_scraper.py
"""

import logging
import sys
from scrape_and_upload import ScraperWithUpload

# Try to import config
try:
    import config
except ImportError:
    print("ERROR: config.py not found!")
    print("Please copy config.example.py to config.py and customize it.")
    print("Command: cp config.example.py config.py")
    sys.exit(1)


def setup_logging():
    """Setup logging based on config."""
    log_config = {
        'level': getattr(logging, config.LOG_LEVEL, logging.INFO),
        'format': '%(asctime)s - %(levelname)s - %(message)s'
    }

    if config.LOG_TO_FILE:
        log_config['filename'] = config.LOG_FILENAME

    logging.basicConfig(**log_config)


def main():
    """Main function to run the scraper."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Starting Web Scraper")
    logger.info("=" * 60)

    try:
        # Initialize scraper
        logger.info(f"Initializing scraper for: {config.BASE_URL}")
        scraper = ScraperWithUpload(
            base_url=config.BASE_URL,
            credentials_file=config.CREDENTIALS_FILE,
            headers=config.CUSTOM_HEADERS
        )

        # Prepare scraping arguments based on method
        scrape_kwargs = {}

        if config.SCRAPE_METHOD == 'multiple':
            scrape_kwargs['urls'] = config.URLS_TO_SCRAPE
            scrape_kwargs['delay'] = config.REQUEST_DELAY
        elif config.SCRAPE_METHOD == 'pagination':
            scrape_kwargs.update(config.PAGINATION_CONFIG)
            scrape_kwargs['delay'] = config.REQUEST_DELAY

        # Run scraper
        logger.info(f"Scraping method: {config.SCRAPE_METHOD}")
        spreadsheet_url = scraper.scrape_and_upload(
            spreadsheet_id=config.SPREADSHEET_ID,
            worksheet_name=config.WORKSHEET_NAME,
            mode=config.UPLOAD_MODE,
            scrape_method=config.SCRAPE_METHOD,
            **scrape_kwargs
        )

        if spreadsheet_url:
            logger.info("=" * 60)
            logger.info("SUCCESS!")
            logger.info(f"Data uploaded to Google Sheets: {spreadsheet_url}")
            logger.info("=" * 60)
            print(f"\n✓ Success! View your data at: {spreadsheet_url}\n")

            # Optionally save local copies
            if config.SAVE_CSV or config.SAVE_JSON:
                logger.info("Saving local copies...")

                # Get the data again for local saving
                soup = scraper.fetch_page(config.BASE_URL)
                if soup:
                    data = scraper.parse_data(soup)

                    if config.SAVE_CSV:
                        scraper.save_to_csv(data, config.CSV_FILENAME)
                        logger.info(f"Saved to {config.CSV_FILENAME}")

                    if config.SAVE_JSON:
                        scraper.save_to_json(data, config.JSON_FILENAME)
                        logger.info(f"Saved to {config.JSON_FILENAME}")
        else:
            logger.error("Failed to upload data to Google Sheets")
            print("\n✗ Failed to upload data. Check the logs for details.\n")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n✗ Error: {e}")
        print("Make sure credentials.json exists in the project directory.\n")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        print("Check the logs for more details.\n")


if __name__ == "__main__":
    main()
