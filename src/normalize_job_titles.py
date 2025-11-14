import json
# Fuzzy matching library matches similar strings 
# for example "SWE" and "Software Engineer"
from fuzzywuzzy import process

# Load taxonomy aka a format for standardized job titles
# the file 'cs_job_taxonomy.json' should be structured as:
# {
#   "standardized_roles": {
#       "Software Engineer": ["Software Engineer", "SWE", "Software Dev"],
#       "Data Scientist": ["Data Scientist", "DS", "Data Science Specialist"],
#       "Machine Learning Engineer": ["Machine Learning Engineer", "ML Engineer", "AI Engineer"]
#   }
# }
with open('jobs-title.json', 'r') as f:
    taxonomy = json.load(f)

# Build lowercase lookup
lookup = {}
for canonical, variants in taxonomy['standardized_roles'].items():
    for v in variants:
        lookup[v.lower()] = canonical

all_variants_lower = list(lookup.keys())

def normalize_title(raw_title, threshold=80):
    if not raw_title or not isinstance(raw_title, str):
        return "Other"
    clean = raw_title.strip().lower()
    if clean in lookup:
        return lookup[clean]
    # Fuzzy fallback
    match, score = process.extractOne(clean, all_variants_lower)
    return lookup[match] if score >= threshold else "Other"

# Example
print(normalize_title("ML ENGINEER"))          # Machine Learning Engineer
print(normalize_title("Senior SWE"))           # Software Engineer
print(normalize_title("Quantum Computing Dev")) # Other