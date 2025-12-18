"""
LinkedIn Job Scraper - Integrated Main Script
Combines scraper with dataset fetcher to scrape all jobs from dataset
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException
)
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

import time
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path


# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# --- WEBDRIVER SETUP ---
def setup_driver():
    """
    Setup Chrome WebDriver with appropriate options
    
    Returns:
        WebDriver instance
    """
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Uncomment for headless mode
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        
        # Use webdriver-manager to automatically download and manage ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        logger.info("✅ WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize WebDriver: {str(e)}")
        logger.error("Make sure Chrome browser is installed")
        logger.error("Install webdriver-manager: pip install webdriver-manager")
        raise


# --- CONFIGURATION ---
class ScraperConfig:
    """Configuration settings for the LinkedIn scraper"""
    
    # Scraping parameters
    COUNTRIES = ["Egypt"]
    DATE_POSTED = "any"  # "any", "24h", "week", "month"
    WORKPLACE_TYPES = []  # ["1"]=On-site, ["2"]=Remote, ["3"]=Hybrid
    EXPERIENCE_LEVELS = []  # ["1"]=Internship, ["2"]=Entry, ["3"]=Associate, etc.
    
    # Scrolling and timing
    MAX_SCROLL_ATTEMPTS = 200
    SCROLL_PAUSE = 5
    DETAIL_PAUSE = 2
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 3
    
    # Output directory
    OUTPUT_DIR = "Data/Collected"
    DATASET_PATH = "dataset.json"
    
    # Browser options
    HEADLESS = False
    INCOGNITO = True
    
    # Limits (for testing)
    MAX_JOBS_PER_TITLE = None  # Set to number to limit, None for all


# --- DATA FETCHER ---
class DatasetFetcher:
    """Fetches job titles and domains from a JSON dataset"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.dataset = None
        
    def load_dataset(self) -> bool:
        """Load the dataset from JSON file"""
        try:
            if not Path(self.dataset_path).exists():
                logger.error(f"Dataset file not found: {self.dataset_path}")
                return False
            
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                self.dataset = json.load(f)
            
            logger.info(f"✅ Dataset loaded successfully from {self.dataset_path}")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in dataset file: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            return False
    
    def get_all_jobs_with_domains(self) -> List[Dict]:
        """Get all jobs with their domain information"""
        if not self.dataset:
            logger.warning("Dataset not loaded")
            return []
        
        all_jobs = []
        
        try:
            for domain in self.dataset:
                domain_name = domain.get("name", "")
                jobs = domain.get("jobs", [])
                
                for job in jobs:
                    job_name = job.get("name", "")
                    if job_name:
                        all_jobs.append({
                            "domain": domain_name,
                            "job_title": job_name
                        })
            
            logger.info(f"📋 Found {len(all_jobs)} jobs across {len(self.dataset)} domains")
            return all_jobs
            
        except Exception as e:
            logger.error(f"Error extracting all jobs: {str(e)}")
            return []


# --- HELPER FUNCTIONS ---

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def build_linkedin_url(
    keyword: str,
    location: str,
    exp_levels: List[str],
    workplace_types: List[str],
    date_posted: str
) -> str:
    """Build LinkedIn job search URL with filters"""
    exp_param = ",".join(exp_levels) if exp_levels else ""
    workplace_param = ",".join(workplace_types) if workplace_types else ""
    
    date_param = ""
    date_map = {
        "24h": "r86400",
        "week": "r604800",
        "month": "r2592000"
    }
    date_param = date_map.get(date_posted, "")

    url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(keyword)}&location={quote_plus(location)}"
    
    if exp_param:
        url += f"&f_E={exp_param}"
    if workplace_param:
        url += f"&f_WT={workplace_param}"
    if date_param:
        url += f"&f_TPR={date_param}"
    
    url += "&position=1&pageNum=0"
    return url


def scroll_page(driver, config: ScraperConfig) -> bool:
    """Scroll through LinkedIn job listings to load all results"""
    try:
        attempt = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        logger.info("Starting page scroll to load all job listings...")
        
        while attempt < config.MAX_SCROLL_ATTEMPTS:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(config.SCROLL_PAUSE)
            
            try:
                show_more_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "infinite-scroller__show-more-button"))
                )
                show_more_btn.click()
                logger.debug("Clicked 'Show more' button")
                time.sleep(config.SCROLL_PAUSE)
            except TimeoutException:
                pass
            except Exception as e:
                logger.debug(f"Error clicking 'Show more': {str(e)}")
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logger.info("Reached bottom of page")
                break
                
            last_height = new_height
            attempt += 1
            
        return True
        
    except Exception as e:
        logger.error(f"Error during page scrolling: {str(e)}")
        return False


def fetch_job_details(driver, job_url: str, config: ScraperConfig) -> Tuple[str, str]:
    """Fetch detailed job description and company info from job page"""
    job_desc = ""
    company_desc = ""
    
    if not job_url:
        return job_desc, company_desc
    
    for attempt in range(config.RETRY_ATTEMPTS):
        try:
            driver.get(job_url)
            time.sleep(config.DETAIL_PAUSE)
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "description__text"))
            )
            
            job_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            job_div = job_soup.find("div", class_="description__text")
            if job_div:
                job_desc = job_div.get_text(separator="\n", strip=True)
            
            company_div = job_soup.find("div", class_="show-more-less-html__markup")
            if company_div:
                company_desc = company_div.get_text(separator="\n", strip=True)
            
            return job_desc, company_desc
            
        except TimeoutException:
            logger.warning(f"Timeout loading job details (attempt {attempt + 1}/{config.RETRY_ATTEMPTS})")
            if attempt < config.RETRY_ATTEMPTS - 1:
                time.sleep(config.RETRY_DELAY)
            else:
                logger.error(f"Failed to load job details after {config.RETRY_ATTEMPTS} attempts: {job_url}")
                
        except Exception as e:
            logger.error(f"Error fetching job details (attempt {attempt + 1}): {str(e)}")
            if attempt < config.RETRY_ATTEMPTS - 1:
                time.sleep(config.RETRY_DELAY)
    
    return job_desc, company_desc


def extract_job_cards(html: str) -> List[BeautifulSoup]:
    """Extract job cards from page HTML"""
    try:
        soup = BeautifulSoup(html, "html.parser")
        job_cards = soup.find_all("div", class_="base-card")
        logger.info(f"Found {len(job_cards)} job cards on page")
        return job_cards
    except Exception as e:
        logger.error(f"Error extracting job cards: {str(e)}")
        return []


def parse_job_card(card: BeautifulSoup, country: str) -> Dict:
    """Parse individual job card to extract job information"""
    try:
        a_tag = card.find("a", class_="base-card__full-link")
        job_url = a_tag["href"].strip() if a_tag else ""
        
        sr_only = a_tag.find("span", class_="sr-only") if a_tag else None
        job_title = sr_only.text.strip() if sr_only else ""
        
        company_tag = card.find("h4", class_="base-search-card__subtitle")
        company_a = company_tag.find("a") if company_tag else None
        company_name = company_a.text.strip() if company_a else ""
        company_url = company_a["href"].strip() if company_a else ""
        
        location_tag = card.find("span", class_="job-search-card__location")
        location = location_tag.text.strip() if location_tag else ""
        
        benefit_tag = card.find("span", class_="job-posting-benefits__text")
        benefit = benefit_tag.text.strip() if benefit_tag else ""
        
        posted_tag = card.find("time", class_="job-search-card__listdate")
        posted = posted_tag.text.strip() if posted_tag else ""
        
        return {
            "country": country,
            "job_title": job_title,
            "company_name": company_name,
            "company_url": company_url,
            "location": location,
            "benefit": benefit,
            "posted": posted,
            "job_url": job_url
        }
        
    except Exception as e:
        logger.error(f"Error parsing job card: {str(e)}")
        return None


def save_job_to_json(job_data: Dict, domain: str, config: ScraperConfig) -> bool:
    """Save job data to JSON file in organized directory structure"""
    try:
        domain_dir = os.path.join(config.OUTPUT_DIR, sanitize_filename(domain))
        os.makedirs(domain_dir, exist_ok=True)
        
        job_title = sanitize_filename(job_data.get("job_title", "unknown"))
        company = sanitize_filename(job_data.get("company_name", "unknown"))
        
        # Add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{job_title}-{company}-{timestamp}.json"
        filepath = os.path.join(domain_dir, filename)
        
        job_data["scraped_at"] = datetime.now().isoformat()
        job_data["domain"] = domain
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(job_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving job to JSON: {str(e)}")
        return False


def scrape_jobs_for_title(
    job_keyword: str,
    domain: str,
    config: ScraperConfig,
    driver
) -> int:
    """Scrape jobs for a specific job title"""
    jobs_saved = 0
    
    try:
        for country in config.COUNTRIES:
            logger.info(f"\n{'='*60}")
            logger.info(f"🔍 Scraping: '{job_keyword}' in {country}")
            logger.info(f"📂 Domain: {domain}")
            logger.info(f"{'='*60}")
            
            url = build_linkedin_url(
                job_keyword,
                country,
                config.EXPERIENCE_LEVELS,
                config.WORKPLACE_TYPES,
                config.DATE_POSTED
            )
            logger.info(f"🔗 URL: {url}")
            
            try:
                driver.get(url)
                time.sleep(3)
            except WebDriverException as e:
                logger.error(f"Failed to load search page: {str(e)}")
                continue
            
            if not scroll_page(driver, config):
                logger.warning("Scrolling failed, continuing with loaded results...")
            
            html = driver.page_source
            job_cards = extract_job_cards(html)
            
            if not job_cards:
                logger.warning(f"No jobs found for '{job_keyword}' in {country}")
                continue
            
            # Apply limit if set
            if config.MAX_JOBS_PER_TITLE:
                job_cards = job_cards[:config.MAX_JOBS_PER_TITLE]
                logger.info(f"⚠️ Limiting to {config.MAX_JOBS_PER_TITLE} jobs")
            
            for idx, card in enumerate(job_cards, 1):
                logger.info(f"\n📋 Processing job {idx}/{len(job_cards)}")
                
                job_data = parse_job_card(card, country)
                if not job_data:
                    continue
                
                logger.info(f"  Title: {job_data['job_title']}")
                logger.info(f"  Company: {job_data['company_name']}")
                
                job_desc, company_desc = fetch_job_details(
                    driver,
                    job_data["job_url"],
                    config
                )
                
                job_data["job_description"] = job_desc
                job_data["company_description"] = company_desc
                
                if save_job_to_json(job_data, domain, config):
                    jobs_saved += 1
        
        return jobs_saved
        
    except Exception as e:
        logger.error(f"Error scraping jobs for '{job_keyword}': {str(e)}")
        return jobs_saved


def main():
    """Main entry point - scrape all jobs from dataset"""
    config = ScraperConfig()
    
    logger.info("🚀 Starting LinkedIn Job Scraper")
    logger.info(f"📂 Output directory: {config.OUTPUT_DIR}")
    logger.info(f"📄 Dataset: {config.DATASET_PATH}")
    
    # Create output directory
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Load dataset
    fetcher = DatasetFetcher(config.DATASET_PATH)
    if not fetcher.load_dataset():
        logger.error("❌ Failed to load dataset. Exiting.")
        return
    
    # Get all jobs to scrape
    jobs_to_scrape = fetcher.get_all_jobs_with_domains()
    
    if not jobs_to_scrape:
        logger.error("❌ No jobs found in dataset. Exiting.")
        return
    
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 SCRAPING PLAN")
    logger.info(f"{'='*60}")
    logger.info(f"Total job titles to scrape: {len(jobs_to_scrape)}")
    logger.info(f"Countries: {', '.join(config.COUNTRIES)}")
    logger.info(f"{'='*60}\n")
    
    # Initialize driver (reuse for all scraping)
    driver = setup_driver()
    
    try:
        total_jobs_saved = 0
        
        for idx, job_info in enumerate(jobs_to_scrape, 1):
            logger.info(f"\n{'#'*60}")
            logger.info(f"📌 JOB {idx}/{len(jobs_to_scrape)}")
            logger.info(f"{'#'*60}")
            
            job_title = job_info["job_title"]
            domain = job_info["domain"]
            
            jobs_saved = scrape_jobs_for_title(
                job_title,
                domain,
                config,
                driver
            )
            
            total_jobs_saved += jobs_saved
            logger.info(f"✅ Saved {jobs_saved} jobs for '{job_title}'")
            
            # Small delay between different job searches
            time.sleep(2)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎉 SCRAPING COMPLETED!")
        logger.info(f"{'='*60}")
        logger.info(f"Total jobs saved: {total_jobs_saved}")
        logger.info(f"Output location: {config.OUTPUT_DIR}")
        logger.info(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Scraping interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
    finally:
        driver.quit()
        logger.info("✅ Browser closed")


if __name__ == "__main__":
    main()
