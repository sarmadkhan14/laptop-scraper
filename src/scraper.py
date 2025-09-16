from selenium import webdriver # launches and controls the browser (Chrome here).
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from datetime import datetime
from typing import List, Dict
import time

class LaptopScraper:
    def __init__(self, headless: bool = True):
        """Initialize scraper with Chrome driver"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
        logging.info("Scraper initialized")
        
    def scrape_products(self, num_products: int = 100) -> List[Dict]:
        """
        Scrape laptop products from the website
        
        Args:
            num_products: Number of products to scrape (default 100)
            
        Returns:
            List of product dictionaries
        """
        products = []
        page = 1
        
        try:
            while len(products) < num_products:
                # Construct URL (keeping pagination logic for scalability)
                url = f"{self.base_url}?page={page}" if page > 1 else self.base_url
                logging.info(f"Scraping page {page}: {url}")
                self.driver.get(url)
                
                # Wait for products to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "thumbnail"))
                )
                
                # Small delay to ensure all elements are loaded
                time.sleep(1)
                
                # Extract all product containers
                items = self.driver.find_elements(By.CLASS_NAME, "thumbnail")
                logging.info(f"Found {len(items)} products on page {page}")
                
                if not items:
                    logging.warning(f"No products found on page {page}")
                    break
                
                for item in items:
                    if len(products) >= num_products:
                        break
                        
                    try:
                        # Extract product details
                        name_elem = item.find_element(By.CLASS_NAME, "title")
                        name = name_elem.get_attribute("title") or name_elem.text
                        
                        price = item.find_element(By.CLASS_NAME, "price").text
                        
                        # Extract additional useful information
                        try:
                            description = item.find_element(By.CLASS_NAME, "description").text
                        except:
                            description = "N/A"
                        
                        # Get product link if available
                        try:
                            link_elem = item.find_element(By.TAG_NAME, "a")
                            product_url = link_elem.get_attribute("href")
                        except:
                            product_url = "N/A"
                        
                        products.append({
                            'product_name': name,
                            'price': price,
                            'description': description[:100] + "..." if len(description) > 100 else description,
                            'product_url': product_url,
                            'extraction_timestamp': datetime.now().isoformat(),
                            'page_number': page,
                            'product_rank': len(products) + 1
                        })
                        
                    except Exception as e:
                        logging.warning(f"Error extracting product {len(products) + 1}: {e}")
                        continue
                
                # Check for pagination (next button or load more)
                try:
                    # Look for pagination controls
                    next_button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'next') or contains(text(), 'Next')]")
                    if next_button.is_enabled():
                        page += 1
                    else:
                        logging.info("No more pages available")
                        break
                except:
                    # No pagination found, all products are on single page
                    logging.info("No pagination found - all products on single page")
                    break
                    
        except Exception as e:
            logging.error(f"Critical scraping error: {e}")
            raise
        finally:
            self.driver.quit()
            logging.info(f"Scraping completed. Extracted {len(products)} products")
            
        return products[:num_products]
    
    def __enter__(self):
        """Context manager entry"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure driver is closed"""
        if self.driver:
            self.driver.quit()