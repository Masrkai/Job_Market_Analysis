def extract_job_criteria(soup):
    """
    Scrapes job criteria items into a dictionary.
    Example output: {'Seniority level': 'Entry level', 'Employment type': 'Part-time', ...}
    """
    job_details = {}

    # Find all list items within the job criteria list
    criteria_items = soup.find_all('li', class_='description__job-criteria-item')

    for item in criteria_items:
        # Extract the label (e.g., Seniority level)
        header = item.find('h3', class_='description__job-criteria-subheader')
        # Extract the value (e.g., Entry level)
        value = item.find('span', class_='description__job-criteria-text')

        if header and value:
            # Clean up whitespace and add to dictionary
            key = header.get_text(strip=True)
            val = value.get_text(strip=True)
            job_details[key] = val

    return job_details