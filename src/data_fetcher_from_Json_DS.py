import json

def extract_jobs_by_domain(json_data):
    """
    Extracts job titles grouped by their corresponding domains from the provided JSON data.

    Args:
        json_data (dict): The JSON data containing domains and their associated jobs.

    Returns:
        dict: A dictionary where keys are domain names and values are lists of job titles.
    """
    jobs_by_domain = {}

    # Loop through all domain objects
    for domain in json_data.get("domains", []):
        domain_name = domain.get("name")
        jobs = domain.get("jobs", [])

        # Extract only job titles
        job_titles = [job.get("name") for job in jobs if job.get("name")]

        if domain_name:
            jobs_by_domain[domain_name] = job_titles

    return jobs_by_domain


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        # Load the JSON file (must be in the same folder)
        with open("CS_Job_Titles.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Extract the jobs grouped by domain
        jobs_by_domain = extract_jobs_by_domain(json_data)

        # Example output
        print("Extracted", len(jobs_by_domain), "domains.\n")

        print("Example: Jobs in 'Software Engineering':")
        print(jobs_by_domain.get("Software Engineering", []))

    except FileNotFoundError:
        print("ERROR: Could not find 'CS_Job_Titles.json'.")
        print("Make sure it is in the same folder as this Python file.")
