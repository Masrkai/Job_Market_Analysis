import json
import resolve_path


def make_jobs_dictionary(json_file):
    with open(json_file, "r") as file:
        Jobs_dictionary = json.load(file)

    jobs_dict = {
        category["name"]: [job["name"] for job in category["jobs"]]
        for category in Jobs_dictionary
    }
    return jobs_dict


def make_category_list(jobs_dict):
    categories = list(jobs_dict.keys())
    return categories


def make_own_category_jobs_list(jobs_dict, category, categories):
    category_name = categories[category]
    jobs_list = jobs_dict[category_name]
    return jobs_list


def length_of(categories):
    number = len(categories)
    return number


def print_List(categories):
    print("Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")


if __name__ == "__main__":
    json_file = resolve_path.resolve_file_path("../../Data/Alternative_Names.json")

    jobs_dict = make_jobs_dictionary(json_file)
    categories_list = make_category_list(jobs_dict)

    # 1. Usingfunction for a numbered list
    print("\n--- Numbered Category List ---")
    print_List(categories_list)

    # # Example of printing jobs within the first category
    # category_jobs = make_own_category_jobs_list(jobs_dict, 0, categories_list)

    # Iterate through every category in your list
    for category_name in categories_list:
        print(f"\nJobs in {category_name}:")

        # Access the list of jobs for THIS specific category from your dictionary
        jobs_in_this_category = jobs_dict[category_name]

        # Nested loop to print each job in the current category
        for job in jobs_in_this_category:
            print(f"  - {job}")
