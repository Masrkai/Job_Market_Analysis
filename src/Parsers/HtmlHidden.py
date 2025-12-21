import os
import sys
from bs4 import BeautifulSoup

def extract_show_more_less_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all matching sections — use exact class match (not partial)
    sections = soup.find_all('section', class_=lambda c: c and 'show-more-less-html' in c.split())

    texts = []
    for sec in sections:
        # Extract the inner div or go directly into contents
        target = sec.find('div', class_=lambda c: c and 'show-more-less-html__markup' in c) or sec

        # Get all text recursively but preserve block structure
        lines = []
        for elem in target.descendants:
            # Skip non-tag elements (e.g., NavigableString outside meaningful context)
            if not hasattr(elem, 'name'):
                continue

            if elem.name == 'p':
                text = elem.get_text(strip=True)
                if text:
                    lines.append(text)
                    lines.append('')  # blank line after paragraph

            elif elem.name == 'br':
                lines.append('')  # line break → blank line

            elif elem.name == 'li':
                text = elem.get_text(strip=True)
                if text:
                    lines.append(f"• {text}")

            elif elem.name in ['ul', 'ol']:
                # Ensure separation around lists
                if lines and lines[-1] != '':
                    lines.append('')

        # Clean up extra blank lines
        cleaned = []
        prev_blank = False
        for line in lines:
            if line == '':
                if not prev_blank:
                    cleaned.append(line)
                    prev_blank = True
            else:
                cleaned.append(line)
                prev_blank = False

        text_block = '\n'.join(cleaned).strip()
        if text_block:
            texts.append(text_block)

    return texts

def process_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback for files with different encoding
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()

    extracted_texts = extract_show_more_less_text(content)

    if not extracted_texts:
        print(f"[!] No <section class=\"show-more-less-html\"> found in {filepath}")
        return None

    # Combine all matched sections (if multiple)
    full_text = '\n\n--- SECTION BREAK ---\n\n'.join(extracted_texts)
    return full_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_job_desc.py <file1.html> [file2.html ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        if not os.path.isfile(path):
            print(f"[!] File not found: {path}")
            continue
        print(f"\n📄 Processing: {path}")
        result = process_html_file(path)
        if result:
            print("\n" + "="*60)
            print(result)
            print("="*60)
            # Optional: save output
            output_path = os.path.splitext(path)[0] + "_extracted.txt"
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write(result)
            print(f"✅ Saved extracted text to: {output_path}")