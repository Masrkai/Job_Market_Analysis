def extract_salary_range(soup):
    """Logic to parse the salary range from compensation section."""
    # Find matching sections - exact class match logic
    salary_sections = soup.find_all('div', class_=lambda c: c and 'compensation__salary-range' in c.split())

    for section in salary_sections:
        # Look for the salary div within the salary range section
        salary_div = section.find('div', class_=lambda c: c and 'salary' in c.split() and 'compensation__salary' in c.split())

        if salary_div:
            salary_text = salary_div.get_text(strip=True)
            if salary_text:
                return salary_text

    # Alternative: look directly for salary div if not found in salary-range section
    salary_divs = soup.find_all('div', class_=lambda c: c and 'salary' in c.split() and 'compensation__salary' in c.split())

    for salary_div in salary_divs:
        salary_text = salary_div.get_text(strip=True)
        if salary_text:
            return salary_text

    return None



def extract_salary_safe(soup):
    """Safely extract salary handling different return types from extract_salary_range"""
    try:
        salary_data = extract_salary_range(soup)
        
        if salary_data is None:
            return "N/A"
        elif isinstance(salary_data, str):
            return salary_data.strip() if salary_data.strip() else "N/A"
        elif hasattr(salary_data, 'get_text'):
            # BeautifulSoup element
            text = salary_data.get_text(strip=True)
            return text if text else "N/A"
        else:
            # Try to convert to string as last resort
            return str(salary_data) if salary_data else "N/A"
    except Exception as e:
        print(f"Warning: Error extracting salary: {e}")
        return "N/A"