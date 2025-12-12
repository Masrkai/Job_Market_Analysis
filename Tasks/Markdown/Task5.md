Here’s a structured task to transform the `main.py` scraper, integrate the data fetcher, and organize the output in the specified folder structure:

---

### **Task: Refactor Scraper and Organize Output in JSON Format**

#### **Objective**
1. **Switch to the `webdriver-flexibility` branch** and use the working `linkedin.py` scraper from the `Prototype` folder.
2. **Refactor `main.py`** to use the `linkedin.py` scraper logic.
3. **Integrate `src/data_fetcher_from_Json_DS.py`** to  scrape all job titles from the dataset.
4. **Output the scraped data** in JSON format, organized in a folder structure:
   - `Data/Collected/{Domain Name}/{job_title}-{company}.json`

---

### **Step 1: Set Up the Environment**
1. **Switch to the `webdriver-flexibility` branch**:
   ```bash
   git checkout webdriver-flexibility
   ```
2. **Verify the `linkedin.py` scraper** in the `Prototype` folder works without requiring login.

---

### **Step 2: Refactor `main.py`**
1. **Copy the core scraping logic** from `Prototype/linkedin.py` into `main.py`.
2. **Ensure `main.py`**:
   - Uses the same webdriver setup and scraping logic.
   - Handles errors gracefully (e.g., timeouts, missing elements).
   - Avoids logging in to LinkedIn.

---

### **Step 3: Integrate `data_fetcher_from_Json_DS.py`**
1. **Use `data_fetcher_from_Json_DS.py`** to:
   - Load the dataset (e.g., `dataset.json`).
   - Extract all job titles and their corresponding domains (e.g., "Software Engineering," "Data Science & AI").
2. **Pass the job titles** to the scraper in `main.py` for processing.

---

### **Step 4: Organize Output in JSON Format**
1. **Create the `Data/Collected` directory** if it doesn’t exist:
   ```python
   import os
   os.makedirs("Data/Collected", exist_ok=True)
   ```
2. **For each domain** (e.g., "Software Engineering," "Data Science & AI"):
   - Create a subdirectory inside `Data/Collected`:
     ```python
     domain_dir = os.path.join("Data/Collected", domain_name)
     os.makedirs(domain_dir, exist_ok=True)
     ```
3. **For each job title**, scrape LinkedIn and save the results as:
   - `{domain_dir}/{job_title}-{company}.json`
   - Example: `Data/Collected/Software Engineering/Software Engineer-Google.json`

4. **JSON Output Format**:
   ```json
   {
     "job_title": "Software Engineer",
     "company": "Google",
     "description": "Design and develop software systems...",
     "location": "Mountain View, CA",
     "posted_date": "2025-10-01",
     "skills": ["Python", "Java", "Cloud Computing"],
     "url": "https://linkedin.com/job/..."
   }
   ```

---

### Example Workflow**
1. **Input Dataset** (`dataset.json`):
   ```json
   [
     {
       "name": "Software Engineering",
       "jobs": [
         {"name": "Software Engineer"},
         {"name": "Backend Developer"}
       ]
     },
     {
       "name": "Data Science & AI",
       "jobs": [
         {"name": "ML Engineer"},
         {"name": "Data Scientist"}
       ]
     }
   ]
   ```
2. **Output Structure**:
   ```
   Data/
   └── Collected/
       ├── Software Engineering/
       │   ├── Software Engineer-Google.json
       │   ├── Software Engineer-Microsoft.json
       │   └── Backend Developer-Amazon.json
       └── Data Science & AI/
           ├── ML Engineer-NVIDIA.json
           └── Data Scientist-IBM.json
   ```

---
