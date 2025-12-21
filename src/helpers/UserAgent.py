import random
from datetime import datetime

def generate_advanced_ua():
    """Generate a realistic random User Agent string"""

    # OS configurations with realistic version ranges
    os_configs = {
        "windows": [
            "Windows NT 10.0; Win64; x64",  # Windows 10/11
            "Windows NT 6.3; Win64; x64",   # Windows 8.1
            "Windows NT 6.1; Win64; x64",   # Windows 7
        ],
        "mac": [
            "Macintosh; Intel Mac OS X 10_15_7",  # Catalina
            "Macintosh; Intel Mac OS X 11_6_8",   # Big Sur
            "Macintosh; Intel Mac OS X 12_6_0",   # Monterey
            "Macintosh; Intel Mac OS X 13_5_2",   # Ventura
            "Macintosh; Intel Mac OS X 14_1_0",   # Sonoma
        ],
        "linux": [
            "X11; Linux x86_64",
            "X11; Ubuntu; Linux x86_64",
            "X11; Fedora; Linux x86_64",
            "X11; Linux Mint; Linux x86_64",

        ],
        "android": [
            f"Linux; Android {v}; SM-G991B" for v in ["11", "12", "13", "14"]
        ] + [
            f"Linux; Android {v}; Pixel 7" for v in ["13", "14"]
        ],
        "ios": [
            f"iPhone; CPU iPhone OS {v} like Mac OS X"
            for v in ["15_0", "16_0", "17_0", "17_2"]
        ] + [
            f"iPad; CPU OS {v} like Mac OS X"
            for v in ["15_0", "16_0", "17_0"]
        ]
    }

    # Browser configurations with engine details
    browsers = {
        "chrome": {
            "name": "Chrome",
            "engine": "AppleWebKit/537.36 (KHTML, like Gecko)",
            "version_range": (115, 123),
            "compatible_os": ["windows", "mac", "linux", "android"]
        },
        "firefox": {
            "name": "Firefox",
            "engine": "Gecko/20100101",
            "version_range": (115, 122),
            "compatible_os": ["windows", "mac", "linux", "android"]
        },
        "safari": {
            "name": "Safari",
            "engine": "AppleWebKit/605.1.15 (KHTML, like Gecko)",
            "version_range": (15, 17),
            "compatible_os": ["mac", "ios"]
        },
        "edge": {
            "name": "Edg",
            "engine": "AppleWebKit/537.36 (KHTML, like Gecko)",
            "version_range": (115, 123),
            "compatible_os": ["windows", "mac"]
        },
        "opera": {
            "name": "OPR",
            "engine": "AppleWebKit/537.36 (KHTML, like Gecko)",
            "version_range": (100, 108),
            "compatible_os": ["windows", "mac", "linux"]
        }
    }

    # Select a random browser
    browser_key = random.choice(list(browsers.keys()))
    browser = browsers[browser_key]

    # Select compatible OS
    compatible_os_list = browser["compatible_os"]
    os_type = random.choice(compatible_os_list)
    os_string = random.choice(os_configs[os_type])

    # Generate browser version
    major = random.randint(*browser["version_range"])
    minor = 0
    build = random.randint(5000, 6500) if browser_key in ["chrome", "edge", "opera"] else random.randint(0, 20)
    patch = random.randint(0, 200) if browser_key in ["chrome", "edge", "opera"] else 0

    # Build User Agent based on browser type
    if browser_key == "firefox":
        if os_type == "android":
            ua = f"Mozilla/5.0 ({os_string}) Gecko/{major}.0 Firefox/{major}.0"
        else:
            ua = f"Mozilla/5.0 ({os_string}; rv:{major}.0) Gecko/20100101 Firefox/{major}.0"

    elif browser_key == "safari":
        if os_type == "ios":
            version = f"{major}.{random.randint(0, 6)}"
            if "iPhone" in os_string:
                ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Version/{version} Mobile/15E148 Safari/604.1"
            else:  # iPad
                ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Version/{version} Mobile/15E148 Safari/604.1"
        else:
            version = f"{major}.{random.randint(0, 6)}"
            ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Version/{version} Safari/605.1.15"

    elif browser_key == "chrome":
        chrome_ver = f"{major}.{minor}.{build}.{patch}"
        if os_type == "android":
            ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Chrome/{chrome_ver} Mobile Safari/537.36"
        else:
            ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Chrome/{chrome_ver} Safari/537.36"

    elif browser_key == "edge":
        chrome_ver = f"{major}.{minor}.{build}.{patch}"
        edge_ver = f"{major}.{minor}.{random.randint(1000, 2000)}.{random.randint(0, 100)}"
        ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Chrome/{chrome_ver} Safari/537.36 Edg/{edge_ver}"

    elif browser_key == "opera":
        chrome_ver = f"{major}.{minor}.{build}.{patch}"
        opera_ver = f"{random.randint(100, 108)}.{minor}.{random.randint(4000, 5000)}.{random.randint(0, 100)}"
        ua = f"Mozilla/5.0 ({os_string}) {browser['engine']} Chrome/{chrome_ver} Safari/537.36 OPR/{opera_ver}"

    return ua

def generate_multiple_uas(count=5):
    """Generate multiple unique User Agents"""
    uas = set()
    attempts = 0
    max_attempts = count * 10

    while len(uas) < count and attempts < max_attempts:
        uas.add(generate_advanced_ua())
        attempts += 1

    return list(uas)

def get_ua_info(ua):
    """Extract information from a User Agent string"""
    info = {
        "browser": "Unknown",
        "os": "Unknown",
        "device": "Desktop"
    }

    # Detect browser
    if "Firefox" in ua:
        info["browser"] = "Firefox"
    elif "Edg/" in ua:
        info["browser"] = "Edge"
    elif "OPR/" in ua or "Opera" in ua:
        info["browser"] = "Opera"
    elif "Chrome" in ua:
        info["browser"] = "Chrome"
    elif "Safari" in ua and "Chrome" not in ua:
        info["browser"] = "Safari"

    # Detect OS - Check iOS devices FIRST before Mac OS X
    if "iPhone" in ua:
        info["os"] = "iOS"
        info["device"] = "Mobile"
    elif "iPad" in ua:
        info["os"] = "iOS"
        info["device"] = "Tablet"
    elif "Android" in ua:
        info["os"] = "Android"
        info["device"] = "Mobile"
    elif "Windows" in ua:
        info["os"] = "Windows"
    elif "Mac OS X" in ua:
        info["os"] = "macOS"
    elif "Linux" in ua:
        info["os"] = "Linux"

    return info

if __name__ == "__main__":

    print("=== Single User Agent ===")
    ua = generate_advanced_ua()
    print(ua)
    print(f"\nInfo: {get_ua_info(ua)}")

    print("\n=== Multiple User Agents ===")
    for i, ua in enumerate(generate_multiple_uas(10), 1):
        info = get_ua_info(ua)
        print(f"{i}. [{info['browser']} - {info['os']} - {info['device']}]")
        print(f"   {ua}\n")


"""
 Output should be like

=== Single User Agent ===
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5664.153 Safari/537.36 OPR/101.0.4967.65

Info: {'browser': 'Opera', 'os': 'Windows', 'device': 'Desktop'}

=== Multiple User Agents ===
1. [Safari - macOS - Desktop]
   Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15

2. [Opera - Linux - Desktop]
   Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.6113.49 Safari/537.36 OPR/108.0.4512.90

3. [Edge - macOS - Desktop]
   Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5783.30 Safari/537.36 Edg/119.0.1097.52

4. [Opera - macOS - Desktop]
   Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5659.132 Safari/537.36 OPR/108.0.4098.78

5. [Firefox - Linux - Desktop]
   Mozilla/5.0 (X11; Linux Mint; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0

6. [Safari - macOS - Desktop]
   Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15

7. [Edge - Windows - Desktop]
   Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.5828.36 Safari/537.36 Edg/120.0.1279.76

8. [Firefox - Android - Mobile]
   Mozilla/5.0 (Linux; Android 11; SM-G991B) Gecko/120.0 Firefox/120.0

9. [Opera - Windows - Desktop]
   Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.6054.76 Safari/537.36 OPR/103.0.4586.28

10. [Edge - Windows - Desktop]
   Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6461.95 Safari/537.36 Edg/121.0.1363.88

"""