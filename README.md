# HSNBA Maintenance Automation

Volunteer automation for the Humane Society of New Braunfels Area (HSNBA): Python and Selenium scripts that clean up records in the shelter's ShelterManager back office.

The scripts log into the ShelterManager system, navigate through the menus to access reports, and perform various automated maintenance tasks to reduce manual data entry and streamline operations.

## What was built

- **Selenium browser automation** against ShelterManager, a browser-based cloud app. Each script logs in with credentials from a `.env` file, opens a ShelterManager report, and works through the records it lists.
- **Two report-driven cleanup jobs:**
  - `jpeg_changer.py` drives the "Jpegs Unnamed" report and labels unnamed JPEGs (such as driver's license photos) as "ID", skipping PDFs and likely animal entries, with an interactive prompt per image (rename, skip, next entry, quit).
  - `oldMovements.py` drives the "Old Movements to Get Rid Of" report and corrects "Offsite Adoption" and "Working Cat" movements to Adoption.
- **Idempotent state checks** that read the current record before writing to it: the Offsite Adoption checkbox is only clicked if it is not already checked, the Feral and Working Cat flags are only added if missing, and a corrected movement no longer shows up as an Offsite Adoption or Working Cat link in the report, so a record that is already correct is left alone and a rerun does not double-apply a change.
- **Logging and error handling** with Python's `logging` module: login, navigation, and movement-change steps are logged with timestamps, and a step that fails on one record is logged and that record is skipped instead of stopping the run.

## Scripts

### 1. JPEG Maintenance (jpeg_changer.py)
This script automates the maintenance of unnamed JPEGs in the system by:
- Navigating to the "Jpegs Unnamed" report
- Skipping PDFs and likely animal entries
- Prompting for each image: rename it to "ID" (for driver's license JPGs), skip it, move to the next entry, or quit

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
  - Marks the "Was this an Offsite Adoption?" checkbox and saves
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
git clone https://github.com/codyjohnsontx/HSNBA.git
cd HSNBA
```

2. **Install required packages**:
```bash
pip install selenium python-dotenv
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