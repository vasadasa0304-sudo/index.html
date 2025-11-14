"""
Google Sheets Uploader Module
==============================
This module handles uploading scraped data to Google Sheets.
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import List, Dict, Optional
import logging


class GoogleSheetsUploader:
    """
    Handles uploading data to Google Sheets using service account credentials.
    """

    def __init__(self, credentials_file: str):
        """
        Initialize the Google Sheets uploader.

        Args:
            credentials_file: Path to the Google service account JSON credentials file
        """
        self.credentials_file = credentials_file
        self.logger = logging.getLogger(__name__)

        # Define the scopes
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        # Authenticate and initialize client
        try:
            self.creds = Credentials.from_service_account_file(
                credentials_file,
                scopes=self.scopes
            )
            self.client = gspread.authorize(self.creds)
            self.logger.info("Successfully authenticated with Google Sheets")
        except Exception as e:
            self.logger.error(f"Error authenticating with Google Sheets: {e}")
            raise

    def create_spreadsheet(self, title: str, share_with: Optional[str] = None) -> gspread.Spreadsheet:
        """
        Create a new Google Spreadsheet.

        Args:
            title: Title for the new spreadsheet
            share_with: Email address to share the spreadsheet with (optional)

        Returns:
            The created spreadsheet object
        """
        try:
            spreadsheet = self.client.create(title)
            self.logger.info(f"Created spreadsheet: {title}")

            if share_with:
                spreadsheet.share(share_with, perm_type='user', role='writer')
                self.logger.info(f"Shared spreadsheet with {share_with}")

            return spreadsheet
        except Exception as e:
            self.logger.error(f"Error creating spreadsheet: {e}")
            raise

    def open_spreadsheet(self, spreadsheet_id: Optional[str] = None,
                        title: Optional[str] = None) -> gspread.Spreadsheet:
        """
        Open an existing spreadsheet by ID or title.

        Args:
            spreadsheet_id: The spreadsheet ID (from URL)
            title: The spreadsheet title

        Returns:
            The opened spreadsheet object
        """
        try:
            if spreadsheet_id:
                spreadsheet = self.client.open_by_key(spreadsheet_id)
                self.logger.info(f"Opened spreadsheet by ID: {spreadsheet_id}")
            elif title:
                spreadsheet = self.client.open(title)
                self.logger.info(f"Opened spreadsheet by title: {title}")
            else:
                raise ValueError("Either spreadsheet_id or title must be provided")

            return spreadsheet
        except Exception as e:
            self.logger.error(f"Error opening spreadsheet: {e}")
            raise

    def upload_data(self, data: List[Dict], spreadsheet_id: Optional[str] = None,
                   title: Optional[str] = None, worksheet_name: str = 'Sheet1',
                   mode: str = 'replace') -> str:
        """
        Upload data to a Google Spreadsheet.

        Args:
            data: List of dictionaries containing the data to upload
            spreadsheet_id: ID of existing spreadsheet (optional)
            title: Title of existing spreadsheet (optional)
            worksheet_name: Name of the worksheet to write to
            mode: 'replace' to replace existing data, 'append' to add new rows

        Returns:
            URL of the spreadsheet
        """
        if not data:
            self.logger.warning("No data to upload")
            return ""

        try:
            # Open or create spreadsheet
            if spreadsheet_id or title:
                spreadsheet = self.open_spreadsheet(spreadsheet_id, title)
            else:
                spreadsheet = self.create_spreadsheet(f"Scraped Data - {pd.Timestamp.now()}")

            # Get or create worksheet
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
                self.logger.info(f"Created new worksheet: {worksheet_name}")

            # Convert data to DataFrame
            df = pd.DataFrame(data)

            if mode == 'replace':
                # Clear existing data and write new data
                worksheet.clear()
                worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                self.logger.info(f"Replaced data in worksheet '{worksheet_name}' with {len(data)} rows")
            elif mode == 'append':
                # Append new data
                worksheet.append_rows(df.values.tolist())
                self.logger.info(f"Appended {len(data)} rows to worksheet '{worksheet_name}'")
            else:
                raise ValueError(f"Invalid mode: {mode}. Use 'replace' or 'append'")

            spreadsheet_url = spreadsheet.url
            self.logger.info(f"Data uploaded successfully. Spreadsheet URL: {spreadsheet_url}")
            return spreadsheet_url

        except Exception as e:
            self.logger.error(f"Error uploading data: {e}")
            raise

    def batch_upload_to_multiple_sheets(self, data: List[Dict],
                                       spreadsheet_id: str,
                                       sheet_mappings: Dict[str, List[str]]):
        """
        Upload different columns to different worksheets in the same spreadsheet.

        Args:
            data: List of dictionaries containing the data
            spreadsheet_id: ID of the spreadsheet
            sheet_mappings: Dict mapping worksheet names to lists of column names
                          e.g., {'Products': ['name', 'price'], 'Details': ['description']}
        """
        try:
            spreadsheet = self.open_spreadsheet(spreadsheet_id=spreadsheet_id)
            df = pd.DataFrame(data)

            for sheet_name, columns in sheet_mappings.items():
                # Filter dataframe to only include specified columns
                sheet_df = df[columns]

                # Get or create worksheet
                try:
                    worksheet = spreadsheet.worksheet(sheet_name)
                except gspread.exceptions.WorksheetNotFound:
                    worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

                # Upload data
                worksheet.clear()
                worksheet.update([sheet_df.columns.values.tolist()] + sheet_df.values.tolist())
                self.logger.info(f"Uploaded data to worksheet '{sheet_name}'")

        except Exception as e:
            self.logger.error(f"Error in batch upload: {e}")
            raise

    def format_worksheet(self, spreadsheet_id: str, worksheet_name: str = 'Sheet1'):
        """
        Apply basic formatting to a worksheet (freeze header, bold header, etc.).

        Args:
            spreadsheet_id: ID of the spreadsheet
            worksheet_name: Name of the worksheet to format
        """
        try:
            spreadsheet = self.open_spreadsheet(spreadsheet_id=spreadsheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)

            # Format header row (bold, freeze)
            worksheet.format('1:1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })

            # Freeze the header row
            worksheet.freeze(rows=1)

            self.logger.info(f"Applied formatting to worksheet '{worksheet_name}'")

        except Exception as e:
            self.logger.error(f"Error formatting worksheet: {e}")
            raise


def example_usage():
    """
    Example usage of the GoogleSheetsUploader class.
    """
    # Sample scraped data
    sample_data = [
        {'name': 'Product 1', 'price': '$10.99', 'description': 'A great product'},
        {'name': 'Product 2', 'price': '$15.99', 'description': 'Another great product'},
        {'name': 'Product 3', 'price': '$20.99', 'description': 'The best product'},
    ]

    # Initialize uploader with credentials file
    uploader = GoogleSheetsUploader('credentials.json')

    # Upload data (will create a new spreadsheet)
    spreadsheet_url = uploader.upload_data(
        data=sample_data,
        worksheet_name='Scraped Products',
        mode='replace'
    )

    print(f"Data uploaded to: {spreadsheet_url}")

    # Or upload to an existing spreadsheet
    # uploader.upload_data(
    #     data=sample_data,
    #     spreadsheet_id='your-spreadsheet-id-here',
    #     worksheet_name='Sheet1',
    #     mode='append'
    # )


if __name__ == "__main__":
    example_usage()
