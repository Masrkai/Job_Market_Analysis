import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def get_default_browser():
    """Detect the default web browser on Linux systems"""
    try:
        # Try xdg-settings first (most reliable on modern Linux systems)
        result = subprocess.run(['xdg-settings', 'get', 'default-web-browser'],
                                    capture_output=True, text=True, check=True)
        default_browser = result.stdout.strip().lower()
        print(f"Default browser detected via xdg-settings: {default_browser}")
        return default_browser
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fall back to BROWSER environment variable
        browser_env = os.getenv('BROWSER')
        if browser_env:
            print(f"Default browser detected via BROWSER environment variable: {browser_env}")
            return os.path.basename(browser_env).lower()

    # Default fallback if detection fails
    print("Could not detect default browser")

def setup_driver():
    """Initialize the appropriate web driver based on default browser"""
    default_browser = get_default_browser()

    if 'firefox' in default_browser or 'mozilla' in default_browser:
        return setup_firefox_driver()
    elif 'chrome' in default_browser or 'chromium' in default_browser or 'brave' in default_browser:
        return setup_chrome_driver()
    else:
        # Fallback to firefox if we can't determine or recognize the browser
        print(f"Unknown browser '{default_browser}'")
        return setup_firefox_driver()

def setup_chrome_driver():
    """Initialize Chrome/Brave driver with options"""
    chrome_options = ChromeOptions()

    # Try to get Brave path from environment, fallback to Chrome
    brave_path = os.getenv("BRAVE_PATH")
    if brave_path and os.path.exists(brave_path):
        chrome_options.binary_location = brave_path

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")

    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Chrome/Brave driver failed: {e}")

def setup_firefox_driver():
    """Initialize Firefox driver with options"""
    firefox_options = FirefoxOptions()

    # Firefox options similar to Chrome's automation protection
    firefox_options.set_preference("dom.webdriver.enabled", False)
    firefox_options.set_preference("useAutomationExtension", False)

    # Start maximized
    firefox_options.add_argument("--start-maximized")

    try:
        return webdriver.Firefox(options=firefox_options)
    except Exception as e:
        print(f"Firefox driver failed: {e}")
        print("Trying with system Firefox binary path")
        # Try to specify Firefox binary location explicitly
        firefox_options.binary_location = "/usr/bin/firefox"  # Common Linux path
        return webdriver.Firefox(options=firefox_options)

# Example usage
if __name__ == "__main__":
    driver = setup_driver()
    try:
        driver.get("https://www.example.com")
        print(f"Successfully opened page with {driver.capabilities['browserName']}-based browser")
    finally:
        driver.quit()