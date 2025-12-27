import csv
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

from helpers.UserAgent import generate_advanced_ua
from URL.description import extract_formatted_description
from URL.salary import extract_salary_safe

from itertools import islice




def proof_of_concept():
    csv_path = Path("Data/Scraped/United States/Cloud & Network Engineering/Cloud & Network Engineering.csv")
    json_path = csv_path.with_suffix('.json')

    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        return

    # Get SECOND row from CSV (index 1)
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Skip first row, get second row
        job_data = next(islice(reader, 1, 2))

    print(f"🚀 Testing Enrichment for: {job_data['title']} at {job_data['company']}")

    # 2. Request the page
    headers = {"User-Agent": generate_advanced_ua()}
    try:
        response = requests.get(job_data['link'], headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Apply Extraction Logic
        # A. JSON-LD
        json_ld_tag = soup.find("script", {"type": "application/ld+json"})
        json_ld_data = json.loads(json_ld_tag.string) if json_ld_tag else None

        # B. Salary - extract_salary_safe already returns a string
        salary_text = extract_salary_safe(soup)

        # C. Detailed Description (Using your logic)
        description_text = extract_formatted_description(soup)

        # 4. Compile and Save
        enriched_entry = {
            **job_data, # Keep original CSV fields
            "enriched_details": {
                "json_ld": json_ld_data,
                "salary": salary_text,
                "description_clean": description_text
            }
        }

        with open(json_path, 'w', encoding='utf-8') as jf:
            json.dump([enriched_entry], jf, indent=4, ensure_ascii=False)

        print("\n--- ✅ ENRICHMENT SUCCESS ---")
        print(f"📍 Location: {json_path}")
        print(f"💰 Salary Found: {salary_text}")
        print(f"📝 Description Length: {len(description_text) if description_text else 0} chars")
        print("\n--- DESCRIPTION PREVIEW ---")
        print(description_text if description_text else "No description found.")

    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    proof_of_concept()