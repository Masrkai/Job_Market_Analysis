import os

from helpers.resolve_path import resolve_file_path
from helpers.LinkedinAPI2 import scrape_linkedin_jobs
from helpers.makefolder import ensure_dir, ensure_file, append_to_csv

from helpers.data_fetcher_from_Json_DS import (
    length_of,
    make_category_list,
    make_jobs_dictionary,
)

json_file = resolve_file_path("../Data/CS_Job_Titles_Categorized.json")

jobs_dict = make_jobs_dictionary(json_file)
categories_list = make_category_list(jobs_dict)

categories_number = length_of(categories_list)

BASE_DIR = "../../Data"
SCRAPED_DIR = os.path.join(BASE_DIR, "Scraped")

COUNTRIES = [
    "United States","Germany","Canada", # 1st class
    "Poland","Finland","Brazil",        # 2nd class
    "Egypt","Madagascar","Morocco"      # 3rd class
]


def main():
    ensure_dir(SCRAPED_DIR)

    for country in COUNTRIES:
        country_dir = os.path.join(SCRAPED_DIR, country)
        ensure_dir(country_dir)
        print(f"working on: {country}")

        for category_name in categories_list:
            category_dir = os.path.join(country_dir, category_name)
            ensure_dir(category_dir)
            print(f"Scraping {category_name}:")

            # Define the specific CSV file path for this category
            csv_filename = f"{category_name}.csv"
            csv_path = os.path.join(category_dir, csv_filename)

            # Ensure the file exists (optional, append_to_csv handles it)
            ensure_file(csv_path)

            jobs_in_this_category = jobs_dict[category_name]

            for job in jobs_in_this_category:
                print(f"  - Searching keyword: {job}")
                results = scrape_linkedin_jobs(job, country)

                if results:
                    for item in results:
                        item['search_keyword'] = job

                    append_to_csv(results, csv_path)
                    print(f"    Saved {len(results)} results for {job}")
                else:
                    print(f"    No results found for {job}")



if __name__ == "__main__":
    main()
