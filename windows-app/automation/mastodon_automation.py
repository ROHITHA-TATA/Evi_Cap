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

class MastodonAutomation:
    def __init__(self):
        self.driver = None
        self.screenshots_dir = "screenshots/mastodon"
        self.data_dir = "data/mastodon"
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
            filename=f'logs/mastodon_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
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

        try:
            # Try to use ChromeDriverManager for automatic driver installation
            service = Service(ChromeDriverManager().install())
        except:
            # Fallback to using the manually downloaded ChromeDriver
            driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
            service = Service(driver_path)
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
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
    
    def extract_public_profile(self, username, instance="mastodon.social"):
        """Extract public profile information from Mastodon"""
        try:
            self._setup_driver(headless=False)  # Set to True for headless operation
            
            # Handle username format - remove @ if present
            if username.startswith('@'):
                username = username[1:]
            
            url = f"https://{instance}/@{username}"
            
            logging.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for the page to load
            time.sleep(5)
            
            # Handle any cookie/consent dialogs
            try:
                consent_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I Accept') or contains(text(), 'Agree') or contains(text(), 'Cookie')]")
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
                "instance": instance,
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
    
    def extract_hashtag(self, hashtag, instance="mastodon.social"):
        """Extract posts from a hashtag"""
        try:
            self._setup_driver(headless=False)  # Set to True for headless operation
            
            # Handle hashtag format - remove # if present
            if hashtag.startswith('#'):
                hashtag = hashtag[1:]
                
            url = f"https://{instance}/tags/{hashtag}"
            
            logging.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for the page to load
            time.sleep(5)
            
            # Handle any cookie/consent dialogs
            try:
                consent_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I Accept') or contains(text(), 'Agree') or contains(text(), 'Cookie')]")
                if consent_buttons:
                    consent_buttons[0].click()
                    time.sleep(2)
            except Exception as e:
                logging.warning(f"No consent dialog found or could not interact: {str(e)}")
            
            # Capture the hashtag page
            hashtag_screenshot = self._capture_screenshot(f"hashtag_{hashtag}")
            logging.info(f"Captured hashtag screenshot: {hashtag_screenshot}")
            
            # Scroll to get more posts
            self._scroll_page(3)  # Scroll 3 times
            posts_screenshot = self._capture_screenshot(f"hashtag_posts_{hashtag}")
            logging.info(f"Captured posts screenshot: {posts_screenshot}")
            
            # Save metadata
            metadata = {
                "hashtag": hashtag,
                "instance": instance,
                "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": url,
                "screenshots": [
                    hashtag_screenshot,
                    posts_screenshot
                ]
            }
            
            metadata_file = f"{self.data_dir}/hashtag_{hashtag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            logging.info(f"Extraction completed successfully for hashtag {hashtag}")
            return {
                "hashtag": hashtag_screenshot,
                "posts": posts_screenshot,
                "metadata": metadata_file
            }
            
        except Exception as e:
            logging.error(f"Error extracting hashtag: {str(e)}")
            # Take debug screenshot if possible
            try:
                if self.driver:
                    debug_screenshot = self._capture_screenshot(f"debug_error_hashtag_{hashtag}")
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
