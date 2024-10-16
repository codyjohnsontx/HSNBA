# HSNBA Maintenance Automation

This project automates tasks on the ShelterManager website using Selenium, a web automation framework for Python. The script logs into the ShelterManager system, navigates through the menus to access the "Jpegs Unnamed" report, and performs actions such as selecting names from the list and renaming them based on the Assistant Director's preferences—whether it's "ID," "Investigation Photos," "Rabies Certs," or other specified labels. The goal is to leverage automation to reduce the workload and time spent on data entry, enabling team members to focus on more important tasks such as animal care and adoption inquiries

I chose Selenium because the ShelterManager system is browser-based, and we needed a solution that could be implemented immediately with the existing setup. Although an API-based approach might offer a more robust and efficient long-term solution, this project focuses on addressing the current needs with the tools currently available to me. In the future, I hope to explore API integration to further improve the automation process.

The short-term goal is to refine this program and make it versatile enough to automate other SQL database maintenance tasks. Given the responsibility entrusted to me, I took a cautious approach, gradually building and testing the program to ensure it worked safely and effectively. The project is still undergoing further testing to strengthen the solution and ensure reliable performance.

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
   ```
