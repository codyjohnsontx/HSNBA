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

# def navigate_to_jpegs(driver):
#    try:
#        logging.info("Navigating to Jpegs Unnamed...")
       
#        # Click Reports
#        reports = WebDriverWait(driver, 10).until(
#            EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
#        )
#        reports.click()
#        time.sleep(0.3)

#        # Click Media submenu
#        media = WebDriverWait(driver, 10).until(
#            EC.element_to_be_clickable((By.ID, "ui-id-15"))
#        )
#        media.click()
#        time.sleep(0.3)

#        # click Jpegs Unnamed
#        jpegs = WebDriverWait(driver, 10).until(
#            EC.element_to_be_clickable((By.LINK_TEXT, "Jpegs Unnamed"))
#        )
#        jpegs.click()
#        time.sleep(0.5)
       
#        # Verify on the correct page
#        WebDriverWait(driver, 10).until(
#            EC.presence_of_element_located((By.XPATH, "//table/tbody/tr"))
#        )
#        logging.info("Successfully navigated to Jpegs Unnamed")
#        return True
#    except Exception as e:
#        logging.error(f"Navigation failed: {e}")
#        return False

# def navigate_to_reports(driver):
#    try:
#        logging.info("Navigating to Reports section...")
       
#        # Click Reports using WebDriverWait
#        reports_button = WebDriverWait(driver, 10).until(
#            EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
#        )
#        reports_button.click()
#        logging.info("Successfully clicked Reports button")
#        return True
       
#    except Exception as e:
#        logging.error(f"Navigation to Reports failed: {e}")
#        return False

# def navigate_to_database_maintenance(driver):
#    try:
#        logging.info("Navigating to Reports section...")
       
#        # Click Reports using WebDriverWait
#        reports_button = WebDriverWait(driver, 10).until(
#            EC.element_to_be_clickable((By.ID, "asm-menu-reports"))
#        )
#        reports_button.click()
#        logging.info("Successfully clicked Reports button")
       
#        # Wait and click Database Maintenance
#        time.sleep(0.3)  # Small wait for animation
#        db_maintenance = WebDriverWait(driver, 10).until(
#            EC.element_to_be_clickable((By.ID, "ui-id-17"))
#        )
#        db_maintenance.click()
#        logging.info("Successfully clicked Database Maintenance")
#        return True
       
#    except Exception as e:
#        logging.error(f"Navigation to Database Maintenance failed: {e}")
#        return False
   
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

       if not navigate_to_database_maintenance(driver):
           raise Exception("Navigation failed")
           
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