"""
Basic test script to verify that Python and logging are working correctly.
This doesn't use Selenium or any web automation, just basic Python functionality.
"""

import os
import sys
import datetime
import logging

# Create a logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), "test_logs")
os.makedirs(logs_dir, exist_ok=True)

# Set up logging
log_file = os.path.join(logs_dir, f"basic_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_basic_test():
    """Run a basic test to verify Python and logging are working"""
    print(f"Starting basic test at {datetime.datetime.now()}")
    print(f"Log file: {log_file}")
    
    # Log some basic information
    logging.info("Basic test started")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current working directory: {os.getcwd()}")
    
    # Create a simple text file
    test_file = os.path.join(os.path.dirname(__file__), "test_output.txt")
    try:
        with open(test_file, "w") as f:
            f.write("This is a test file.\n")
            f.write(f"Created at: {datetime.datetime.now()}\n")
            f.write(f"Python version: {sys.version}\n")
        
        print(f"Test file created at: {test_file}")
        logging.info(f"Test file created at: {test_file}")
        
        # Read the file back
        with open(test_file, "r") as f:
            content = f.read()
        
        print(f"File content:\n{content}")
        logging.info("File successfully read back")
        
        print("Basic test completed successfully!")
        logging.info("Basic test completed successfully")
        return True
        
    except Exception as e:
        error_msg = f"Error during test: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        return False

if __name__ == "__main__":
    success = run_basic_test()
    sys.exit(0 if success else 1)
