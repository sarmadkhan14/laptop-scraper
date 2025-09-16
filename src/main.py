import os # Accesses operating system functions (getting environment variables)
import logging # Creates detailed logs for debugging
from datetime import datetime # Generates timestamps for file names
from dotenv import load_dotenv # Loads variables from .env file (keeps secrets secure)
from src.scraper import LaptopScraper # Calls scrapper.py from src folder
from src.sheets_handler import GoogleSheetsHandler # Calls sheet_handler.py from src folder


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/scraper_{datetime.now():%Y%m%d_%H%M%S}.log'), 
        logging.StreamHandler() # Prints logs to console (real-time monitoring) 
    ]
)

def main():
    """Main execution function"""
    load_dotenv()
    
    # Configuration
    SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_ID')
    CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')
    NUM_PRODUCTS = 100 # Hardcoded value based on requirement document
    
    try:
        # Step 1: Scrape products
        logging.info(f"Starting scraper for {NUM_PRODUCTS} products")
        scraper = LaptopScraper(headless=False)  # Set to True for production
        products = scraper.scrape_products(num_products=NUM_PRODUCTS)
        
        if not products:
            logging.error("No products scraped")
            return
            
        logging.info(f"Successfully scraped {len(products)} products")
        
        # Step 2: Upload to Google Sheets
        logging.info("Initializing Google Sheets handler")
        sheets = GoogleSheetsHandler(CREDENTIALS_PATH, SPREADSHEET_ID)
        
        # Create sheet with timestamp
        sheet_name = f"Laptop_Data_{datetime.now():%Y%m%d_%H%M%S}"
        sheets.create_sheet(sheet_name)
        
        # Append data
        logging.info(f"Uploading data to sheet: {sheet_name}")
        sheets.append_data(sheet_name, products)
        
        # Summary
        logging.info("=" * 50)
        logging.info("SCRAPING COMPLETED SUCCESSFULLY")
        logging.info(f"Products scraped: {len(products)}")
        logging.info(f"Sheet name: {sheet_name}")
        logging.info(f"Spreadsheet ID: {SPREADSHEET_ID}")
        logging.info("=" * 50)
        
    except Exception as e:
        logging.error(f"Script failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()