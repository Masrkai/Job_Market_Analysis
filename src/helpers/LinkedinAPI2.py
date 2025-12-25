import asyncio
import random
import aiohttp
from bs4 import BeautifulSoup
from helpers.UserAgent import generate_advanced_ua
from helpers.normalize import normalize_linkedin_url


async def fetch_job_batch(session, base_url, keywords, location, start_index, semaphore):
    """Fetch a single batch of jobs with rate limiting via semaphore."""
    async with semaphore:  # Limit concurrent requests
        user_agent = generate_advanced_ua()  # Fresh UA per request
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-US,en;q=0.9",
        }
        params = {"keywords": keywords, "location": location, "start": start_index}

        try:
            async with session.get(
                base_url, params=params, headers=headers, timeout=10
            ) as response:
                if response.status != 200:
                    return None, start_index

                text = await response.text()
                if not text.strip():
                    return None, start_index

                # Add random delay between requests
                await asyncio.sleep(random.uniform(1, 3))
                return text, start_index

        except Exception as e:
            print(f"Error fetching batch at index {start_index}: {e}")
            return None, start_index


def parse_job_batch(html_text, start_index):
    """Parse HTML and extract job listings."""
    jobs = []
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        cards = soup.find_all("li")

        for card in cards:
            try:
                title = card.find("h3", class_="base-search-card__title").text.strip()
                company = card.find("h4", class_="base-search-card__subtitle").text.strip()
                location_tag = card.find("span", class_="job-search-card__location").text.strip()
                link_tag = card.find("a", class_="base-card__full-link")
                raw_link = link_tag["href"] if link_tag else None

                if raw_link:
                    normalized_link = normalize_linkedin_url(raw_link)
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location_tag,
                        "link": normalized_link,
                    })
            except (AttributeError, TypeError):
                continue

    except Exception as e:
        print(f"Error parsing batch at index {start_index}: {e}")

    return jobs


async def scrape_linkedin_jobs_concurrent(keywords, location, max_jobs=0,
                                          max_concurrent=3, batch_size=5):
    """
    Scrape LinkedIn jobs with controlled concurrency.

    Args:
        keywords: Job search keywords
        location: Job location
        max_jobs: Maximum number of jobs to fetch (0 = unlimited)
        max_concurrent: Maximum concurrent requests (default: 3)
        batch_size: Number of pages to fetch per batch (default: 5)
    """
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    all_jobs = []
    start_index = 0

    # Semaphore controls concurrent request limit
    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        while True:
            # Create batch of requests
            if max_jobs > 0 and len(all_jobs) >= max_jobs:
                break

            # Determine how many pages to fetch in this batch
            indices = [start_index + (i * 10) for i in range(batch_size)]

            print(f"Fetching batch: indices {indices[0]} to {indices[-1]}")

            # Fetch multiple pages concurrently
            tasks = [
                fetch_job_batch(session, base_url, keywords, location, idx, semaphore)
                for idx in indices
            ]
            results = await asyncio.gather(*tasks)

            # Parse all results
            batch_jobs = []
            empty_results = 0

            for html_text, idx in results:
                if html_text is None:
                    empty_results += 1
                    continue

                jobs = parse_job_batch(html_text, idx)
                if not jobs:
                    empty_results += 1
                else:
                    batch_jobs.extend(jobs)

            # Stop if we got mostly empty results
            if empty_results >= len(results) * 0.7:  # 70% empty
                print("Most results empty, stopping pagination")
                break

            if not batch_jobs:
                break

            all_jobs.extend(batch_jobs)
            print(f"Batch complete: {len(batch_jobs)} jobs. Total: {len(all_jobs)}")

            # Check if we've hit the max
            if max_jobs > 0 and len(all_jobs) >= max_jobs:
                all_jobs = all_jobs[:max_jobs]
                break

            # Move to next batch
            start_index += batch_size * 10

            # Delay between batches
            await asyncio.sleep(random.uniform(2, 4))

    return all_jobs


# Wrapper function to maintain compatibility with sync code
def scrape_linkedin_jobs(keywords, location, max_jobs=0, max_concurrent=3):
    """Synchronous wrapper for the async scraper."""
    return asyncio.run(
        scrape_linkedin_jobs_concurrent(keywords, location, max_jobs, max_concurrent)
    )


# # Example usage
# if __name__ == "__main__":
#     jobs = scrape_linkedin_jobs(
#         keywords="python developer",
#         location="San Francisco",
#         max_jobs=100,
#         max_concurrent=3  # Adjust based on your needs
#     )
#     print(f"\nTotal jobs scraped: {len(jobs)}")