import os
import json
import time
import re
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

# ==================================================
# PATH CONFIGURATION
# ==================================================

BASE_DIR = "Data"
SCRAPED_DIR = os.path.join(BASE_DIR, "Scraped")
JOBS_FILE = os.path.join(BASE_DIR, "Alternative_Names.json")
CHECKPOINT_FILE = "checkpoint.json"

# ==================================================
# INPUT CONFIG
# ==================================================

COUNTRIES = [
    "United States","Germany","Canada",
    "Poland","Finland","Brazil",
    "Egypt","Madagascar","Morocco"
]


MAX_JOBS_PER_QUERY = 50
REQUEST_DELAY_RANGE = (2, 5)

# ==================================================
# UTILITIES
# ==================================================

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def normalize_linkedin_url(url: str) -> str:
    return re.sub(
        r"https://[a-z]{2}\.linkedin\.com",
        "https://www.linkedin.com",
        url
    )


def generate_user_agent():
    return random.choice([
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    ])


# ==================================================
# LOAD JOB DOMAINS (LIST-BASED JSON)
# ==================================================

def load_jobs():
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [job["name"] for job in data if "name" in job]


# ==================================================
# CHECKPOINTING
# ==================================================

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return {"country_index": 0, "job_index": 0}

    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"country_index": 0, "job_index": 0}


def save_checkpoint(ci, ji):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(
            {"country_index": ci, "job_index": ji},
            f,
            indent=2
        )


# ==================================================
# LINKEDIN GUEST SCRAPER
# ==================================================

def scrape_linkedin_jobs(keyword, location, max_jobs):
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    jobs = []
    start = 0

    while len(jobs) < max_jobs:
        headers = {
            "User-Agent": generate_user_agent(),
            "Accept-Language": "en-US,en;q=0.9",
        }

        params = {
            "keywords": keyword,
            "location": location,
            "start": start
        }

        response = requests.get(base_url, headers=headers, params=params, timeout=10)

        if response.status_code != 200 or not response.text.strip():
            break

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("li")

        if not cards:
            break

        for card in cards:
            if len(jobs) >= max_jobs:
                break

            try:
                title = card.find("h3").get_text(strip=True)
                company = card.find("h4").get_text(strip=True)
                location_text = card.find("span").get_text(strip=True)
                link = card.find("a")["href"]

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "url": normalize_linkedin_url(link)
                })
            except Exception:
                continue

        start += 10
        time.sleep(random.uniform(*REQUEST_DELAY_RANGE))

    return jobs


# ==================================================
# MAIN
# ==================================================

def main():
    ensure_dir(SCRAPED_DIR)

    job_names = load_jobs()
    checkpoint = load_checkpoint()

    for ci, country in enumerate(
        COUNTRIES[checkpoint["country_index"]:],
        start=checkpoint["country_index"]
    ):
        country_dir = os.path.join(SCRAPED_DIR, country.replace(" ", "_"))
        ensure_dir(country_dir)

        for ji, job in enumerate(
            job_names[checkpoint["job_index"]:],
            start=checkpoint["job_index"]
        ):
            print(f"[SCRAPING] {country} | {job}")

            job_dir = os.path.join(country_dir, job.replace(" ", "_"))
            ensure_dir(job_dir)

            results = scrape_linkedin_jobs(
                keyword=job,
                location=country,
                max_jobs=MAX_JOBS_PER_QUERY
            )

            if results:
                pd.DataFrame(results).to_csv(
                    os.path.join(job_dir, "jobs.csv"),
                    index=False
                )

            save_checkpoint(ci, ji + 1)

        save_checkpoint(ci + 1, 0)


if __name__ == "__main__":
    main()
