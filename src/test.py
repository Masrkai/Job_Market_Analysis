import os

from helpers.resolve_path import resolve_file_path
# from helpers.LinkedinAPI import scrape_linkedin_jobs
from helpers.LinkedinAPI2 import scrape_linkedin_jobs
from helpers.makefolder import ensure_dir, ensure_file, save_to_csv, append_to_csv
# from helpers.normalize import normalize_linkedin_url
from helpers.checkpointing import load_checkpoint, save_checkpoint

from helpers.data_fetcher_from_Json_DS import (
    length_of,
    print_List,
    make_category_list,
    make_jobs_dictionary,
    make_own_category_jobs_list,
)


json_file = resolve_file_path("../Data/Alternative_Names.json")

jobs_dict = make_jobs_dictionary(json_file)
categories_list = make_category_list(jobs_dict)

categories_number = length_of(categories_list)

BASE_DIR = "../../Data"
SCRAPED_DIR = os.path.join(BASE_DIR, "Scraped")

COUNTRIES = [
    # "United States","Germany","Canada", # 1st class
    # "Poland","Finland","Brazil",        # 2nd class
    "Egypt",
    # "Madagascar","Morocco"      # 3rd class
]


def main():
    ensure_dir(SCRAPED_DIR)

    # for country in COUNTRIES:
    #     country_dir = os.path.join(SCRAPED_DIR, country)
    #     ensure_dir(country_dir)
    #     print(f"working on: {country}")

    #     for category_name in categories_list:
    #         category_dir = os.path.join(country_dir, category_name)
    #         ensure_dir(category_dir)
    #         print(f"Scraping {category_name}:")


    #         all_category_results = []
    #         jobs_in_this_category = jobs_dict[category_name]
    #         ensure_file(f"{category_dir}/{category_name.csv}")


    #         for job in jobs_in_this_category:
    #             print(f"  - Searching keyword: {job}")
    #             results = scrape_linkedin_jobs(job, country)

    #             for item in results:
    #                 item['search_keyword'] = job

    #             all_category_results.extend(results)



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

                    # KEY CHANGE: Save immediately after this specific job keyword finishes
                    append_to_csv(results, csv_path)
                    print(f"    Saved {len(results)} results for {job}")
                else:
                    print(f"    No results found for {job}")




    # for country in COUNTRIES:
    #     print(f"Working on: {country}")

    #     for category_name in categories_list:
    #         print(f"Scraping Category: {category_name}")

    #         # 1. Gather all results for this category
    #         all_category_results = []
    #         jobs_in_this_category = jobs_dict[category_name]

    #         for job_keyword in jobs_in_this_category:
    #             print(f"  - Searching keyword: {job_keyword}")
    #             results = scrape_linkedin_jobs(job_keyword, country)

    #             for item in results:
    #                 item['search_keyword'] = job_keyword

    #             all_category_results.extend(results)

    #         # 2. Define the final path directly
    #         csv_filename = f"{category_name.replace(' ', '_').lower()}_jobs.csv"
    #         # We target the deep path directly: SCRAPED_DIR/Country/Category/file.csv
    #         csv_path = os.path.join(SCRAPED_DIR, country, category_name, csv_filename)

    #         # 3. Save directly
    #         if all_category_results:
    #             # save_to_csv now handles the directory creation internally
    #             save_to_csv(all_category_results, csv_path)
    #             print(f"  >>> Saved {len(all_category_results)} jobs to {csv_path}")
    #         else:
    #             # Optional: ensure an empty file exists even if no results found
    #             # ensure_file(csv_path)
    #             print(f"  >>> No jobs found for {category_name} in {country}")






    # for country in COUNTRIES:
    #     country_dir = os.path.join(SCRAPED_DIR, country)
    #     ensure_dir(country_dir)
    #     print(f"Working on: {country}")

    #     for category_name in categories_list:
    #         category_dir = os.path.join(country_dir, category_name)
    #         ensure_dir(category_dir)
    #         print(f"Scraping Category: {category_name}")

    #         # 1. Initialize an empty list for this specific category and country
    #         all_category_results = []

    #         jobs_in_this_category = jobs_dict[category_name]
    #         for job_keyword in jobs_in_this_category:
    #             print(f"  - Searching keyword: {job_keyword}")

    #             # 2. Call the scraper
    #             results = scrape_linkedin_jobs(job_keyword, country)

    #             # 3. Add metadata (optional but recommended) and append to main list
    #             for item in results:
    #                 item['search_keyword'] = job_keyword # Tracks which keyword found the job

    #             all_category_results.extend(results)

    #         # 4. Define the CSV path inside the category folder
    #         csv_filename = f"{category_name.replace(' ', '_').lower()}_jobs.csv"
    #         csv_path = os.path.join(category_dir, csv_filename)

    #         # 5. Save all results gathered for this category
    #         if all_category_results:
    #             save_to_csv(all_category_results, csv_path)
    #             print(f"  >>> Saved {len(all_category_results)} jobs to {csv_path}")
    #         else:
    #             print(f"  >>> No jobs found for {category_name} in {country}")





    # job_names = load_jobs()
    # checkpoint = load_checkpoint()

    # for ci, country in enumerate(
    #     COUNTRIES[checkpoint["country_index"]:],
    #     start=checkpoint["country_index"]
    # ):
    #     country_dir = os.path.join(SCRAPED_DIR, country.replace(" ", "_"))
    #     ensure_dir(country_dir)

    #     for ji, job in enumerate(
    #         job_names[checkpoint["job_index"]:],
    #         start=checkpoint["job_index"]
    #     ):
    #         print(f"[SCRAPING] {country} | {job}")

    #         job_dir = os.path.join(country_dir, job.replace(" ", "_"))
    #         ensure_dir(job_dir)

    #         results = scrape_linkedin_jobs(
    #             keyword=job,
    #             location=country,
    #             max_jobs=MAX_JOBS_PER_QUERY
    #         )

    #         if results:
    #             pd.DataFrame(results).to_csv(
    #                 os.path.join(job_dir, "jobs.csv"),
    #                 index=False
    #             )

    #         save_checkpoint(ci, ji + 1)

    #     save_checkpoint(ci + 1, 0)


if __name__ == "__main__":
    main()
