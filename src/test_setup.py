"""
Test Setup Script
Verifies all components are working before running the full scraper
"""

import os
import sys
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imports():
    """Test if all required packages are installed"""
    logger.info("🔍 Testing imports...")
    
    required_packages = {
        'selenium': 'selenium',
        'bs4': 'beautifulsoup4',
        'urllib': 'built-in'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            if module == 'bs4':
                from bs4 import BeautifulSoup
            elif module == 'selenium':
                from selenium import webdriver
            elif module == 'urllib':
                from urllib.parse import quote_plus
            logger.info(f"  ✅ {module} imported successfully")
        except ImportError:
            logger.error(f"  ❌ {module} not found (install with: pip install {package})")
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        logger.info("Install with: pip install " + " ".join(missing_packages))
        return False
    
    logger.info("✅ All imports successful\n")
    return True


def test_webdriver():
    """Test if webdriver setup works"""
    logger.info("🔍 Testing WebDriver setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        logger.info("✅ WebDriver setup successful\n")
        return True
    except Exception as e:
        logger.error(f"❌ WebDriver setup failed: {str(e)}")
        logger.info("Make sure Chrome and ChromeDriver are properly installed")
        logger.info("Install with: pip install selenium")
        logger.info("Download ChromeDriver: https://chromedriver.chromium.org/\n")
        return False


def test_dataset():
    """Test if dataset file exists and is valid"""
    logger.info("🔍 Testing dataset...")
    
    dataset_path = "dataset.json"
    
    if not Path(dataset_path).exists():
        logger.warning(f"⚠️ Dataset file not found: {dataset_path}")
        logger.info("Creating sample dataset...\n")
        create_sample_dataset()
        return True
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        if not isinstance(dataset, list):
            logger.error("❌ Dataset must be a list")
            return False
        
        total_jobs = 0
        for domain in dataset:
            if 'name' not in domain or 'jobs' not in domain:
                logger.error("❌ Invalid domain structure")
                return False
            total_jobs += len(domain.get('jobs', []))
        
        logger.info(f"✅ Dataset valid: {len(dataset)} domains, {total_jobs} job titles\n")
        return True
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in dataset: {str(e)}\n")
        return False


def test_output_directory():
    """Test if output directory can be created"""
    logger.info("🔍 Testing output directory...")
    
    output_dir = "Data/Collected"
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Test write permissions
        test_file = os.path.join(output_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        logger.info(f"✅ Output directory ready: {output_dir}\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Cannot create output directory: {str(e)}\n")
        return False


def test_main_script():
    """Test if main.py exists and is valid Python"""
    logger.info("🔍 Testing main.py...")
    
    if not Path("main.py").exists():
        logger.error("❌ main.py not found\n")
        return False
    
    try:
        with open("main.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, "main.py", "exec")
        logger.info("✅ main.py is valid Python code\n")
        return True
        
    except SyntaxError as e:
        logger.error(f"❌ Syntax error in main.py: {str(e)}\n")
        return False


def test_data_fetcher():
    """Test if data_fetcher_from_Json_DS.py works"""
    logger.info("🔍 Testing data fetcher...")
    
    if not Path("data_fetcher_from_Json_DS.py").exists():
        logger.warning("⚠️ data_fetcher_from_Json_DS.py not found (optional)\n")
        return True  # Not critical
    
    try:
        from data_fetcher_from_Json_DS import DatasetFetcher
        
        fetcher = DatasetFetcher("dataset.json")
        if fetcher.load_dataset():
            jobs = fetcher.get_all_jobs_with_domains()
            logger.info(f"✅ Data fetcher working: {len(jobs)} jobs loaded\n")
            return True
        else:
            logger.error("❌ Failed to load dataset with data fetcher\n")
            return False
            
    except Exception as e:
        logger.error(f"❌ Data fetcher error: {str(e)}\n")
        return False


def create_sample_dataset():
    """Create a minimal sample dataset for testing"""
    sample_data = [
        {
            "name": "Software Engineering",
            "jobs": [
                {"name": "Software Engineer"},
                {"name": "Backend Developer"}
            ]
        }
    ]
    
    try:
        with open("dataset.json", 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2)
        logger.info("✅ Sample dataset created: dataset.json\n")
    except Exception as e:
        logger.error(f"❌ Failed to create sample dataset: {str(e)}\n")


def run_mini_test():
    """Run a minimal scraping test (just 1 job)"""
    logger.info("🔍 Running mini scraping test...")
    logger.info("This will scrape 1 job to verify everything works\n")
    
    try:
        # Import after all checks pass
        import main
        
        # Backup original config
        original_max_jobs = main.ScraperConfig.MAX_JOBS_PER_TITLE
        original_scroll = main.ScraperConfig.MAX_SCROLL_ATTEMPTS
        
        # Set to minimal for testing
        main.ScraperConfig.MAX_JOBS_PER_TITLE = 1
        main.ScraperConfig.MAX_SCROLL_ATTEMPTS = 5
        
        logger.info("⚠️ Modified config for testing:")
        logger.info(f"  - MAX_JOBS_PER_TITLE: {original_max_jobs} → 1")
        logger.info(f"  - MAX_SCROLL_ATTEMPTS: {original_scroll} → 5\n")
        
        response = input("Run mini test? This will open Chrome and scrape 1 job (y/n): ")
        
        if response.lower() == 'y':
            logger.info("\n🚀 Starting mini test...\n")
            main.main()
            logger.info("\n✅ Mini test completed!\n")
        else:
            logger.info("⏭️ Skipped mini test\n")
        
        # Restore original config
        main.ScraperConfig.MAX_JOBS_PER_TITLE = original_max_jobs
        main.ScraperConfig.MAX_SCROLL_ATTEMPTS = original_scroll
        
        return True
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Test interrupted by user\n")
        return False
    except Exception as e:
        logger.error(f"❌ Mini test failed: {str(e)}\n")
        return False


def main():
    """Run all tests"""
    logger.info("="*60)
    logger.info("🧪 LINKEDIN SCRAPER - SETUP TEST")
    logger.info("="*60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("WebDriver", test_webdriver),
        ("Dataset", test_dataset),
        ("Output Directory", test_output_directory),
        ("Main Script", test_main_script),
        ("Data Fetcher", test_data_fetcher),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {str(e)}\n")
            results[test_name] = False
    
    # Summary
    logger.info("="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    logger.info("="*60)
    
    if all_passed:
        logger.info("🎉 All tests passed! Ready to scrape.\n")
        
        # Offer to run mini test
        run_mini_test()
        
        logger.info("\n📝 Next steps:")
        logger.info("1. Review and adjust ScraperConfig in main.py")
        logger.info("2. Run: python main.py")
        logger.info("3. Check output in: Data/Collected/\n")
    else:
        logger.error("⚠️ Some tests failed. Fix issues before running scraper.\n")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())