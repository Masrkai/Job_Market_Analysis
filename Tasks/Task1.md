### **Task: Create a Function to Extract Job Titles by Domain**

#### **Objective**
Write a function that takes the provided JSON file as input and returns a dictionary where:

- **Keys** are the domain names (e.g., `"Software Engineering"`, `"Data Science & AI"`).
- **Values** are lists of job titles for each domain.


#### **Function Signature**
```python
def extract_jobs_by_domain(json_data):
    """
    Extracts job titles grouped by their corresponding domains from the provided JSON data.

    Args:
        json_data (dict): The JSON data containing domains and their associated jobs.

    Returns:
        dict: A dictionary where keys are domain names and values are lists of job titles.
    """
    pass
```

#### **Expected Output**
The function should return a dictionary structured as follows:

```python
{
    "Software Engineering": ["Software Engineer", "Software Developer", "Application Developer", ...],
    "Data Science & AI": ["Data Scientist", "Senior Data Scientist", "Lead Data Scientist", ...],
    "Cybersecurity": ["Security Analyst", "Penetration Tester", "Security Engineer", ...],
    # ... and so on for all domains
}
```


#### **Example Usage**
```python
jobs_by_domain = extract_jobs_by_domain(json_data)
print(jobs_by_domain["Quantitative Finance & Engineering"])
# Output: ['Quant Engineer', 'Quantitative Researcher', 'Quant Developer', ...]
```


#### **Implementation Notes**
- The function should iterate over the `domains` array in the JSON data.
- For each domain, extract the `name` and the list of job `name`s.
- Return the dictionary for further use (e.g., searching or filtering job titles).