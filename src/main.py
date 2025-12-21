import os
import csv
import time
from datetime import datetime
from urllib.parse import quote_plus

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from helpers.webdriver import setup_driver

driver = setup_driver()















































# def login(driver):
#     """Login to LinkedIn"""
#     try:
#         driver.get("https://www.linkedin.com/login")

#         email_field = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "username"))
#         )
#         email_field.send_keys(os.getenv("LINKEDIN_EMAIL"))

#         password_field = driver.find_element(By.ID, "password")
#         password_field.send_keys(os.getenv("LINKEDIN_PASSWORD"))

#         driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#         WebDriverWait(driver, 10).until(EC.url_contains("feed"))
#         print("✓ Login successful")
#         time.sleep(2)
#     except Exception as e:
#         print(f"✗ Login failed: {e}")
#         raise


# def search_jobs(driver, keyword, location="", filters=None):
#     """Search for jobs with given keyword and optional filters"""
#     encoded_keyword = quote_plus(keyword)
#     encoded_location = quote_plus(location) if location else ""

#     search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keyword}"
#     if encoded_location:
#         search_url += f"&location={encoded_location}"
#     if filters:
#         search_url += filters

#     driver.get(search_url)
#     time.sleep(3)
#     print(f"✓ Searching for: {keyword}" + (f" in {location}" if location else ""))


# def extract_job_cards(driver):
#     """Extract all job card elements on the current page"""
#     try:
#         job_cards = driver.find_elements(By.CSS_SELECTOR, "li[data-occludable-job-id]")
#         print(f"✓ Found {len(job_cards)} job cards on this page")
#         return job_cards
#     except NoSuchElementException:
#         print("✗ No job cards found")
#         return []


# def extract_job_details(driver, job_card):
#     """Extract details from a single job card"""
#     job_data = {
#         'title': '',
#         'company': '',
#         'location': '',
#         'description': '',
#         'job_url': '',
#         'posted_date': '',
#         'easy_apply': False,
#         'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }

#     try:
#         clickable = job_card.find_element(By.CSS_SELECTOR, ".job-card-container__link")
#         driver.execute_script("arguments[0].scrollIntoView(true);", clickable)
#         time.sleep(0.5)
#         clickable.click()
#         time.sleep(2.5)

#         try:
#             title_elem = WebDriverWait(driver, 5).until(
#                 EC.presence_of_element_located(
#                     (By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title")
#                 )
#             )
#             job_data['title'] = title_elem.text.strip()
#         except TimeoutException:
#             title_selectors = [
#                 ".job-card-list__title strong",
#                 ".job-card-list__title",
#                 ".artdeco-entity-lockup__title",
#             ]
#             for selector in title_selectors:
#                 try:
#                     title_elem = job_card.find_element(By.CSS_SELECTOR, selector)
#                     job_data['title'] = title_elem.text.strip()
#                     if job_data['title']:
#                         break
#                 except NoSuchElementException:
#                     continue

#         try:
#             company_elem = driver.find_element(
#                 By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name"
#             )
#             job_data['company'] = company_elem.text.strip()
#         except NoSuchElementException:
#             try:
#                 company_elem = job_card.find_element(
#                     By.CSS_SELECTOR, ".artdeco-entity-lockup__subtitle"
#                 )
#                 job_data['company'] = company_elem.text.strip()
#             except NoSuchElementException:
#                 pass

#         try:
#             location_elem = driver.find_element(
#                 By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__bullet"
#             )
#             job_data['location'] = location_elem.text.strip()
#         except NoSuchElementException:
#             try:
#                 location_elem = job_card.find_element(
#                     By.CSS_SELECTOR, ".artdeco-entity-lockup__caption span"
#                 )
#                 job_data['location'] = location_elem.text.strip()
#             except NoSuchElementException:
#                 pass

#         job_data['job_url'] = driver.current_url

#         try:
#             desc_elem = WebDriverWait(driver, 3).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-description-content__text"))
#             )
#             job_data['description'] = desc_elem.text.strip()
#         except TimeoutException:
#             pass

#         try:
#             job_card.find_element(By.XPATH, ".//*[contains(text(), 'Easy Apply')]")
#             job_data['easy_apply'] = True
#         except NoSuchElementException:
#             pass

#         try:
#             time_elem = job_card.find_element(By.CSS_SELECTOR, "time")
#             job_data['posted_date'] = time_elem.text.strip()
#         except NoSuchElementException:
#             pass

#     except Exception as e:
#         print(f"⚠ Error extracting job details: {e}")

#     return job_data


# def go_to_next_page(driver):
#     """Navigate to the next page of search results, if available"""
#     try:
#         next_button = driver.find_element(
#             By.CSS_SELECTOR, "button[aria-label='Page forward']"
#         )
#         if next_button.is_enabled():
#             driver.execute_script("arguments[0].click();", next_button)
#             time.sleep(3)
#             print("→ Navigated to next page")
#             return True
#         else:
#             print("✓ No more pages available")
#             return False
#     except NoSuchElementException:
#         print("✓ No next page button found")
#         return False


# def scrape_jobs(driver, keyword, location="", max_jobs=50):
#     """Scrape jobs for a given keyword"""
#     jobs_data = []
#     search_jobs(driver, keyword, location)
#     total_scraped = 0
#     page = 1

#     while total_scraped < max_jobs:
#         print(f"\n📄 Scraping page {page}...")
#         job_cards = extract_job_cards(driver)

#         if not job_cards:
#             print("✗ No job cards found on this page.")
#             break

#         for idx, card in enumerate(job_cards):
#             if total_scraped >= max_jobs:
#                 break

#             print(f"\nScraping job {total_scraped + 1}/{max_jobs}...")
#             job_data = extract_job_details(driver, card)

#             if job_data['title']:
#                 job_data['search_keyword'] = keyword
#                 jobs_data.append(job_data)
#                 total_scraped += 1
#                 print(f"  ✓ {job_data['title']} at {job_data['company']}")
#                 if job_data['posted_date']:
#                     print(f"    Posted: {job_data['posted_date']}")
#             else:
#                 print("  ✗ Skipped (no title found)")

#             time.sleep(1)

#         # Try to move to next page
#         if not go_to_next_page(driver):
#             break
#         page += 1

#     print(f"\n✓ Scraped {total_scraped} jobs for '{keyword}'")
#     return jobs_data


# def save_to_csv(jobs_data, filename="linkedin_jobs.csv"):
#     """Save scraped jobs to CSV file"""
#     if not jobs_data:
#         print("⚠ No data to save")
#         return

#     keys = jobs_data[0].keys()
#     with open(filename, 'w', newline='', encoding='utf-8') as f:
#         dict_writer = csv.DictWriter(f, fieldnames=keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(jobs_data)

#     print(f"✓ Saved {len(jobs_data)} jobs to {filename}")


# def scrape_multiple_keywords(driver, keywords, location="", max_jobs_per_keyword=10):
#     """Scrape jobs for multiple keywords"""
#     all_jobs_data = []
    
#     for keyword in keywords:
#         print(f"\n{'='*60}")
#         print(f"Processing keyword: {keyword}")
#         print(f"{'='*60}")
#         try:
#             jobs_data = scrape_jobs(driver, keyword, location, max_jobs_per_keyword)
#             all_jobs_data.extend(jobs_data)
#         except Exception as e:
#             print(f"✗ Error scraping '{keyword}': {e}")
#             driver.save_screenshot(f"error_{keyword.replace(' ', '_')}.png")
#         time.sleep(3)
    
#     return all_jobs_data


# def main():
#     KEYWORDS = [
#         "Machine Learning Engineer",
#         "Data Scientist",
#         "AI Engineer",
#         "Deep Learning Engineer"
#     ]
#     LOCATION = ""
#     MAX_JOBS_PER_KEYWORD = 25
#     OUTPUT_FILE = "linkedin_jobs.csv"

#     driver = None

#     try:
#         driver = setup_driver()
#         login(driver)
#         all_jobs_data = scrape_multiple_keywords(
#             driver,
#             keywords=KEYWORDS,
#             location=LOCATION,
#             max_jobs_per_keyword=MAX_JOBS_PER_KEYWORD
#         )
#         save_to_csv(all_jobs_data, OUTPUT_FILE)
#     except Exception as e:
#         print(f"✗ Fatal error: {e}")
#         if driver:
#             driver.save_screenshot("error_fatal.png")
#     finally:
#         if driver:
#             driver.quit()
#             print("✓ Browser closed")


# if __name__ == "__main__":
#     main()