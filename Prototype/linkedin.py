from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from webdriver import setup_driver

import time
import csv


# --- CONFIG ---
COUNTRIES = ["Egypt"]
JOB_KEYWORD = "Software engineer"

DATE_POSTED = "any"
WORKPLACE_TYPES = []
EXPERIENCE_LEVELS = []

# DATE_POSTED codes:            # EXPERIENCE_LEVELS codes:          # WORKPLACE_TYPES codes:
# "any" = Any time              # [] = All levels                   # [] = All types
# "24h" = Past 24 hours         # ["1"] = Internship                # ["1"] = On-site
# "week" = Past week            # ["2"] = Entry level               # ["2"] = Remote
# "month" = Past month          # ["3"] = Associate                 # ["3"] = Hybrid
                                # ["4"] = Mid-Senior level
                                # ["5"] = Director
                                # ["6"] = Executive

# --- SCROLL ---
MAX_SCROLL_ATTEMPTS = 200
SCROLL_PAUSE = 5
DETAIL_PAUSE = 2

# --- SAFE FILENAMES ---
safe_keyword = JOB_KEYWORD.replace(" ", "_")
safe_exp = ",".join(EXPERIENCE_LEVELS).replace(",", "_") if EXPERIENCE_LEVELS else "all"
safe_workplace = ",".join(WORKPLACE_TYPES).replace(",", "_") if WORKPLACE_TYPES else "all"
safe_date = DATE_POSTED

# --- SETUP CHROME ---
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
driver = setup_driver()

# --- HELPER FUNCTIONS ---
def build_linkedin_url(keyword, location, exp_levels, workplace_types, date_posted):
    exp_param = ",".join(exp_levels) if exp_levels else ""
    workplace_param = ",".join(workplace_types) if workplace_types else ""
    date_param = ""
    if date_posted == "24h": date_param = "r86400"
    elif date_posted == "week": date_param = "r604800"
    elif date_posted == "month": date_param = "r2592000"

    url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(keyword)}&location={quote_plus(location)}"
    if exp_param: url += f"&f_E={exp_param}"
    if workplace_param: url += f"&f_WT={workplace_param}"
    if date_param: url += f"&f_TPR={date_param}"
    url += "&position=1&pageNum=0"
    return url

def scroll_page(driver):
    attempt = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while attempt < MAX_SCROLL_ATTEMPTS:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        try:
            show_more_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "infinite-scroller__show-more-button"))
            )
            show_more_btn.click()
            time.sleep(SCROLL_PAUSE)
        except:
            pass
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        attempt += 1

def fetch_job_details(job_url):
    job_desc = ""
    company_desc = ""
    if not job_url:
        return job_desc, company_desc
    try:
        driver.get(job_url)
        time.sleep(DETAIL_PAUSE)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "description__text"))
        )
        job_soup = BeautifulSoup(driver.page_source, "html.parser")
        job_div = job_soup.find("div", class_="description__text")
        job_desc = job_div.get_text(separator="\n", strip=True) if job_div else ""
        company_div = job_soup.find("div", class_="show-more-less-html__markup")
        company_desc = company_div.get_text(separator="\n", strip=True) if company_div else ""
    except Exception as e:
        print(f"⚠️ Failed to fetch job detail: {e}")
    return job_desc, company_desc

# --- MAIN SCRAPING LOOP ---
all_jobs = []

for country in COUNTRIES:
    print(f"=== Scraping LinkedIn Jobs for {country} ===")
    url = build_linkedin_url(JOB_KEYWORD, country, EXPERIENCE_LEVELS, WORKPLACE_TYPES, DATE_POSTED)
    print(f"🔗 URL: {url}")
    driver.get(url)
    scroll_page(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    job_cards = soup.find_all("div", class_="base-card")

    for idx, card in enumerate(job_cards):
        a_tag = card.find("a", class_="base-card__full-link")
        job_url = a_tag["href"].strip() if a_tag else ""
        job_title = a_tag.find("span", class_="sr-only").text.strip() if a_tag and a_tag.find("span", class_="sr-only") else ""
        company_tag = card.find("h4", class_="base-search-card__subtitle")
        company_a = company_tag.find("a") if company_tag else None
        company_name = company_a.text.strip() if company_a else ""
        company_url = company_a["href"].strip() if company_a else ""
        location = card.find("span", class_="job-search-card__location")
        location = location.text.strip() if location else ""
        benefit = card.find("span", class_="job-posting-benefits__text")
        benefit = benefit.text.strip() if benefit else ""
        posted = card.find("time", class_="job-search-card__listdate")
        posted = posted.text.strip() if posted else ""

        print(f"🔍 ({idx + 1}/{len(job_cards)}) Fetching job: {job_title}")
        job_description, company_description = fetch_job_details(job_url)

        all_jobs.append({
            "country": country,
            "job_title": job_title,
            "company_name": company_name,
            "company_url": company_url,
            "location": location,
            "benefit": benefit,
            "posted": posted,
            "company_description": company_description,
            "job_url": job_url,
            "job_description": job_description
        })

# --- SAVE TO CSV ---
if all_jobs:
    csv_file = f"linkedin_jobs_{safe_keyword}_{'_'.join([c.replace(' ','') for c in COUNTRIES])}_{safe_exp}_{safe_workplace}_{safe_date}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
        writer.writeheader()
        writer.writerows(all_jobs)
    print(f"📁 Saved {len(all_jobs)} jobs to {csv_file}")
else:
    print("⚠️ No jobs extracted.")

driver.quit()