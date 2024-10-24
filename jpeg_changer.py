import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import logging

# Load environment variables and setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Set up and return the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def wait_for_input():
    """Wait for user input with clear prompt."""
    print("\nWhat would you like to do?")
    print("1: Rename to ID (for driver's license JPGs)")
    print("2: Skip this item")
    print("3: Go to next entry")
    print("4: Quit program")
    while True:
        try:
            choice = input("Choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("Invalid choice, please enter 1-4")
        except Exception:
            print("Invalid input, please try again")

def login(driver, username, password):
    """Log in to ShelterManager."""
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

def navigate_to_jpegs(driver):
    """Navigate to the Jpegs Unnamed section."""
    try:
        logging.info("Navigating to Jpegs Unnamed...")
        
        # Click Reports
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

        # Click Jpegs Unnamed
        jpegs = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Jpegs Unnamed"))
        )
        jpegs.click()
        time.sleep(0.5)
        
        # Verify we're on the correct page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table/tbody/tr"))
        )
        logging.info("Successfully navigated to Jpegs Unnamed")
        return True
    except Exception as e:
        logging.error(f"Navigation failed: {e}")
        return False

def safe_click(driver, element, use_js=True):
    """Safely click an element using either JavaScript or regular click."""
    try:
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)
        
        if use_js:
            driver.execute_script("arguments[0].click();", element)
        else:
            element.click()
        return True
    except Exception as e:
        logging.error(f"Click failed: {e}")
        return False

def close_dialog_if_open(driver):
    """Try to close any open dialog."""
    try:
        cancel_buttons = driver.find_elements(
            By.XPATH, 
            "//button[contains(@class, 'ui-button') and (text()='Cancel' or text()='Close')]"
        )
        if cancel_buttons:
            safe_click(driver, cancel_buttons[0])
            time.sleep(0.3)
    except Exception:
        pass

def move_dialog_down(driver, pixels=300):
    """Move the dialog box down by dragging the Edit media title."""
    try:
        time.sleep(0.5)
        
        # Find the "Edit media" title text specifically
        edit_media_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-title"))
        )
        
        print("Found Edit media title, attempting to drag...")
        
        actions = ActionChains(driver)
        # Move to the exact title element
        actions.move_to_element(edit_media_title)
        # Pause briefly to simulate human hover
        actions.pause(0.5)
        # Click and hold left mouse button
        actions.click_and_hold()
        # Pause briefly to simulate human holding
        actions.pause(0.5)
        # Move straight down
        actions.move_by_offset(0, pixels)
        # Release mouse button
        actions.release()
        # Execute the action sequence
        actions.perform()
        
        print("Drag action completed")
        return True
        
    except Exception as e:
        logging.error(f"Failed to move dialog with error: {str(e)}")
        return False

def rename_to_id(driver):
    """Rename the current file to ID."""
    try:
        # Wait for the textarea
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "medianotes"))
        )
        
        # Select all and type ID - no wait needed between these
        textarea.send_keys(Keys.COMMAND + "a")
        textarea.send_keys("ID")
        
        # Click the Change button
        change_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(@class, 'asm-dialog-actionbutton') and text()='Change']"
            ))
        )
        safe_click(driver, change_button)
        time.sleep(0.3)  # Brief wait for change to register
        
        # Go back immediately
        driver.back()
        time.sleep(0.3)
        
        return True
    except Exception as e:
        logging.error(f"Error renaming file: {e}")
        close_dialog_if_open(driver)
        return False

def is_pdf_link(link):
    """Check if the link is for a PDF file."""
    try:
        # Check multiple attributes for PDF indication
        attributes_to_check = ['title', 'text', 'data-original-title']
        for attr in attributes_to_check:
            value = link.get_attribute(attr) or ''
            if value.lower().endswith('.pdf'):
                return True
        return False
    except:
        return False

def process_entries(driver):
    """Interactive processing of entries."""
    try:
        continue_processing = True
        current_entry_index = 0
        
        while continue_processing:
            # Find entries
            entries = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr/td[2]/b/a"))
            )
            
            if not entries:
                print("No more entries found.")
                break
                
            if current_entry_index >= len(entries):
                print("Processed all entries.")
                break
            
            # Get the current entry
            entry = entries[current_entry_index]
            entry_name = entry.text
            
            # Skip if it looks like an animal entry (typically single word names)
            if len(entry_name.split()) == 1:
                print(f"Skipping likely animal entry: {entry_name}")
                current_entry_index += 1
                continue
            
            # Click the entry
            print(f"\nNavigating to entry {current_entry_index + 1} of {len(entries)}: {entry_name}")
            if not safe_click(driver, entry):
                print("Failed to click entry, trying next one...")
                current_entry_index += 1
                continue
            time.sleep(0.3)
            
            # Find edit links (dates)
            edit_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.link-edit[data-id]"))
            )
            
            print(f"Found {len(edit_links)} items to process")
            
            for i, link in enumerate(edit_links):
                # Skip PDFs automatically
                if is_pdf_link(link):
                    print(f"Skipping PDF file (item {i+1})")
                    continue
                
                date_text = link.text or "No date"
                print(f"\nProcessing item {i+1} of {len(edit_links)} (Date: {date_text})")
                
                if safe_click(driver, link):
                    time.sleep(2)  # Increased wait time to 2 seconds after clicking link
                    action = wait_for_input()
                    
                    if action == "1":
                        if rename_to_id(driver):
                            print("Successfully renamed to ID")
                            current_entry_index += 1
                            break  # Exit the loop for this entry's items
                        else:
                            print("Failed to rename")
                            close_dialog_if_open(driver)
                    elif action == "2":
                        print("Skipping this item")
                        close_dialog_if_open(driver)
                    elif action == "3":
                        print("Moving to next entry")
                        close_dialog_if_open(driver)
                        current_entry_index += 1
                        driver.back()
                        time.sleep(0.3)
                        break  # Exit the loop for this entry's items
                    elif action == "4":
                        print("Quitting program")
                        return
                else:
                    print(f"Failed to click item {i+1}")
            
            # Go back to list if we haven't already (if we skipped all items)
            if not action in ["1", "3"]:
                driver.back()
                time.sleep(0.3)
                current_entry_index += 1
            
            print("\nReady for next entry")
                
    except Exception as e:
        logging.error(f"Error in process_entries: {e}")
        print("\nAn error occurred. Press Enter to continue...")
        input()

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

        if not navigate_to_jpegs(driver):
            raise Exception("Navigation failed")

        # Start interactive processing
        process_entries(driver)

    except Exception as e:
        logging.error(f"Main process error: {e}")
        print("\nAn error occurred. Press Enter to continue...")
        input()
    finally:
        try:
            if driver:
                driver.quit()
                logging.info("Browser closed successfully")
        except Exception as e:
            logging.error(f"Error closing browser: {e}")

if __name__ == "__main__":
    main()