import os

from helpers.makefolder import ensure_dir
from helpers.resolve_path import resolve_file_path
from helpers.normalize import normalize_linkedin_url
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
    "United States","Germany","Canada", # 1st class
    "Poland","Finland","Brazil",        # 2nd class
    "Egypt","Madagascar","Morocco"      # 3rd class
]


def main():
    # ensure_dir(SCRAPED_DIR)
    for country in COUNTRIES:
        country_dir = os.path.join(SCRAPED_DIR, country)
        ensure_dir(country_dir)
        print(f"working on: {country}")

        for category_name in categories_list:
            category_dir = os.path.join(country_dir, category_name)
            ensure_dir(category_dir)
            print(f"Scraping {category_name}:")


            jobs_in_this_category = jobs_dict[category_name]
            for job in jobs_in_this_category:
                # job = os.path.join(category_dir, job)
                # ensure_dir(job)
                print(f"  - {job}")









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
