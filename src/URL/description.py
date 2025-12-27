from bs4 import BeautifulSoup

def extract_formatted_description(soup):
    """Logic to parse the 'show-more-less-html' section."""
    sections = soup.find_all('section', class_=lambda c: c and 'show-more-less-html' in c.split())

    texts = []
    for sec in sections:
        target = sec.find('div', class_=lambda c: c and 'show-more-less-html__markup' in c.split()) or sec

        # Get the HTML content
        html_content = str(target)

        # Parse with BeautifulSoup to handle the content
        content_soup = BeautifulSoup(html_content, 'html.parser')

        # Get text with br tags converted to newlines
        # Replace <br> tags with newlines before getting text
        for br in content_soup.find_all('br'):
            br.replace_with('\n')

        # Get the text content
        text = content_soup.get_text()

        # Clean up: remove excessive whitespace and normalize line breaks
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines

        # Join with single newlines
        text_block = '\n\n'.join(lines)

        if text_block:
            texts.append(text_block)

    return '\n\n--- SECTION BREAK ---\n\n'.join(texts) if texts else None