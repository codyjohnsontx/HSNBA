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

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def login(driver, username, password):
    try: 
        logging.info("Attempting to login..")
        driver.get('https://service.sheltermanager.com/asmlogin')
        time.sleep(.5)

        #LOGIN INFO
        driver.find_element(By.ID, "smaccount").send_keys('hsnba')
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "asm-menu-reports"))
        )
        logging.info("Login successful")
        return True
    
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False
    
def navigate_to_reports(driver):
    try:
        logging.info("Navigating to Reports section...")
        
        # Click Reports using WebDriverWait
        reports_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
        )
        reports_button.click()
                
        logging.info("Successfully navigated to report")
        return True
        
    except Exception as e:
        logging.error(f"Navigation to Reports failed: {e}")
        return False

def navigate_to_database_maintenance(driver):
    try:
        logging.info("Navigating to Reports section...")
        
        # Click Reports using WebDriverWait
        reports_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
        )
        reports_button.click()
        time.sleep(0.3)  # Small wait for animation
        
        # Click Database Maintenance
        db_maintenance = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ui-id-17"))
        )
        db_maintenance.click()
        logging.info("Successfully entered Database Maintenance")
        return True

    except Exception as e:
        logging.error(f"Navigation to Database Maintenance failed: {e}")
        return False

def main():
    driver = None
    try:
        driver = setup_driver()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        if not username or not password: 
            raise ValueError("Username or password not found in env")

        if not login(driver, username, password):
            raise Exception("Login failed")
            
        if not navigate_to_database_maintenance(driver):
            raise Exception("Navigation failed")

        print('\nProcess complete - press Enter to Quit')
        input()

    except Exception as e:
        logging.error(f"Main process error: {e}")
        print("\nAn error occurred. Press Enter to exit.")
        input()
    finally: 
        if driver: 
            driver.quit()
            logging.info("Browser closed successfully")

if __name__ == "__main__":
    main()