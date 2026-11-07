"""
Production-Ready Web Scraper Template (Fedora & Linux Compatible)
Author: Web Scraping Study Guide
Description: Navigates a dynamic site, extracts structured content, handles pagination, 
             and exports results into structured formats (CSV & JSON).
"""

import logging
import json
import time
from typing import List, Dict, Any

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class WebScraper:
    def __init__(self, headless: bool = False):
        """Initializes the browser driver using modern Selenium Manager."""
        self.options = Options()
        
        if headless:
            self.options.add_argument("--headless=new")  # Modern headless mode
            
        # Hardening against basic scraper detection and container limitations
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Selenium Manager automatically detects Chromium/Chrome and matches the driver
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.scraped_data: List[Dict[str, Any]] = []

    def navigate_to(self, url: str) -> None:
        """Navigates to the specified URL."""
        logging.info(f"Navigating to {url}")
        self.driver.get(url)

    def scroll_to_bottom(self, pause_time: float = 1.5) -> None:
        """Scrolls down incrementally to trigger dynamic JavaScript/lazy loading."""
        logging.info("Scrolling down page to trigger dynamic load...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_page_data(self) -> None:
        """Waits for target container and extracts structured elements."""
        try:
            # Explicit Wait: Wait until parent cards are present on the DOM
            cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quote"))
            )
            
            for card in cards:
                try:
                    text = card.find_element(By.CSS_SELECTOR, ".text").text.strip()
                    author = card.find_element(By.CSS_SELECTOR, ".author").text.strip()
                    
                    tag_elements = card.find_elements(By.CSS_SELECTOR, ".tags .tag")
                    tags = [tag.text.strip() for tag in tag_elements]

                    item = {
                        "quote": text,
                        "author": author,
                        "tags": ", ".join(tags)
                    }
                    self.scraped_data.append(item)
                except NoSuchElementException as e:
                    logging.warning(f"Failed to parse child element inside card: {e}")
                    continue

        except TimeoutException:
            logging.error("Timed out waiting for quotes containers to load.")

    def handle_pagination(self, max_pages: int = 3) -> None:
        """Iterates through paginated pages using safe button clicking."""
        current_page = 1
        
        while current_page <= max_pages:
            logging.info(f"Extracting data from page {current_page}...")
            self.extract_page_data()
            
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, "li.next > a")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(0.5)
                
                next_button.click()
                current_page += 1
                
            except (NoSuchElementException, ElementClickInterceptedException):
                logging.info("No more pages available or Next button unclickable. Exiting loop.")
                break

    def export_data(self, base_filename: str = "output") -> None:
        """Exports gathered data to JSON and CSV formats using Pandas."""
        if not self.scraped_data:
            logging.warning("No data was collected to export.")
            return

        json_path = f"{base_filename}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.scraped_data, f, indent=4, ensure_ascii=False)
        logging.info(f"Successfully saved {len(self.scraped_data)} items to {json_path}")

        df = pd.DataFrame(self.scraped_data)
        csv_path = f"{base_filename}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logging.info(f"Successfully saved CSV report to {csv_path}")

    def close(self) -> None:
        """Gracefully closes browser session and driver process."""
        logging.info("Tearing down driver connection...")
        self.driver.quit()

# Execution Pipeline
if __name__ == "__main__":
    TARGET_URL = "https://quotes.toscrape.com/"
    
    # Set headless=False if you want to watch the browser pop up and work live
    scraper = WebScraper(headless=False)
    try:
        scraper.navigate_to(TARGET_URL)
        scraper.handle_pagination(max_pages=2)
        scraper.export_data(base_filename="quotes_dataset")
    finally:
        scraper.close()