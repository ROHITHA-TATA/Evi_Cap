import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from automation.instagram_automation import InstagramAutomation
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def test_instagram_chromedriver():
    """Test that Instagram automation can use the local ChromeDriver"""
    print("\nTesting Instagram ChromeDriver setup...")
    try:
        instagram = InstagramAutomation()
        instagram._setup_driver(headless=True)
        print("✓ Instagram ChromeDriver setup successful")
        instagram.close()
        return True
    except Exception as e:
        print(f"✗ Instagram ChromeDriver setup failed: {str(e)}")
        return False

def main():
    setup_logging()
    
    print("=== ForensicCapture Test Fixes ===")
    
    # Test Instagram ChromeDriver
    instagram_result = test_instagram_chromedriver()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Instagram ChromeDriver: {'PASS' if instagram_result else 'FAIL'}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(0)
