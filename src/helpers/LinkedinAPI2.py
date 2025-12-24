import time
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from helpers.UserAgent import generate_advanced_ua
from helpers.normalize import normalize_linkedin_url

def fetch_job_page(base_url, keywords, location, start_index, headers_lock):
    """Fetch a single page of job listings"""
    user_agent = generate_advanced_ua()
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    params = {"keywords": keywords, "location": location, "start": start_index}
    
    try:
        response = requests.get(
            base_url, params=params, headers=headers, timeout=10
        )
        
        if response.status_code != 200 or not response.text.strip():
            return None, start_index
        
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("li")
        
        if not cards:
            return None, start_index
        
        page_jobs = []
        for card in cards:
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
                    normalized_link = normalize_linkedin_url(raw_link)
                    page_jobs.append(
                        {
                            "title": title,
                            "company": company,
                            "location": location_tag,
                            "link": normalized_link,
                        }
                    )
            except (AttributeError, TypeError):
                continue
        
        return page_jobs, start_index
        
    except Exception as e:
        print(f"Error occurred at start={start_index}: {e}")
        return None, start_index


def scrape_linkedin_jobs(keywords, location, max_jobs=0, max_workers=5, batch_size=10):
    """
    Scrape LinkedIn jobs with multi-threading
    
    Args:
        keywords: Job search keywords
        location: Job location
        max_jobs: Maximum number of jobs to fetch (0 = no limit, fetch all available)
        max_workers: Number of concurrent threads
        batch_size: Number of pages to fetch per batch
    """
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    job_list = []
    jobs_lock = Lock()
    headers_lock = Lock()
    
    jobs_per_page = 10
    current_start = 0
    consecutive_empty_batches = 0
    max_empty_batches = 2  # Stop if we get 2 consecutive batches with no results
    
    print(f"Starting scrape with {max_workers} workers, batch size: {batch_size} pages...")
    
    while True:
        # Check if we've reached the max_jobs limit
        if max_jobs > 0 and len(job_list) >= max_jobs:
            print(f"Reached max_jobs limit of {max_jobs}")
            break
        
        # Generate start indices for this batch
        start_indices = [current_start + (i * jobs_per_page) for i in range(batch_size)]
        
        print(f"\nFetching batch starting at index {current_start}...")
        
        batch_jobs = []
        empty_pages = 0
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks for this batch
            future_to_index = {
                executor.submit(
                    fetch_job_page, 
                    base_url, 
                    keywords, 
                    location, 
                    start_idx, 
                    headers_lock
                ): start_idx 
                for start_idx in start_indices
            }
            
            # Process completed tasks
            for future in as_completed(future_to_index):
                start_idx = future_to_index[future]
                try:
                    page_jobs, idx = future.result()
                    
                    if page_jobs:
                        batch_jobs.extend(page_jobs)
                        print(f"  Page {idx//jobs_per_page + 1}: Found {len(page_jobs)} jobs")
                    else:
                        empty_pages += 1
                        print(f"  Page {idx//jobs_per_page + 1}: No jobs found")
                        
                except Exception as e:
                    print(f"  Error processing page starting at {start_idx}: {e}")
                    empty_pages += 1
                
                # Small delay between processing results
                time.sleep(random.uniform(0.1, 0.3))
        
        # Add batch results to main list
        if batch_jobs:
            with jobs_lock:
                # Check if we need to limit the jobs added
                if max_jobs > 0:
                    remaining_slots = max_jobs - len(job_list)
                    jobs_to_add = batch_jobs[:remaining_slots]
                else:
                    jobs_to_add = batch_jobs
                
                job_list.extend(jobs_to_add)
                print(f"\nBatch complete: Added {len(jobs_to_add)} jobs. Total: {len(job_list)}")
            
            consecutive_empty_batches = 0
        else:
            consecutive_empty_batches += 1
            print(f"\nBatch complete: No jobs found (empty batch {consecutive_empty_batches}/{max_empty_batches})")
        
        # Check stopping conditions
        if consecutive_empty_batches >= max_empty_batches:
            print(f"\nStopping: {consecutive_empty_batches} consecutive empty batches")
            break
        
        if max_jobs > 0 and len(job_list) >= max_jobs:
            print(f"\nStopping: Reached max_jobs limit of {max_jobs}")
            break
        
        # Move to next batch
        current_start += batch_size * jobs_per_page
        
        # Delay between batches to be respectful
        time.sleep(random.uniform(1, 2))
    
    return job_list[:max_jobs] if max_jobs > 0 else job_list


def scrape_linkedin_jobs_sequential(keywords, location, max_jobs=0):
    """Original sequential version for comparison"""
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
                    return job_list
                
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
            start_index += 10
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Error occurred at start={start_index}: {e}")
            break
    
    return job_list


if __name__ == "__main__":
    KEYWORDS = "Software Engineer"
    LOCATION = "Egypt"
    MAX_JOBS = 53  # Set to 0 to fetch all available jobs
    
    # Benchmark multi-threaded version
    print("=" * 60)
    print("MULTI-THREADED VERSION")
    print("=" * 60)
    start_time = time.time()
    results = scrape_linkedin_jobs(
        KEYWORDS, 
        LOCATION, 
        max_jobs=MAX_JOBS,
        max_workers=5,  # Adjust based on your needs (3-10 is reasonable)
        batch_size=10   # Fetch 10 pages per batch concurrently
    )
    multi_threaded_time = time.time() - start_time
    
    print(f"\n{'=' * 60}")
    print(f"Successfully scraped {len(results)} jobs in {multi_threaded_time:.2f} seconds")
    print(f"{'=' * 60}\n")
    
    for i, job in enumerate(results[:5], 1):  # Show first 5
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Loc: {job['location']}")
        print(f"   URL: {job['link']}\n")
    
    if len(results) > 5:
        print(f"... and {len(results) - 5} more jobs")
    
    # Optional: Compare with sequential version
    # print("\n" + "=" * 60)
    # print("SEQUENTIAL VERSION (for comparison)")
    # print("=" * 60)
    # start_time = time.time()
    # results_seq = scrape_linkedin_jobs_sequential(KEYWORDS, LOCATION, max_jobs=MAX_JOBS)
    # sequential_time = time.time() - start_time
    # print(f"\nSequential version took {sequential_time:.2f} seconds")
    # print(f"Speed improvement: {sequential_time / multi_threaded_time:.2f}x faster")