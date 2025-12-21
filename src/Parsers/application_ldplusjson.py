import os
import json
import sys
from bs4 import BeautifulSoup

def extract_ld_json_content(html_file_path):
    # 1. Open and parse the file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    scripts = soup.find_all('script', {'type': 'application/ld+json'})
    
    if not scripts:
        print("No LD+JSON found.")
        return

    # 2. Construct the output file path
    # Get the directory and the base filename (without extension)
    base_path = os.path.splitext(html_file_path)[0]
    output_path = f"{base_path}_extracted.json"

    # 3. Extract and save content
    extracted_data = []
    for script in scripts:
        if script.string:
            try:
                json_content = json.loads(script.string)
                extracted_data.append(json_content)
            except json.JSONDecodeError:
                continue

    # 4. Write to the new file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(extracted_data, outfile, indent=2, ensure_ascii=False)
    
    print(f"Success! Data saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)
    
    extract_ld_json_content(sys.argv[1])