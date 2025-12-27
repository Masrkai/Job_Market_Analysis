import csv
import logging
from pathlib import Path
from helpers.resolve_path import resolve_file_path
from helpers.makefolder import ensure_dir, save_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_links_only(base_path, output_file=None):
    """
    Extract just the URL strings from all CSV files.

    Args:
        base_path: Root directory containing the CSV files
        output_file: Optional file to save URLs (one per line)

    Returns:
        List of URL strings
    """
    base_path = Path(resolve_file_path(base_path))
    all_links = []

    # Find all CSV files recursively
    csv_files = list(base_path.rglob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files to process")

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    if 'link' in row and row['link']:
                        all_links.append(row['link'].strip())

            logger.info(f"Extracted {len(all_links)} links from {csv_file.name}")

        except Exception as e:
            logger.error(f"Error reading {csv_file}: {e}")

    logger.info(f"Total links extracted: {len(all_links)}")

    if output_file:
        output_path = Path(resolve_file_path(output_file))
        ensure_dir(str(output_path.parent))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_links))

        logger.info(f"Saved {len(all_links)} URLs to {output_file}")

    return all_links


# Example usage
if __name__ == "__main__":
    scraped_data_dir = "../Data/Scraped"

    urls = get_links_only(
        scraped_data_dir,
        output_file="../Data/Processed/urls_only.txt"
    )
    print(f"Extracted {len(urls)} URLs")