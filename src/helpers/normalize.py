import re


def normalize_linkedin_url(url: str) -> str:
    return re.sub(
        r"https://[a-z]{2}\.linkedin\.com",
        "https://www.linkedin.com",
        url
    )