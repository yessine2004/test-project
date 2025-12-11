import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://demowebshop.tricentis.com/"

# -------------------
# Utility Function
# -------------------

def slow(seconds=1):
    """Slow down test execution for readability/observation."""
    time.sleep(seconds)

def step(message):
    """Print step title for clearer logs."""
    print(f"\n------------------------------\n➡️  {message}\n------------------------------")
    slow(0.5)

# -------------------
# Positive Test Cases
# -------------------

def test_homepage_title(driver):
    """
    TC01 - Homepage Title
    Objectif :
        Vérifier que la page d'accueil du site s'ouvre correctement et que
        le titre contient 'Demo Web Shop'.
    """
    step("Open Homepage")
    driver.get(BASE_URL)
    slow(2)

    step("Validate Title Contains 'Demo Web Shop'")
    assert "Demo Web Shop" in driver.title
    slow(2)


def test_search_product(driver):
    """
    TC02 - Search Valid Product
    Objectif :
        Vérifier que la recherche d'un produit existant retourne des résultats.
    """
    step("Search for Product: computer")
    driver.get(BASE_URL)
    slow(2)

    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys("computer")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'].search-box-button").click()
    slow(2)

    step("Verify Search Results")
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item")))
    assert len(products) > 0
    step(f"Verified: {len(products)} products found.")
    slow(2)


def test_add_to_cart(driver):
    """
    TC03 - Add Product to Cart
    Objectif :
        Vérifier qu’un produit peut être ajouté au panier et qu’un message
        de confirmation apparaît.
    """
    step("Open Product Page")
    driver.get(BASE_URL + "141-inch-laptop")
    slow(2)

    wait = WebDriverWait(driver, 10)

    step("Click Add to Cart")
    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button")))
    add_btn.click()
    slow(2)

    step("Verify Success Message")
    success_bar = wait.until(EC.visibility_of_element_located((By.ID, "bar-notification")))
    assert "added to your shopping cart" in success_bar.text
    slow(2)


def test_register_flow(driver):
    """
    TC05 - Registration Flow
    Objectif :
        Vérifier qu’un nouvel utilisateur peut s’enregistrer avec succès.
    """
    step("Navigate to Register Page")
    driver.get(BASE_URL + "register")
    slow(2)

    driver.find_element(By.ID, "gender-male").click()
    driver.find_element(By.ID, "FirstName").send_keys("yessine")
    driver.find_element(By.ID, "LastName").send_keys("allani")
    slow(1)

    
    email = f"yessineallanii@gmail.com"

    step("Fill Registration Fields")
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys("pass123456")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("pass123456")
    driver.find_element(By.ID, "register-button").click()

    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".result")))
    assert "Your registration completed" in result.text
    slow(2)

def test_login_valid(driver):
    """
    TC04 - Login Valid Credentials
    Objectif :
        Vérifier que l’utilisateur peut se connecter avec email/mot de passe valides.
    """
    step("Navigate to Login")
    driver.get(BASE_URL + "login")
    slow(2)

    step("Enter Credentials")
    driver.find_element(By.ID, "Email").send_keys("yessineallani@gmail.com")
    driver.find_element(By.ID, "Password").send_keys("passw123456")
    driver.find_element(By.CSS_SELECTOR, "input.login-button").click()
    slow(2)

    step("Login Attempt Done")


def test_checkout_anonymous(driver):
    """
    TC06 - Checkout as Anonymous User
    Objectif :
        Vérifier qu’un utilisateur non connecté est redirigé vers une page
        de login lors du checkout.
    """
    step("Add Product to Cart")
    driver.get(BASE_URL + "141-inch-laptop")
    driver.find_element(By.CSS_SELECTOR, ".add-to-cart-button").click()
    slow(2)

    step("Go to Cart")
    driver.get(BASE_URL + "cart")
    driver.find_element(By.ID, "termsofservice").click()
    driver.find_element(By.ID, "checkout").click()
    slow(2)

    step("Verify Redirect")
    assert "login" in driver.current_url or "checkout" in driver.current_url
    slow(2)

# -------------------
# Negative Test Cases
# -------------------

def test_search_no_results(driver):
    """
    TC07 - Search Nonexistent Product
    Objectif :
        Vérifier que la recherche d’un produit invalide affiche un message
        'No products were found'.
    """
    step("Search Invalid Product")
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "q").send_keys("NonExistentProductXYZ123")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'].search-box-button").click()
    slow(2)

    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results")))
    assert "No products were found" in result.text
    slow(2)


def test_login_invalid(driver):
    """
    TC08 - Invalid Login
    Objectif :
        Vérifier qu’un message d’erreur s’affiche lorsque l’utilisateur
        entre des informations incorrectes.
    """
    step("Attempt Login with Wrong Credentials")
    driver.get(BASE_URL + "login")
    slow(2)

    driver.find_element(By.ID, "Email").send_keys("yessineallani@gmail.com")
    driver.find_element(By.ID, "Password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "input.login-button").click()
    slow(2)

    wait = WebDriverWait(driver, 10)
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".validation-summary-errors")))
    assert "Login was unsuccessful" in error.text
    slow(2)
