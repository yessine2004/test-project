from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def explore():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        print(">>> Exploring Homepage")
        driver.get("https://demowebshop.tricentis.com/")
        print("Title:", driver.title)
        
        print(">>> Checking Search")
        try:
            driver.find_element(By.NAME, "q") # Common name for search
            print("FOUND: Search Box (name='q')")
        except:
            print("NOT FOUND: Search Box")

        print(">>> Checking Login")
        driver.get("https://demowebshop.tricentis.com/login")
        try:
            driver.find_element(By.ID, "Email")
            print("FOUND: Login Email (id='Email')")
            driver.find_element(By.ID, "Password")
            print("FOUND: Login Password (id='Password')")
        except:
            print("NOT FOUND: Login elements")

        print(">>> Checking Register")
        driver.get("https://demowebshop.tricentis.com/register")
        try:
            driver.find_element(By.ID, "FirstName")
            print("FOUND: Register FirstName")
        except:
            print("NOT FOUND: Register elements")

    finally:
        driver.quit()

if __name__ == "__main__":
    explore()
