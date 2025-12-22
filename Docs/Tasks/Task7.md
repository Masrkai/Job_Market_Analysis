### **Task: Web Scraping Logic for Job Market Analysis**

#### **Objective**
Build a Python script to scrape job listings from LinkedIn, organized by country and job domain. The goal is to collect data for comparative analysis across countries of different economic classes.

---

### **1. Data Sources & Dictionaries**
You will scrape using **two dictionaries**:
- **Countries**: A list of target countries (to be provided).
- **Jobs**: Job titles/domains from [this dataset](../../Data/Alternative_Names.json).

**Key Variables**:
```python
KEYWORDS = "Defense"  # Example job domain
LOCATION = "United States"  # Example country
```
Your script should **loop through all combinations** of countries and job domains.

---

### **2. Scraping Workflow**
#### **Folder Structure**
- Create a `Scraped` folder in the [Data](../../Data) directory.
- Inside `Scraped`, create a subfolder for **each country**.
- Within each country folder, create subfolders for **each job domain**.

#### **Data Collection**
- Save scraped data as `.csv` files.
- **URL Standardization**: Convert all LinkedIn URLs to the `www.linkedin.com` format (e.g., `eg.linkedin.com` → `www.linkedin.com`).
  - Use `regex` from the `re` library to clean URLs **before writing to `.csv`**.

#### **Checkpointing**
- Implement a `checkpoint.json` file to **pause and resume scraping** from where it stopped.
- Be prepared for potential complications (e.g., file corruption, interruptions).

---

### **3. Data Analysis & Comparative Study**
#### **Focus Areas**
- Compare job markets across:
  - **3 first-class countries** (e.g., high GDP, low unemployment).
  - **3 second-class countries** (e.g., mid-tier GDP, moderate unemployment).
  - **3 third-class countries** (e.g., low GDP, high unemployment).

#### **Economic Metrics**
Use the following sources to classify countries:
- **GDP**: [World Bank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD), [Worldometers](https://www.worldometers.info/gdp/gdp-by-country/), [IMF](https://data.imf.org/en/Data%20Explorer).
- **GDP per Capita & Unemployment**: [CIA World Factbook](https://www.cia.gov/the-world-factbook/field/real-gdp-per-capita/country-comparison/).

**Note**: GDP is not perfect, but it’s a practical starting point. Supplement with other metrics (e.g., unemployment, GDP growth) for deeper insights.

---

### **4. Additional Notes**
- **Avoid Overcomplicating**: Focus on **data collection and basic analysis**. Machine learning/deep learning is **not** required for this task.
- **Reference**: Review [Task6.md](Task6.md) for team perspectives and expectations.

---

### **Deliverables**

1. A **Python script** that:
   - Scrapes job listings for all country/job combinations.
   - Standardizes URLs and saves data in `.csv` format.
   - Implements checkpointing.

2. A **folder structure** with organized scraped data.
