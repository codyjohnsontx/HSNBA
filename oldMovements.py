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
        time.sleep(1)

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
        time.sleep(1)

        # Click Media submenu
        media = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ui-id-15"))
        )
        media.click()
        time.sleep(1)

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
        time.sleep(1)
        
        logging.info("Successfully navigated to Old Movements")
        return True
        
    except Exception as e:
        logging.error(f"Navigation failed: {e}")
        print(f"\nNavigation error: {e}")
        return False

def check_movement_type(driver):
    try:
        logging.info("Looking for movement links...")
        
        # Wait for movement links to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.link-edit"))
        )
        
        # Find all movement links
        movement_links = driver.find_elements(By.CSS_SELECTOR, "a.link-edit")
        
        # Look for both types
        offsite_link = None
        working_cat_link = None
        
        for link in movement_links:
            text = link.text.strip()
            if text == "Offsite Adoption":
                offsite_link = link
                break
            elif text == "Working Cat":
                working_cat_link = link
                break
                
        if offsite_link:
            print("Found Offsite Adoption link, clicking...")
            offsite_link.click()
            time.sleep(1)
            logging.info("Successfully clicked Offsite Adoption")
            return "offsite"
        elif working_cat_link:
            print("Found Working Cat link, clicking...")
            working_cat_link.click()
            time.sleep(1)
            logging.info("Successfully clicked Working Cat")
            return "working_cat"
        else:
            print("No relevant movement type found")
            return None
            
    except Exception as e:
        logging.error(f"Failed to check movement type: {e}")
        return None

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
        time.sleep(1)
        
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
            time.sleep(1)
        else:
            print("Checkbox was already checked")
            
        # Click the Change button
        print("Clicking Change button...")
        change_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'asm-dialog-actionbutton') and text()='Change']"))
        )
        change_button.click()
        time.sleep(2)
        
        logging.info("Successfully checked box and clicked Change")
        return True
        
    except Exception as e:
        logging.error(f"Failed to handle checkbox and save: {e}")
        return False

def handle_working_cat_flags(driver):
    try:
        print("Clicking on Animal tab...")
        animal_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-tabs-anchor[href^='animal?id=']"))
        )
        animal_tab.click()
        time.sleep(2)

        # Find the flags dropdown
        print("Looking for flags dropdown...")
        flags_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "asmSelect"))
        )
        select = Select(flags_select)

        # Get all selected options
        selected_values = [option.get_attribute('value') for option in select.all_selected_options]
        
        # Check current status of flags
        feral_selected = "Feral" in selected_values
        working_cat_selected = "Working Cat" in selected_values

        # Log the current status
        print("\nCurrent flag status:")
        print(f"Feral flag: {'Already selected' if feral_selected else 'Not selected'}")
        print(f"Working Cat flag: {'Already selected' if working_cat_selected else 'Not selected'}")

        # Handle all possible cases
        if feral_selected and working_cat_selected:
            print("Both flags are already selected - no changes needed")
        elif feral_selected:
            print("Only Feral flag is selected - adding Working Cat flag...")
            try:
                select.select_by_value("Working Cat")
                time.sleep(1)
            except Exception as e:
                print(f"Note: Could not add Working Cat flag: {e}")
        elif working_cat_selected:
            print("Only Working Cat flag is selected - adding Feral flag...")
            try:
                select.select_by_value("Feral")
                time.sleep(1)
            except Exception as e:
                print(f"Note: Could not add Feral flag: {e}")
        else:
            print("Neither flag is selected - adding both flags...")
            try:
                print("Adding Feral flag...")
                select.select_by_value("Feral")
                time.sleep(1)
                print("Adding Working Cat flag...")
                select.select_by_value("Working Cat")
                time.sleep(1)
            except Exception as e:
                print(f"Note: Could not add flags: {e}")

        # Verify final state
        final_values = [option.get_attribute('value') for option in select.all_selected_options]
        print("\nFinal flag status:")
        print(f"Feral flag: {'Selected' if 'Feral' in final_values else 'Not selected'}")
        print(f"Working Cat flag: {'Selected' if 'Working Cat' in final_values else 'Not selected'}")
        
        # Click Save button regardless of whether changes were made
        print("\nClicking Save button...")
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-save"))
        )
        save_button.click()
        time.sleep(2)
        
        print("Successfully processed animal flags")
        return True
        
    except Exception as e:
        logging.error(f"Failed to handle working cat flags: {e}")
        print(f"Error details: {e}")
        return False

def process_all_entries(driver):
    try:
        current_entry = 0
        while True:
            print("\n" + "="*50)
            print("Looking for all entries...")
            time.sleep(1)
            
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
            time.sleep(1)
            
            # Click the entry
            entry.click()
            time.sleep(1)
            
            # Check what type of movement it is
            movement_type = check_movement_type(driver)
            
            if movement_type is None:
                print("No relevant movement found, skipping...")
                print("Going back to list...")
                driver.back()
                time.sleep(1)
                current_entry += 1
                continue
                
            if movement_type == "offsite":
                # Handle Offsite Adoption
                print("\nHandling Offsite Adoption...")
                if not change_movement_type(driver):
                    print("Failed to change movement type, skipping...")
                    print("Going back to list...")
                    driver.back()
                    time.sleep(1)
                    current_entry += 1
                    continue
                    
                if not check_offsite_and_save(driver):
                    print("Failed to save changes, skipping...")
                    print("Going back to list...")
                    driver.back()
                    time.sleep(1)
                    current_entry += 1
                    continue
                    
            elif movement_type == "working_cat":
                print("\nHandling Working Cat...")
                # Change movement type to Adoption
                if not change_movement_type(driver):
                    print("Failed to change movement type, skipping...")
                    print("Going back to list...")
                    driver.back()
                    time.sleep(1)
                    current_entry += 1
                    continue
                
                # Check the Offsite Adoption box and save
                if not check_offsite_and_save(driver):
                    print("Failed to save changes, skipping...")
                    print("Going back to list...")
                    driver.back()
                    time.sleep(1)
                    current_entry += 1
                    continue
                
                # Handle the flags
                if not handle_working_cat_flags(driver):
                    print("Failed to update animal flags, skipping...")
                    driver.back()
                    time.sleep(1)
                    current_entry += 1
                    continue
                
                # Go back twice after handling flags
                print("Going back to movement page...")
                driver.back()
                time.sleep(1)
                print("Going back to list...")
                driver.back()
                time.sleep(1)
            
            current_entry += 1
                
    except Exception as e:
        logging.error(f"Error in process_all_entries: {e}")
        print(f"\nError processing entries: {e}")
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