# HSNBA Maintenance Automation

This project automates tasks on the ShelterManager website using Selenium, a web automation framework for Python. The scripts log into the ShelterManager system, navigate through the menus to access reports, and perform various automated maintenance tasks to reduce manual data entry and streamline operations.

## Scripts

### 1. JPEG Maintenance (jpeg_changer.py)
This script automates the maintenance of unnamed JPEGs in the system by:
- Navigating to the "Jpegs Unnamed" report
- Processing each entry to rename images based on specific criteria (ID, Investigation Photos, Rabies Certs, etc.)
- Providing interactive options for handling different types of entries

### 2. Movement Records Maintenance (oldMovements.py)
This script automates the maintenance of old movement records by:
- Navigating to the "Old Movements to Get Rid Of" report
- Processing entries that contain either "Offsite Adoption" or "Working Cat" movements
- For Offsite Adoption entries:
  - Changes movement type to Adoption
  - Marks the "Was this an Offsite Adoption?" checkbox
  - Saves changes
- For Working Cat entries:
  - Changes movement type to Adoption
  - Navigates to the animal's record
  - Adds both "Feral" and "Working Cat" flags
  - Saves all changes

## Technical Implementation

I chose Selenium because the ShelterManager system is a browser-based cloud app, and we needed a solution that could be implemented immediately with the existing setup. Although an API-based approach might offer a more robust and efficient long-term solution, this project focuses on addressing the current needs with the tools currently available.

Both scripts include comprehensive error handling, logging, and progress tracking to ensure reliable operation and easy troubleshooting. The automation is designed to be cautious and verify each step before proceeding, maintaining data integrity throughout the process.

## Features
* Secure login using credentials stored in a `.env` file
* Navigation through various ShelterManager menus and reports
* Automated processing of JPEGs and movement records
* Comprehensive logging for debugging and tracking
* Error handling and recovery mechanisms
* Progress tracking and status updates

## Prerequisites
* Python 3.7 or higher
* Google Chrome browser installed
* ChromeDriver compatible with your Chrome browser version
* `pip` for managing Python packages

## Installation
1. **Clone the repository**:
```bash
git clone https://github.com/your-username/sheltermanager-maintenance.git
cd sheltermanager-maintenance
```

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the project root with your credentials:
```
USERNAME=your_username
PASSWORD=your_password
```

## Usage
To run the JPEG maintenance script:
```bash
python jpeg_changer.py
```

To run the movement records maintenance script:
```bash
python oldMovements.py
```

## Future Development
The short-term goal is to continue refining these programs and expanding automation capabilities for other database maintenance tasks. Future improvements may include:
- API integration when available
- Additional automation scripts for other maintenance tasks
- Enhanced error recovery mechanisms
- Performance optimizations
- User interface improvements

The project is continuously being tested and improved to ensure reliable performance and meet the evolving needs of the shelter's data management requirements.