# Social Media Evidence Tool

A desktop application for automated extraction and documentation of social media evidence for investigative purposes.

## Features

- Support for multiple social media platforms (Facebook, Twitter, Instagram, Reddit, Mastodon, etc.)
- Automated login and data extraction
- Public profile extraction without authentication
- Screenshot capture of posts, messages, friends lists, etc.
- PDF report generation with metadata
- User-friendly interface

## Requirements

- Python 3.8 or higher
- Chrome browser installed
- Windows 10 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-media-evidence-tool.git
cd social-media-evidence-tool
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python windows-app/main.py
```

2. Select the social media platform
3. Enter credentials
4. Choose the type of data to extract
5. Click "Extract Data"
6. Find the generated report in the `reports` directory

## Security Notes

- Credentials are stored only in memory during the session
- All data is processed locally
- Screenshots and reports are saved locally

## Legal Disclaimer

This tool is intended for use by authorized personnel only. Users are responsible for ensuring compliance with:
- Applicable laws and regulations
- Platform terms of service
- Privacy laws and data protection regulations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


