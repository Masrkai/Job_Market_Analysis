# src/linkedin_scraper.py
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LinkedInScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(options=chrome_options)

    def search_job(self, job_title):
        query = job_title.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}"

        self.driver.get(url)
        time.sleep(3)

        try:
            job_cards = self.driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
            results = []

            for card in job_cards[:5]:  # limit results
                try:
                    title_el = card.find_element(By.CSS_SELECTOR, "h3")
                    company_el = card.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle")
                    location_el = card.find_element(By.CSS_SELECTOR, ".job-search-card__location")

                    description = "Not fetched on preview results"

                    results.append({
                        "job_title": title_el.text.strip(),
                        "company": company_el.text.strip(),
                        "location": location_el.text.strip(),
                        "description": description,
                        "posted_date": "",
                        "skills": [],
                        "url": card.find_element(By.TAG_NAME, "a").get_attribute("href")
                    })

                except:
                    continue

            return results

        except Exception as e:
            print(f"Error scraping {job_title}: {e}")
            return []

    def close(self):
        self.driver.quit()
