## My code so far ##

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

def login(driver, username, password):
    logging.info("Logging in to the ShelterManager website.")
    sm_account_field = driver.find_element(By.ID, "smaccount")
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login")

    sm_account_field.send_keys('hsnba')
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

def navigate_to_jpegs_unnamed(driver):
    logging.info("Navigating to Jpegs Unnamed.")
    
    # Click on the Reports button
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
    ).click()

    # Click on Database Maintenance
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "ui-id-15"))
    ).click()

    # Click on Jpegs Unnamed
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Jpegs Unnamed"))
    ).click()

def click_last_jpeg_unnamed(driver):
    logging.info("Clicking on the last JPEG Unnamed entry.")
    # Wait for the table rows to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
    )
    
    # Find all rows in the table
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    
    if rows:
        # Click on the last row's anchor tag inside the <td><b><a> structure
        last_row = rows[-1]
        try:
            # XPath to target <a> inside <b> inside the second <td>
            last_cell = last_row.find_element(By.XPATH, "./td[2]/b/a")
            last_cell.click()
            logging.info(f"Clicked on the last JPEG unnamed entry: {last_cell.text}")
        except Exception as e:
            logging.error(f"Could not click the last entry: {e}")
    else:
        logging.info("No entries found in the list.")


def main():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Run in headless mode (no browser UI)
    options.add_argument('--disable-gpu')

    # Initialize WebDriver with the defined options
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the website
        driver.get("https://service.sheltermanager.com/asmlogin")
        driver.implicitly_wait(2.0)

        # Get username and password from environment variables (.env)
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        # Perform login
        login(driver, username, password)

        # Wait for login to complete (adjust URL accordingly)
        WebDriverWait(driver, 2).until(
            EC.url_contains("https://us10d.sheltermanager.com/main")
        )

        # Navigate to Jpegs Unnamed
        navigate_to_jpegs_unnamed(driver)

        # Click on the last JPEG unnamed entry
        click_last_jpeg_unnamed(driver)

        # Keep the browser open
        input("Press Enter to close the browser and end the script...")

    finally:
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    main()