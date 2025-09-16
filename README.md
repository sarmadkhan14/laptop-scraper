# Laptop Scraper with Google Sheets Integration

An automated web scraper that extracts laptop product data from an e-commerce test site and uploads it to Google Sheets using Python, Selenium, and Google Sheets API.

## Features

- Scrapes product information (name, price, description, URL) from 100 laptop listings
- Automatically creates timestamped sheets in Google Sheets
- Implements robust error handling and logging
- Includes pagination support for scalability
- Secure credential management using environment variables

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Google Cloud Platform account with Sheets API enabled
- Service account with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/laptop-scraper.git
cd laptop-scraper
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
```

3. Set up Google Sheets API:
   - Enable Google Sheets API in Google Cloud Console
   - Create a service account and download the JSON key
   - Place the JSON file in `credentials/` folder as `service_account.json`
   - Share your target Google Sheet with the service account email

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your Google Sheets ID and credentials path

## Usage

Run the scraper:
```bash
python -m src.main
```

The script will:
1. Launch Chrome browser (can run headless)
2. Navigate to the target website
3. Extract product data for 100 laptops
4. Create a new timestamped sheet in your Google Sheets
5. Upload all data with extraction timestamps

## Project Structure

laptop-scraper/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── scraper.py        # Web scraping logic
│   └── sheets_handler.py # Google Sheets API integration
├── credentials/          # Service account JSON (not tracked)
├── logs/                # Execution logs
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
└── README.md


## Output

The scraper creates a Google Sheet with the following columns:
- Product Name
- Price
- Description
- Product URL
- Extraction Timestamp
- Page Number
- Product Rank

## Security

- API credentials are stored securely and never committed to version control
- `.gitignore` configured to exclude sensitive files
- Environment variables used for configuration

## Technologies Used

- **Python 3.11** - Core programming language
- **Selenium WebDriver** - Web scraping automation
- **Google Sheets API** - Data storage
- **python-dotenv** - Environment variable management

## Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues
- Missing page elements
- API authentication failures
- Rate limiting

## Logging

Detailed logs are saved to `logs/` directory with timestamps for debugging and monitoring.

## Author

Sarmad Ullah Khan Sherwani

## License

This project is created for assessment purposes.

