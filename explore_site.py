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
        driver.get("https://automationexercise.com/")
        print("Title:", driver.title)
        
        # Check for search button? Actually search is usually on /products
        print(">>> Navigating to Products")
        driver.get("https://automationexercise.com/products")
        try:
            search_box = driver.find_element(By.ID, "search_product")
            print("FOUND: Search Box (ID: search_product)")
            search_btn = driver.find_element(By.ID, "submit_search")
            print("FOUND: Search Button (ID: submit_search)")
        except:
            print("NOT FOUND: Search elements")

        print(">>> Navigating to Login")
        driver.get("https://automationexercise.com/login")
        try:
            # Login form
            email = driver.find_element(By.CSS_SELECTOR, ".login-form input[name='email']")
            print("FOUND: Login Email")
            password = driver.find_element(By.CSS_SELECTOR, ".login-form input[name='password']")
            print("FOUND: Login Password")
            
            # Signup form
            signup_name = driver.find_element(By.CSS_SELECTOR, ".signup-form input[name='name']")
            print("FOUND: Signup Name")
            signup_email = driver.find_element(By.CSS_SELECTOR, ".signup-form input[name='email']")
            print("FOUND: Signup Email")
        except Exception as e:
            print("Error finding login elements:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    explore()
