"""
Test script to verify Instagram public profile extraction works correctly.
This script avoids using any personal login credentials and only tests
public profile access to prevent any account restrictions.
"""

import os
import sys
import logging
from automation.instagram_automation import InstagramAutomation

def test_public_profile_extraction():
    """
    Test Instagram public profile extraction with well-known public accounts
    that are unlikely to cause any issues when accessed.
    """
    print("Starting Instagram public profile extraction test...")
    print("This test will NOT use any personal login credentials.")
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create test directories if they don't exist
    os.makedirs("test_screenshots", exist_ok=True)
    
    # Initialize Instagram automation
    instagram = InstagramAutomation()
    
    # List of public Instagram accounts to test
    # These are official/verified accounts that are public and widely accessed
    test_accounts = [
        "instagram",      # Official Instagram account
        "natgeo"          # National Geographic
    ]
    
    try:
        # Test with one account only to avoid making too many requests
        test_account = test_accounts[0]
        print(f"\nTesting public profile extraction for @{test_account}...")
        
        # Extract profile data
        data_type = "Posts"
        result = instagram.extract_public_profile(test_account, data_type)
        
        # Check results
        if result:
            print(f"✓ SUCCESS: Public profile extraction worked for @{test_account}")
            print(f"Screenshot saved to: {result}")
            return True
        else:
            print(f"✗ FAILED: Public profile extraction failed for @{test_account}")
            return False
    
    except Exception as e:
        print(f"ERROR: An exception occurred during testing: {str(e)}")
        return False
    
    finally:
        # Always make sure to close the browser
        print("\nCleaning up...")
        instagram.close()
        print("Test completed.")

if __name__ == "__main__":
    success = test_public_profile_extraction()
    sys.exit(0 if success else 1)
