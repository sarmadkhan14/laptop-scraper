import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
from typing import List, Dict

class GoogleSheetsHandler:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """Initialize Google Sheets API client"""
        self.spreadsheet_id = spreadsheet_id
        
        # Load credentials securely
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
            
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        self.service = build('sheets', 'v4', credentials=self.creds)
        logging.info("Google Sheets handler initialized")
        
    def create_sheet(self, sheet_name: str) -> None:
        """Create a new sheet in the spreadsheet"""
        try:
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': [request]}
            ).execute()
            
            logging.info(f"Created new sheet: {sheet_name}")
            
        except Exception as e:
            if 'already exists' in str(e):
                logging.info(f"Sheet {sheet_name} already exists, will append to it")
            else:
                raise
                
    def append_data(self, sheet_name: str, data: List[Dict]) -> None:
        """Append data to the specified sheet"""
        if not data:
            logging.warning("No data to append")
            return
            
        # Prepare headers
        headers = [['Product Name', 'Price', 'Description', 'Product URL', 'Extraction Timestamp', 'Page Number', 'Product Rank']]
        
        # Prepare values
        values = headers + [
            [
                item.get('product_name', ''),
                item.get('price', ''),
                item.get('description', ''),
                item.get('product_url', ''),
                item.get('extraction_timestamp', ''),
                item.get('page_number', ''),
                item.get('product_rank', '')
            ]
            for item in data
        ]
        
        # Append to sheet
        body = {'values': values}
        
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption='RAW',
            body=body
        ).execute()
        
        logging.info(f"Appended {result.get('updates', {}).get('updatedRows', 0)} rows to {sheet_name}")