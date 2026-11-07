# Python & Selenium Web Scraper Project

A robust, production-ready web scraper built with **Python**, **Selenium v4+** (utilizing Selenium Manager), and **Pandas**. Designed with built-in explicit waits, resilient error handling, automated pagination, and dual data exports (CSV & JSON).

---

## Project Directory Structure

```text
Scrapper/
│
├── venv/                 # Isolated Python virtual environment
├── scraper.py            # Main application script
├── README.md             # Project documentation and guide
├── quotes_dataset.csv    # Generated spreadsheet export
└── quotes_dataset.json   # Generated structured JSON export
```

---

## Prerequisites & System Dependencies

Because Selenium automates a real browser instance, your operating system needs a compatible browser installed.

* **Fedora Linux:**
  ```bash
  sudo dnf install chromium
  ```
* **Ubuntu / Debian Linux:**
  ```bash
  sudo apt install chromium-browser
  ```
* **macOS / Windows:** Ensure Google Chrome or Microsoft Edge is installed.

*(Note: Modern Selenium v4 includes **Selenium Manager**, which automatically detects your installed browser and manages matching driver binaries dynamically.)*

---

## Setup & Execution Guide

### 1. Activate the Virtual Environment
Ensure your virtual environment is active in your terminal:
```bash
source venv/bin/activate
```

### 2. Required Packages
Verify all required packages are installed inside `venv`:
```bash
pip install selenium pandas
```

### 3. Run the Scraper
Run the main script to start scraping and export data:
```bash
python scraper.py
```

---

## Key Features

1. **Selenium Manager Integration:** Automatically connects to system Chromium binaries without needing hardcoded paths.
2. **Explicit Waits (`WebDriverWait`):** Ensures elements are fully rendered before attempting extraction, avoiding race conditions.
3. **Resilient Exception Handling:** Gracefully handles missing elements, click intercepts, and timeouts without crashing.
4. **Pagination Loop:** Automatically scrolls, verifies, and navigates through multiple pages of content.
5. **Dual Exporting:** Leverages **Pandas** and native `json` modules to output structured `.csv` and `.json` datasets.