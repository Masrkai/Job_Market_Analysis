# LinkedIn Job Market Scraper

A lightweight, ethical scraper to collect unbiased job market data from LinkedIn for Computer Science roles—using a dedicated dummy account to avoid personalized feed bias.

## 📌 Purpose

This project systematically scrapes LinkedIn job listings for predefined CS/AI/ML job titles (from `Data/CS_Job_Titles.json`) to analyze current market offerings—especially in regions like Egypt and EMEA—without interference from personal profile algorithms.

To ensure neutrality and protect main accounts, scraping is performed via a **dedicated fake LinkedIn account** with no profile history, courses, or affiliations.

## 🛠️ Features

- Scrapes job title, company, location, URL, posting date, Easy Apply status, and timestamp
- Supports multiple search keywords (e.g., "Machine Learning Engineer", "Data Scientist")
- Outputs clean, structured `.csv` files (no database dependency)
- Uses Brave/Chrome with anti-detection measures
- Includes error handling and screenshots on failure

## 📂 File Structure

```
Project/
├── Data/
│   ├── CS_Job_Titles.json    # Job titles to scrape
│   └── linkedin_jobs.csv     # Output (generated)
├── src/
│   └── main.py               # Scraper implementation
├── requirements.txt
├── shell.nix                 # (NixOS dev shell)
└── README.md
```

## ⚙️ Setup

1. **Environment Variables**
   Set in your shell or `.env`:
   ```bash
   export LINKEDIN_EMAIL="dummy@example.com"
   export LINKEDIN_PASSWORD="secure_password"
   export BRAVE_PATH="/path/to/brave"  # Optional; defaults to Chrome if omitted
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # Also requires Selenium + Chrome/Brave WebDriver
   ```

3. **Run**
   ```bash
   python src/main.py
   ```
   Output: `linkedin_jobs.csv` in the project root.

## ⚠️ Notes

- **Ethical Use**: Only scrape publicly available data; respect `robots.txt` and rate limits.
- **LinkedIn Policy**: Automation violates LinkedIn’s ToS—use at your own risk and only for personal research.
- **Output**: Descriptions are often empty due to dynamic loading; focus is on metadata (title, co, loc, etc.).
- **Scalability**: Designed for small-scale, periodic market scans—not high-volume scraping.

