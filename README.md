# LinkedIn Job Market Analysis

A lightweight, ethical scraper to collect unbiased job market data from LinkedIn for Computer Science roles using a dedicated dummy account to avoid personalized feed bias.

## 📌 Purpose

This project systematically scrapes LinkedIn job listings for predefined CS/AI/ML job titles (from `Data/CS_Job_Titles.json`) to analyze current market offerings especially in regions like Egypt without interference from a biased personal profile algorithm.

To ensure neutrality and protect main accounts, scraping is performed via a **dedicated fake LinkedIn account** with no profile history, courses, or affiliations.


## 👥 This is a group project

the project/study is an idea lead by these maintainers:

- @Masrkai
- @AHMED-ESSA007
- @dev-ahmedkhaled
- @maryam-othmann5
- @SalmANasef

Tasks would be assigned and informed about completion in the [Tasks](Tasks/) Directory, as:

- code of the documents in [Markdown](Tasks/Markdown/)
- PDF readable files in [PDF](Tasks/PDF/)

We all take responsibility in making this real, any inquiries should be `OPEN TO PUBLIC` more on that later when the project is completed,
and we wish for your behaviour to be civilized, any uncivilized behaviour from harassment to burdening maintainers will result in you getting ignored or banned

### 🛠️ Features

- Scrapes `job title`, `company`, `location`, `URL` and `Easy Apply status`
- Outputs clean, structured `.csv` files (no database dependency ***this is a blessing and a curse but becuase we couldnn't decide if we needed databases for such a workflow we will go `"the manual"` route of depending on basic files***)
- Includes error handling and screenshots on failure

### 📂 File Structure (needs to be updated soon)

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

1. install a chromium based brouwer, what was used by maintainer @Masrkai from the start was [brave-browser](https://github.com/brave/brave-browser) but any other chromium engine based browser would work, theoretically even gecko/firefox ones but with some modifications to the current setup for the webdriver.

2. **Environment Variables**
   Set in your shell or `.env`:
   ```bash
   export LINKEDIN_EMAIL="dummy@example.com"
   export LINKEDIN_PASSWORD="secure_password"
   export BRAVE_PATH="/path/to/brave"  # Optional; defaults to Chrome if omitted
   ```

3. From here you take ***Two Routes***, `NixOS` and `Non NixOS`

   - NixOS:

     1. run  `nix-shell` it would install the [requirements.txt](requirements.txt) and all the things you need


   - Non NixOS

      2. **Install Dependencies**
         ```bash
         pip install -r requirements.txt
         # Also requires Selenium + Chrome/Brave WebDriver
         ```

4. **Run**
   ```bash
   python src/main.py
   ```
   Output: `linkedin_jobs.csv` in the project root.
   or `was` because we are updating how the scraper is fed see [Json_Dataset](Data/CS_Job_Titles.json)


### ⚠️ Notes

- **Scalability**: Designed for small-scale, periodic market scans not high-volume scraping.
- **LinkedIn Policy**: Automation violates LinkedIn’s ToS use at your own risk and only for personal research.