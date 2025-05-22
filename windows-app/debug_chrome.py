"""
Debug script to test if Chrome WebDriver works properly.
This will just open a local HTML file to avoid any network issues.
"""

import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_chrome_driver():
    """Simple test to check if Chrome WebDriver works properly"""
    print("Starting Chrome WebDriver test...")
    
    # Create a simple HTML file
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chrome WebDriver Test</title>
    </head>
    <body>
        <h1>Chrome WebDriver Test</h1>
        <p>If you can see this page, Chrome WebDriver is working!</p>
        <p>Current time: <span id="time"></span></p>
        <script>
            document.getElementById('time').textContent = new Date().toString();
        </script>
    </body>
    </html>
    """
    
    # Create the HTML file
    html_path = os.path.join(os.path.dirname(__file__), "debug_test.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    
    # Get the full file path as URL
    file_url = f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}"
    print(f"Created test HTML file at: {file_url}")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # No headless so we can see what's happening
    
    try:
        print("Trying to use local ChromeDriver...")
        # Try to use local ChromeDriver first
        driver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "drivers", "chromedriver.exe")
        if os.path.exists(driver_path):
            print(f"Found local ChromeDriver at {driver_path}")
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Local ChromeDriver loaded successfully!")
        else:
            print("Local ChromeDriver not found, using WebDriver Manager...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("WebDriver Manager setup completed!")
        
        # Open the HTML file
        print(f"Navigating to {file_url}...")
        driver.get(file_url)
        print("Navigation successful!")
        
        # Wait to see the page
        print("Waiting for 5 seconds...")
        time.sleep(5)
        
        # Take a screenshot
        screenshot_path = os.path.join(os.path.dirname(__file__), "chrome_debug_test.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Close the browser
        driver.quit()
        print("Test completed successfully!")
        return True
    
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
if __name__ == "__main__":
    success = test_chrome_driver()
    sys.exit(0 if success else 1)
