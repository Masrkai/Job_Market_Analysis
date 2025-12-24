import time
import random
import requests
from bs4 import BeautifulSoup

from UserAgent import generate_advanced_ua
from normalize import normalize_linkedin_url  # Import your new helper


def scrape_linkedin_jobs(keywords, location, max_jobs=0):
    # Removed trailing space from the base URL string
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    job_list = []
    start_index = 0

    while True:
        user_agent = generate_advanced_ua()
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-US,en;q=0.9",
        }

        params = {"keywords": keywords, "location": location, "start": start_index}

        print(f"Fetching jobs starting at index {start_index}...")

        try:
            response = requests.get(
                base_url, params=params, headers=headers, timeout=10
            )

            if response.status_code != 200 or not response.text.strip():
                print("No more jobs found or access blocked.")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("li")

            if not cards:
                break

            new_jobs_count = 0
            for card in cards:
                if max_jobs > 0 and len(job_list) >= max_jobs:
                    return job_list  # Exit early if limit reached

                try:
                    title = card.find(
                        "h3", class_="base-search-card__title"
                    ).text.strip()
                    company = card.find(
                        "h4", class_="base-search-card__subtitle"
                    ).text.strip()
                    location_tag = card.find(
                        "span", class_="job-search-card__location"
                    ).text.strip()
                    link_tag = card.find("a", class_="base-card__full-link")

                    raw_link = link_tag["href"] if link_tag else None

                    if raw_link:
                        # --- Apply the normalization here ---
                        normalized_link = normalize_linkedin_url(raw_link)

                        job_list.append(
                            {
                                "title": title,
                                "company": company,
                                "location": location_tag,
                                "link": normalized_link,
                            }
                        )
                        new_jobs_count += 1
                except (AttributeError, TypeError):
                    continue

            if new_jobs_count == 0:
                break

            print(f"Scraped {new_jobs_count} jobs this batch. Total: {len(job_list)}")

            # LinkedIn Guest API usually paginates by 10 or 25.
            # If you get fewer than 10 results, it's often the end.
            start_index += 10
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            print(f"Error occurred at start={start_index}: {e}")
            break

    return job_list



if __name__ == "__main__":
    # Example usage
    KEYWORDS = "Software Engineering"
    LOCATION = "Egypt"

    results = scrape_linkedin_jobs(KEYWORDS, LOCATION, max_jobs=3)

    print(f"\nSuccessfully scraped {len(results)} jobs:\n")
    for i, job in enumerate(results, 1):
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Loc: {job['location']}")
        print(f"   URL: {job['link']}\n")