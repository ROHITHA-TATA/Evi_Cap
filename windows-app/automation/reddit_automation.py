from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime
import json
from PIL import Image
import logging
import random

class RedditAutomation:
    def __init__(self):
        self.driver = None
        self.screenshots_dir = "screenshots/reddit"
        self.data_dir = "data/reddit"
        self._create_directories()
        self._setup_logging()
        
    def _create_directories(self):
        """Create necessary directories for storing data"""
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename=f'logs/reddit_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _setup_driver(self, headless=False):
        """Set up the Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add additional arguments to make the browser look more like a regular user
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Try to use local ChromeDriver first
        try:
            driver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "drivers", "chromedriver.exe")
            if os.path.exists(driver_path):
                logging.info(f"Using local ChromeDriver from {driver_path}")
                service = Service(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                return
        except Exception as e:
            logging.warning(f"Failed to use local ChromeDriver: {str(e)}")
        
        # Fallback to WebDriver Manager
        try:
            logging.info("Attempting to use ChromeDriverManager")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            logging.error(f"Error setting up Chrome WebDriver: {str(e)}")
            raise
        
        # Execute CDP commands to prevent detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def _capture_screenshot(self, element_name):
        """Capture and save a screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{element_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logging.info(f"Screenshot saved: {filename}")
        return filename
    
    def extract_public_profile(self, username):
        """Extract public profile information from Reddit"""
        try:
            self._setup_driver(headless=False)  # Set to True for headless operation
            url = f"https://www.reddit.com/user/{username}"
            
            logging.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for the page to load
            time.sleep(5)
            
            # Handle any consent dialogs that might appear
            try:
                consent_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I Accept') or contains(text(), 'Agree')]")
                if consent_buttons:
                    consent_buttons[0].click()
                    time.sleep(2)
            except Exception as e:
                logging.warning(f"No consent dialog found or could not interact: {str(e)}")
            
            # Capture the profile page
            profile_screenshot = self._capture_screenshot(f"public_profile_{username}")
            logging.info(f"Captured profile screenshot: {profile_screenshot}")
            
            # Extract posts (scroll down to capture more posts)
            self._scroll_page(3)  # Scroll 3 times
            posts_screenshot = self._capture_screenshot(f"public_posts_{username}")
            logging.info(f"Captured posts screenshot: {posts_screenshot}")
            
            # Save metadata
            metadata = {
                "username": username,
                "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": url,
                "screenshots": [
                    profile_screenshot,
                    posts_screenshot
                ]
            }
            
            metadata_file = f"{self.data_dir}/{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            logging.info(f"Extraction completed successfully for {username}")
            return {
                "profile": profile_screenshot,
                "posts": posts_screenshot,
                "metadata": metadata_file
            }
            
        except Exception as e:
            logging.error(f"Error extracting public profile: {str(e)}")
            # Take debug screenshot if possible
            try:
                if self.driver:
                    debug_screenshot = self._capture_screenshot(f"debug_error_{username}")
                    logging.info(f"Debug screenshot captured: {debug_screenshot}")
            except:
                pass
            return None
        finally:
            if self.driver:
                self.driver.quit()
    
    def extract_subreddit(self, subreddit_name):
        """Extract posts from a subreddit"""
        try:
            self._setup_driver(headless=False)  # Set to True for headless operation
            url = f"https://www.reddit.com/r/{subreddit_name}"
            
            logging.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for the page to load
            time.sleep(5)
            
            # Handle any consent dialogs that might appear
            try:
                consent_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I Accept') or contains(text(), 'Agree')]")
                if consent_buttons:
                    consent_buttons[0].click()
                    time.sleep(2)
            except Exception as e:
                logging.warning(f"No consent dialog found or could not interact: {str(e)}")
            
            # Capture the subreddit page
            subreddit_screenshot = self._capture_screenshot(f"subreddit_{subreddit_name}")
            logging.info(f"Captured subreddit screenshot: {subreddit_screenshot}")
            
            # Scroll to get more posts
            self._scroll_page(3)  # Scroll 3 times
            posts_screenshot = self._capture_screenshot(f"subreddit_posts_{subreddit_name}")
            logging.info(f"Captured posts screenshot: {posts_screenshot}")
            
            # Save metadata
            metadata = {
                "subreddit": subreddit_name,
                "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": url,
                "screenshots": [
                    subreddit_screenshot,
                    posts_screenshot
                ]
            }
            
            metadata_file = f"{self.data_dir}/subreddit_{subreddit_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            logging.info(f"Extraction completed successfully for subreddit {subreddit_name}")
            return {
                "subreddit": subreddit_screenshot,
                "posts": posts_screenshot,
                "metadata": metadata_file
            }
            
        except Exception as e:
            logging.error(f"Error extracting subreddit: {str(e)}")
            # Take debug screenshot if possible
            try:
                if self.driver:
                    debug_screenshot = self._capture_screenshot(f"debug_error_subreddit_{subreddit_name}")
                    logging.info(f"Debug screenshot captured: {debug_screenshot}")
            except:
                pass
            return None
        finally:
            if self.driver:
                self.driver.quit()
    
    def _scroll_page(self, num_scrolls=3):
        """Scroll down the page to load more content"""
        for i in range(num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load
