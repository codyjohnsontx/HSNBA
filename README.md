# ShelterManager JPEG Maintenance Automation

This project automates tasks on the ShelterManager website using Selenium, a web automation framework for Python. The script logs into the ShelterManager system, navigates through the menus to reach the "Jpegs Unnamed" report, and performs actions such as selecting names from the list.

I chose Selenium because the ShelterManager system is browser-based, and we needed an immediate solution that works with the current setup. While implementing an API-based solution could potentially offer a more robust and efficient approach, this project prioritizes solving the problem at hand. If time allows in the future, I plan to explore API integration to enhance the automation process further.

## Features

- Automates login to ShelterManager using credentials stored in a `.env` file.
- Navigates through the ShelterManager menu to the "Jpegs Unnamed" report.
- Selects and interacts with items in the "Jpegs Unnamed" list.
- Provides logging for debugging and tracking the automation process.

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver compatible with your Chrome browser version
- `pip` for managing Python packages

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/sheltermanager-jpeg-maintenance.git
   cd sheltermanager-jpeg-maintenance
