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

        # Keep the browser open
        input("Press Enter to close the browser and end the script...")

    finally:
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    main()







##pseudocode
# Step through website login
# Name -> Password
# Enter

## AND THEN ##

# Click on Reports
# Click on Database Maintanence
# Click on Jpegs Unnamed
# Start on the bottom....(CAN WE DIFFERATE BETWEEN TOP MIDDLE AND BOTTOM? AKA IDENTIFIERS)

#EXAMPLE html markup
# <a href="person_media?id=15078"> Cristalyn Valdez-Montoya &amp;  Ricardo Valdez- Montoya</a>
##   ##


# Features to have
# Confirm each step through?
# Confirm each change to ID? ie shows me the picture?
# Maybe with different choices -> "ID" , "Proof", "Citation", "Investigation", "christmas-picture"


# Needs to idenitify between JPG and PDF


# Delete duplicate IDs if need? 
# How do i implement that


# Questions -> 
# 1) It seems like Changing to ID triggers an event to remove
# person from list
# How does it remove them and what causes it not to?
# ie the 5-6 people at top of list


# 2) At top of list: 
# Jpegs should have names like "ID", "Proof", "Citation"
# Is this something that needs to be included in program?

# Code in JPEG'S report

# select o.id, '<b><a href="person_media?id=' || o.ID::varchar || '">' || o.OwnerName || '</a><br />' ||
# o.OwnerAddress
# from owner o
# join media m on m.LinkID=o.ID and m.LinkTypeID=3 and m.MediaMimeType like '%jpeg%' and m.MediaNotes not like '%ID%'
# and m.MediaNotes not like '%id.%' and m.MediaNotes not like '%Proof%' 
# and m.medianotes not like '%Citation%' and m.MediaNotes not like '%Investigation%' and m.MediaNotes not like '%christmas-picture%'
# and m.MediaSize>0
# and o.id not in (46216,46216)
# group by o.ID
# order by Max(m.CreatedDate)
# limit 200




#If Rabies cert-> make it into PDF file and label it animalName-rabies-year
#If App jpeg already have App pdf, delete the jpeg

