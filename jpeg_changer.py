import time
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

    time.sleep(3)

def navigate_to_jpegs_unnamed(driver):
    logging.info("Navigating to Jpegs Unnamed.")
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
    ).click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ui-id-15"))
    ).click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Jpegs Unnamed"))
    ).click()
    time.sleep(3)

def click_last_entry(driver):
    logging.info("Clicking on the last entry in the Jpegs Unnamed list.")
    
    # Wait for the table to load and find the last row
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    if rows:
        last_row = rows[-1]
        last_entry = last_row.find_element(By.XPATH, "./td[2]/b/a")
        last_entry.click()
        time.sleep(3)
        return True
    else:
        logging.info("No entries found in the list.")
        return False

def process_single_jpeg(driver):
    logging.info("Checking if there is a single JPEG on the page.")
    
    # Wait for elements with the class "link-edit" to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "link-edit"))
    )
    
    # Find all media links with the class "link-edit"
    media_links = driver.find_elements(By.CLASS_NAME, "link-edit")
    
    if media_links:
        try:
            # Scroll the element into view before clicking
            driver.execute_script("arguments[0].scrollIntoView(true);", media_links[0])
            time.sleep(1)  # Small delay to ensure it's in view
            
            # Make sure the element is clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "link-edit"))
            )
            
            # Click the first "link-edit" element to go to the media details
            media_links[0].click()
            time.sleep(3)
            
            logging.info("Clicked on the media link to check if it's a JPEG.")
        except Exception as e:
            logging.error(f"Could not interact with the media link: {e}")
            return
    else:
        logging.info("No media links found.")
        return
    
    # Now check if the file is a JPEG by looking at the text box content
    try:
        name_field = driver.find_element(By.XPATH, "//input[@name='mediaName']")
        media_name = name_field.get_attribute("value").lower()
        
        if media_name.endswith(".jpg") or media_name.endswith(".jpeg"):
            logging.info("Single JPEG found, renaming to 'ID'.")
            try:
                # Rename the JPEG to "ID"
                name_field.clear()
                name_field.send_keys("ID")
                
                # Click the "Change" button to save the changes
                change_button = driver.find_element(By.XPATH, "//button[contains(@class, 'asm-dialog-actionbutton')]")
                change_button.click()
                logging.info("Renamed the JPEG to 'ID' and clicked the 'Change' button.")
            except Exception as e:
                logging.error(f"Could not rename the JPEG: {e}")
            time.sleep(3)
        else:
            logging.info("The file is not a JPEG. No action taken.")
    except Exception as e:
        logging.error(f"Error checking the file type: {e}")

    # Go back to the previous page
    driver.back()
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "link-edit"))
    )
    time.sleep(3)



def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://service.sheltermanager.com/asmlogin")
        driver.implicitly_wait(2.0)

        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        login(driver, username, password)

        WebDriverWait(driver, 10).until(
            EC.url_contains("https://us10d.sheltermanager.com/main")
        )

        # Navigate to Jpegs Unnamed initially
        navigate_to_jpegs_unnamed(driver)

        # Loop to repeat the process
        while True:
            # Prompt the user to continue or stop
            user_input = input("Proceed to process the next item? (y/n): ").strip().lower()
            if user_input != 'y':
                logging.info("Stopping the process as per user request.")
                break

            # Click on the last entry in the list
            if not click_last_entry(driver):
                break  # If no entries are found, exit the loop

            # Process the entry for a single JPEG
            process_single_jpeg(driver)

            # Go back to Jpegs Unnamed to start over
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'person_media?id=')]"))
            )
            time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
