"""
Simple script to test if Instagram public profile functionality works 
without using any personal credentials.
"""

import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from windows_app.automation.instagram_automation import InstagramAutomation

def run_test():
    print("Testing Instagram public profile extraction...")
    print("This will NOT use your personal credentials.")
    print(f"Current working directory: {os.getcwd()}")
    
    # Test with a well-known public Instagram account
    test_account = "instagram"  # Official Instagram account, which is public
    
    try:
        # Create an instance of the automation class
        print("Creating InstagramAutomation instance...")
        instagram = InstagramAutomation()
        
        # Setup the Chrome driver
        print("Setting up Chrome driver...")
        try:
            instagram._setup_driver(headless=False)
            print("Chrome driver set up successfully!")
        except Exception as driver_error:
            print(f"Error setting up Chrome driver: {str(driver_error)}")
            raise
        
        # Navigate to the public profile
        print(f"Navigating to {test_account}'s public profile...")
        instagram.driver.get(f"https://www.instagram.com/{test_account}")
        print("Navigation successful!")
        
        # Wait a moment for the page to load
        print("Waiting for page to load...")
        import time
        time.sleep(5)
        
        # Take a screenshot
        print("Taking a screenshot...")
        screenshot_path = instagram.capture_screenshot(f"test_{test_account}")
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Close the browser
        print("Closing browser...")
        instagram.close()
        
        print("Test completed successfully!")
        return True
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
