"""
WebDriver Setup Module
Configure and initialize Chrome WebDriver for scraping
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging

logger = logging.getLogger(__name__)


def setup_driver(headless=False, incognito=True):
    """
    Setup Chrome WebDriver with appropriate options
    
    Args:
        headless: Run browser in headless mode (no GUI)
        incognito: Run in incognito/private mode
        
    Returns:
        WebDriver instance
        
    Raises:
        Exception: If WebDriver setup fails
    """
    try:
        options = Options()
        
        # Window settings
        if not headless:
            options.add_argument("--start-maximized")
        
        # Privacy settings
        if incognito:
            options.add_argument("--incognito")
        
        # Anti-detection settings
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        
        # Performance settings
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        
        # User agent (optional - makes requests look more human)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Initialize driver
        driver = webdriver.Chrome(options=options)
        
        # Additional anti-detection
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        logger.info("✅ WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize WebDriver: {str(e)}")
        logger.error("\nTroubleshooting:")
        logger.error("1. Make sure Chrome browser is installed")
        logger.error("2. Install selenium: pip install selenium")
        logger.error("3. ChromeDriver should be auto-downloaded by selenium")
        logger.error("   If not, download from: https://chromedriver.chromium.org/")
        raise


def test_driver():
    """Test if WebDriver works"""
    try:
        logger.info("Testing WebDriver setup...")
        driver = setup_driver(headless=True)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        logger.info(f"✅ Test successful! Page title: {title}")
        return True
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test the driver
    test_driver()
