import time
import random
import requests
from bs4 import BeautifulSoup
from helpers.UserAgent import generate_advanced_ua

def scrape_linkedin_jobs(keywords, location, max_jobs=50):
    """
    Scrapes LinkedIn job listings using the guest API endpoint.
    Uses a different user agent for each request to avoid detection.
    """

    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    job_list = []
    start_index = 0

    while len(job_list) < max_jobs:
        # Generate a fresh user agent for each request
        user_agent = generate_advanced_ua()

        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-US,en;q=0.9",
        }

        params = {
            "keywords": keywords,
            "location": location,
            "start": start_index
        }

        print(f"Fetching jobs starting at index {start_index}...")
        print(f"Using User Agent: {user_agent}...")  # Print first 80 chars

        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)

            # If the response is empty or 400+, we've hit the end or a block
            if response.status_code != 200 or not response.text.strip():
                print("No more jobs found or access blocked.")
                break

            soup = BeautifulSoup(response.text, 'html.parser')

            # Each job is contained in a <li> tag
            cards = soup.find_all('li')

            if not cards:
                break

            for card in cards:
                if len(job_list) >= max_jobs:
                    break

                try:
                    # Logic to extract data based on the LinkedIn Guest HTML structure
                    title = card.find('h3', class_='base-search-card__title').text.strip()
                    company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                    location_tag = card.find('span', class_='job-search-card__location').text.strip()
                    link = card.find('a', class_='base-card__full-link')['href']

                    job_list.append({
                        "title": title,
                        "company": company,
                        "location": location_tag,
                        "link": link
                    })
                except AttributeError:
                    # Skip cards that don't match the expected structure (ads, etc)
                    continue

            # Increment by 10
            start_index += 10

            # Be polite: wait a random amount of time to avoid detection
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            print(f"Error occurred: {e}")
            break

    return job_list

if __name__ == "__main__":
    # Example usage
    KEYWORDS = "Python Developer"
    LOCATION = "Egypt"

    results = scrape_linkedin_jobs(KEYWORDS, LOCATION, max_jobs=49)

    print(f"\nSuccessfully scraped {len(results)} jobs:\n")
    for i, job in enumerate(results, 1):
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Loc: {job['location']}")
        print(f"   URL: {job['link']}\n")