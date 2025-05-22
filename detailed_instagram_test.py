"""
Simplified Instagram test that saves detailed logs to a file
to diagnose any issues with the Instagram automation.
"""
import os
import sys
import time
import logging
import traceback

# Set up detailed logging to file
log_dir = os.path.join(os.path.dirname(__file__), "debug_logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"instagram_debug_{time.strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add console handler to see logs in console as well
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def log_info(message):
    """Log to both console and file"""
    logging.info(message)
    print(message)

# Import the Instagram automation class - handle import errors gracefully
try:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from windows_app.automation.instagram_automation import InstagramAutomation
    log_info("Successfully imported InstagramAutomation")
except Exception as e:
    error_msg = f"Failed to import InstagramAutomation: {str(e)}"
    logging.error(error_msg)
    logging.error(traceback.format_exc())
    print(error_msg)
    sys.exit(1)

def run_test():
    """Test Instagram public profile extraction with detailed logging"""
    log_info("\n=== Instagram Public Profile Test ===")
    log_info(f"Log file: {log_file}")
    log_info(f"Current working directory: {os.getcwd()}")
    log_info(f"Python version: {sys.version}")
    
    # List available files in the drivers directory
    drivers_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "drivers")
    log_info(f"Checking drivers directory: {drivers_dir}")
    if os.path.exists(drivers_dir):
        log_info(f"Files in drivers directory: {os.listdir(drivers_dir)}")
    else:
        log_info("Drivers directory not found")
    
    # Test with a well-known public Instagram account
    test_account = "instagram"  # Official Instagram account, which is public
    
    try:
        # Create an instance of the automation class
        log_info("Creating InstagramAutomation instance...")
        instagram = InstagramAutomation()
        
        # Set up Chrome driver
        log_info("Setting up Chrome driver...")
        try:
            instagram._setup_driver(headless=False)
            log_info("Chrome driver setup successful!")
        except Exception as e:
            logging.error(f"Chrome driver setup failed: {str(e)}")
            logging.error(traceback.format_exc())
            raise
        
        # Navigate to the public profile
        log_info(f"Navigating to {test_account}'s public profile...")
        instagram.driver.get(f"https://www.instagram.com/{test_account}")
        log_info("Navigation successful")
        
        # Wait for page to load
        log_info("Waiting for page to load (5 seconds)...")
        time.sleep(5)
        
        # Take screenshot
        log_info("Taking screenshot...")
        screenshot_path = instagram.capture_screenshot(f"test_{test_account}")
        log_info(f"Screenshot saved to: {screenshot_path}")
        
        # Try to extract public posts
        log_info("Attempting to extract public posts...")
        result = instagram._extract_public_posts()
        if result:
            log_info(f"Public posts extraction successful. Screenshot: {result}")
        else:
            log_info("Public posts extraction failed")
        
        # Close the browser
        log_info("Closing browser...")
        instagram.close()
        
        log_info("Test completed successfully!")
        log_info(f"For detailed logs, check: {log_file}")
        return True
        
    except Exception as e:
        error_msg = f"Error during test: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        print(error_msg)
        print(f"For detailed logs, check: {log_file}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
