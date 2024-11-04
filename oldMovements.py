import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import logging

# Load environment variables and setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def login(driver, username, password):
    try:
        logging.info("Attempting to log in...")
        driver.get("https://service.sheltermanager.com/asmlogin")
        time.sleep(0.5)

        # Fill in login details
        driver.find_element(By.ID, "smaccount").send_keys('hsnba')
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login").click()
        
        # Wait for login to complete
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "asm-menu-reports"))
        )
        logging.info("Login successful")
        return True
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False

def navigate_to_old_movements(driver):
    try:
        logging.info("Navigating to Old Movements...")
        
        # Click Reports menu
        reports = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
        )
        reports.click()
        time.sleep(0.3)

        # Click Media submenu
        media = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ui-id-15"))
        )
        media.click()
        time.sleep(0.3)

        # Click Old Movements link
        try:
            old_movements = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Old Movements to Get Rid Of"))
            )
        except:
            old_movements = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='report?id=994']"))
            )
        
        old_movements.click()
        time.sleep(0.5)
        
        logging.info("Successfully navigated to Old Movements")
        return True
        
    except Exception as e:
        logging.error(f"Navigation failed: {e}")
        print(f"\nNavigation error: {e}")
        print("Press Enter to exit...")
        input()
        return False

def click_first_entry(driver):
    try:
        logging.info("Attempting to click first entry...")
        
        # Wait for entries to load and click first one
        first_entry = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='animal_movements?id=']"))
        )
        
        print(f"Clicking on entry: {first_entry.text}")
        first_entry.click()
        time.sleep(0.5)
        
        logging.info("Successfully clicked first entry")
        return True
        
    except Exception as e:
        logging.error(f"Failed to click first entry: {e}")
        return False

def click_offsite_adoption(driver):
    try:
        logging.info("Looking for Offsite Adoption link...")
        
        # Wait for movement links to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.link-edit"))
        )
        
        # Find all movement links
        movement_links = driver.find_elements(By.CSS_SELECTOR, "a.link-edit")
        
        # Look specifically for "Offsite Adoption"
        offsite_link = None
        for link in movement_links:
            if link.text.strip() == "Offsite Adoption":
                offsite_link = link
                break
                
        if offsite_link:
            print("Found Offsite Adoption link, clicking...")
            offsite_link.click()
            time.sleep(0.5)
            logging.info("Successfully clicked Offsite Adoption")
            return True
        else:
            print("No Offsite Adoption link found")
            return False
            
    except Exception as e:
        logging.error(f"Failed to click Offsite Adoption: {e}")
        return False

def change_movement_type(driver):
    try:
        logging.info("Attempting to change movement type to Adoption...")
        
        # Wait for select box to be present
        movement_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "type"))
        )
        
        # Create Select object and select by value
        select = Select(movement_select)
        select.select_by_value("1")  # "1" is the value for Adoption
        time.sleep(0.5)
        
        logging.info("Successfully changed movement type to Adoption")
        return True
        
    except Exception as e:
        logging.error(f"Failed to change movement type: {e}")
        return False

def check_offsite_and_save(driver):
    try:
        logging.info("Looking for Offsite Adoption checkbox...")
        
        # Find the label first
        label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Was this an Offsite Adoption?')]"))
        )
        
        # Get the 'for' attribute to find the associated checkbox
        checkbox_id = label.get_attribute('for')
        
        # Find and click the checkbox
        checkbox = driver.find_element(By.ID, checkbox_id)
        
        # Only click if it's not currently checked
        if not checkbox.is_selected():
            print("Checking Offsite Adoption checkbox...")
            checkbox.click()
            time.sleep(0.5)
        else:
            print("Checkbox was already checked")
            
        # Click the Change button with more specific selector
        print("Clicking Change button...")
        change_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'asm-dialog-actionbutton') and text()='Change']"))
        )
        change_button.click()
        time.sleep(1)  # Increased wait time after clicking
        
        logging.info("Successfully checked box and clicked Change")
        print("Changes saved - press Enter to exit")
        input()
        return True
        
    except Exception as e:
        logging.error(f"Failed to handle checkbox and save: {e}")
        print("\nError with checkbox/save. Press Enter to exit...")
        input()
        return False

def process_all_entries(driver):
    try:
        current_entry = 0
        while True:
            print("\n" + "="*50)
            print("Looking for all entries...")
            time.sleep(0.5)  # Reduced from 2
            
            # Wait for all entries to load
            entries = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='animal_movements?id=']"))
            )
            
            # Check if we've processed all entries
            if current_entry >= len(entries):
                print("All entries have been processed!")
                return True
                
            # Get the current entry
            entry = entries[current_entry]
            print(f"\nProcessing entry {current_entry + 1} of {len(entries)}")
            print(f"Entry name: {entry.text}")
            print("Clicking entry...")
            time.sleep(0.3)  # Reduced from 3
            
            # Click the entry
            entry.click()
            print("Clicked entry...")
            time.sleep(0.5)  # Reduced from 3
            
            # Process the entry
            print("\nLooking for Offsite Adoption link...")
            if not click_offsite_adoption(driver):
                print("No Offsite Adoption found for this entry, skipping...")
                print("Going back to list...")
                driver.back()
                time.sleep(0.5)  # Reduced from 3
                current_entry += 1
                continue
                
            print("\nChanging movement type...")
            time.sleep(0.5)  # Reduced from 2
            if not change_movement_type(driver):
                print("Failed to change movement type, skipping...")
                print("Going back to list...")
                driver.back()
                time.sleep(0.5)
                current_entry += 1
                continue
                
            print("\nChecking box and saving...")
            time.sleep(0.5)  # Reduced from 1.5
            if not check_offsite_and_save(driver):
                print("Failed to save changes, skipping...")
                print("Going back to list...")
                driver.back()
                time.sleep(0.5)
                current_entry += 1
                continue
            
            # After successful processing
            print("\nSuccessfully processed entry.")
            print("Going back to list...")
            driver.back()
            time.sleep(0.5)  # Reduced from 1
            current_entry += 1
                
    except Exception as e:
        logging.error(f"Error in process_all_entries: {e}")
        print(f"\nError processing entries: {e}")
        return False

def check_offsite_and_save(driver):
    try:
        logging.info("Looking for Offsite Adoption checkbox...")
        
        # Find the label first
        label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Was this an Offsite Adoption?')]"))
        )
        
        # Get the 'for' attribute to find the associated checkbox
        checkbox_id = label.get_attribute('for')
        
        # Find and click the checkbox
        checkbox = driver.find_element(By.ID, checkbox_id)
        
        # Only click if it's not currently checked
        if not checkbox.is_selected():
            print("Checking Offsite Adoption checkbox...")
            checkbox.click()
            time.sleep(0.3)  # Reduced from 0.5
        else:
            print("Checkbox was already checked")
            
        # Click the Change button with more specific selector
        print("Clicking Change button...")
        change_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'asm-dialog-actionbutton') and text()='Change']"))
        )
        change_button.click()
        time.sleep(1)  # Keep this at 1 second to ensure change is processed
        
        logging.info("Successfully checked box and clicked Change")
        return True
        
    except Exception as e:
        logging.error(f"Failed to handle checkbox and save: {e}")
        return False

def main():
    driver = None
    try:
        # Setup
        driver = setup_driver()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        if not username or not password:
            raise ValueError("Username or password not found in environment variables")

        # Login and navigate
        if not login(driver, username, password):
            raise Exception("Login failed")

        if not navigate_to_old_movements(driver):
            raise Exception("Navigation failed")
            
        # Process all entries
        process_all_entries(driver)
            
        print("\nProcess complete - press Enter to exit")
        input()

    except Exception as e:
        logging.error(f"Main process error: {e}")
        print("\nAn error occurred. Press Enter to exit...")
        input()
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed successfully")

if __name__ == "__main__":
    main()