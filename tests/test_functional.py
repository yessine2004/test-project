import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

BASE_URL = "https://tutorialsninja.com/demo/"


# Petite fonction pour afficher les étapes
def step(message):
    print(f"\n------------------------------\n➡️  {message}\n------------------------------")
    time.sleep(2)


# -------------------
# Cas positifs
# -------------------

import time
# Test : Vérification du titre de la page d'accueil
def test_homepage_title(driver):
    step("Ouverture de la page d'accueil")
    driver.get(BASE_URL)
    time.sleep(3)  

    step("Validation du titre")
    assert "Your Store" in driver.title
    time.sleep(2) 

# Test : Recherche d'un produit sur la page d'accueil
def test_search_product(driver):
    step("Recherche d'un produit : iphone")
    driver.get(BASE_URL)

    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys("iphone")
    search_box.send_keys(Keys.ENTER) 

    step("Vérification de l'affichage du résultat")

    wait = WebDriverWait(driver, 10)
    products = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
    )
    assert len(products) > 0
    step(f"Résultat vérifié : {len(products)} produits trouvés.")

# Test : Ajout d'un produit au panier
WAIT_TIME = 10 
def test_add_to_cart(driver):
    step("Ouverture du produit iphone")
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)
    iphone_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "iphone"))
    )
    iphone_link.click()
    step("Ajout au panier")
    add_to_cart_button = wait.until(
        EC.element_to_be_clickable((By.ID, "button-cart"))
    )
    add_to_cart_button.click()
    step("Vérification du message de succès")

    success_msg = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))
    if "added to your shopping cart" in success_msg.text:
        print("PASSED: Produit ajouté avec succès")
    else:
        raise AssertionError(f"FAILED: Message reçu : {success_msg.text}")
    
# Test : Suppression d'un produit du panier
def test_remove_from_cart(driver):
    step("Ouverture du panier")
    driver.get(BASE_URL + "index.php?route=checkout/cart")
    time.sleep(2)  

    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
    if cart_items:
        step("Suppression d'un article du panier")
        driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()
        time.sleep(2) 

    step("Vérification que le panier est vide")
    assert len(driver.find_elements(By.CSS_SELECTOR, ".cart-item")) == 0
    time.sleep(2) 

# Test : Création d'un compte utilisateur avec des données valides
def test_create_account_valid(driver):
    step("Ouverture de la page inscription")
    driver.get(BASE_URL + "index.php?route=account/register")

    step("Remplissage du formulaire valide")
    driver.find_element(By.ID, "input-firstname").send_keys("Yessine")
    driver.find_element(By.ID, "input-lastname").send_keys("Allani")
    driver.find_element(By.ID, "input-email").send_keys("yessineallanni@gmail.com")
    driver.find_element(By.ID, "input-telephone").send_keys("58357168")  
    driver.find_element(By.ID, "input-password").send_keys("Password123")
    driver.find_element(By.ID, "input-confirm").send_keys("Password123")   

    agree_checkbox = driver.find_element(By.NAME, "agree")
    if not agree_checkbox.is_selected():
        agree_checkbox.click()

    step("Soumission du formulaire")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    step("Vérification de la création du compte")
    wait = WebDriverWait(driver, 10)
    success_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Your Account Has Been Created!')]")))
    assert "Your Account Has Been Created!" in success_msg.text

# Test : Connexion avec des identifiants valides
def test_login_valid(driver):
    step("Ouverture page login")
    driver.get(BASE_URL + "index.php?route=account/login")
    time.sleep(2)  

    step("Connexion avec identifiants valides")
    driver.find_element(By.ID, "input-email").send_keys("yessineallanni@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("Password123")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(2)  

    step("Vérification du titre")
    assert "My Account" in driver.title
    time.sleep(2)  

# Test : Filtrage des produits par catégorie
def test_filter_category(driver):
    step("Ouverture des catégories Desktops")
    driver.get(BASE_URL)
    
    wait = WebDriverWait(driver, WAIT_TIME)
    desktop_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Desktops"))
    )
    desktop_link.click()
    step("Vérification de la navigation (titre)")
    wait.until(
        EC.title_contains("Desktops")
    )
    assert "Desktops" in driver.title

# Test : Vérification du tri par prix dans la catégorie Desktops
def test_sort_price(driver):
    step("Ouverture Desktops")
    driver.get(BASE_URL)
    
    wait = WebDriverWait(driver, WAIT_TIME)
    step("Clic sur la catégorie Desktops")
    try:
        desktop_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Desktops"))
        )
        desktop_link.click()
    except TimeoutException:
        raise AssertionError("Échec : Le lien 'Desktops' n'a pas pu être trouvé ou cliqué.")

    step("Attente de la page Desktops et du menu de tri")
    try:
        wait.until(
            EC.title_contains("Desktops")
        )
    except TimeoutException:
        raise AssertionError("Échec : Le titre de la page n'a pas changé après le clic.")
    step("Vérification du menu de tri")
    select = wait.until(
        EC.presence_of_element_located((By.ID, "input-sort"))
    )

    options = [o.text for o in select.find_elements(By.TAG_NAME, "option")]
    assert "Price (Low > High)" in options

# Test : Accès à la page "Contact Us"
def test_contact_page(driver):
    step("Ouverture page Contact")
    driver.get(BASE_URL)
    time.sleep(2)  

    driver.find_element(By.LINK_TEXT, "Contact Us").click()
    time.sleep(2) 

    assert "Contact Us" in driver.title
    time.sleep(2)  


# Test : Passage à la caisse sans être connecté
def test_checkout_without_login(driver):
    step("Ouverture panier puis checkout")
    driver.get(BASE_URL + "index.php?route=checkout/cart")
    time.sleep(2) 

    driver.find_element(By.LINK_TEXT, "Checkout").click()
    time.sleep(2)  

    step("Vérification redirection login")
    assert "Account Login" in driver.title
    time.sleep(2) 

# -------------------
# Cas négatifs
# -------------------
# Test négatif : Recherche d'un produit inexistant
def test_search_invalid_product(driver):
    step("Recherche d'un produit inexistant")
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)
    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "search"))
    )
    search_box.send_keys("ProduitInexistant")
    search_box.send_keys(Keys.ENTER) 

    step("Vérification du message d'erreur")
    
    no_results = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#content p"))
    )
    expected_text = "There is no product that matches the search criteria"
    assert expected_text in no_results.text, f"Le message attendu '{expected_text}' n'a pas été trouvé. Réel : {no_results.text}"

# Test négatif : Connexion avec un mot de passe invalide

def test_login_invalid_password(driver):
    step("Tentative de login avec mauvais mot de passe")
    driver.get(BASE_URL + "index.php?route=account/login")
    wait = WebDriverWait(driver, WAIT_TIME)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "input-email")))
    email_field.send_keys("yessineallani2@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("WrongPass")
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_button.click()
    step("Vérification du message d'erreur")
    error_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
    )
    expected_partial_text = "No match for E-Mail Address and/or Password" 
    assert expected_partial_text in error_element.text
    step(f"Message d'erreur vérifié : {error_element.text}")

# Test négatif : Création d'un compte avec un email déjà existant
def test_create_account_existing_email(driver):
    step("Création compte avec email déjà existant")
    driver.get(BASE_URL + "index.php?route=account/register")
    wait = WebDriverWait(driver, WAIT_TIME)
    driver.find_element(By.ID, "input-firstname").send_keys("Test")
    driver.find_element(By.ID, "input-lastname").send_keys("User")
    driver.find_element(By.ID, "input-email").send_keys("yessineallanii@gmail.com") # Email déjà enregistré
    driver.find_element(By.ID, "input-telephone").send_keys("58357168")
    driver.find_element(By.ID, "input-password").send_keys("Password123")
    driver.find_element(By.ID, "input-confirm").send_keys("Password123")
    
    step("Cocher la case Politique de Confidentialité")
    driver.find_element(By.NAME, "agree").click() 

    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    error = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
    )
    
    expected_error_text = "Warning: E-Mail Address is already registered!"
    assert expected_error_text in error.text
    step(f"Message d'erreur vérifié : {error.text}")

# Test négatif : Création d'un compte avec un prénom et un nom trop longs
def test_create_account_long_name(driver):
    step("Inscription avec nom/prénom trop long")
    driver.get(BASE_URL + "index.php?route=account/register")
    time.sleep(2)  

    driver.find_element(By.ID, "input-firstname").send_keys("A"*51)
    driver.find_element(By.ID, "input-lastname").send_keys("B"*51)
    driver.find_element(By.ID, "input-email").send_keys("yessineallani3@gmail.com")
    driver.find_element(By.ID, "input-telephone").send_keys("58357168")  
    driver.find_element(By.ID, "input-password").send_keys("Password123")
    driver.find_element(By.ID, "input-confirm").send_keys("Password123")  
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(2)  

    error = driver.find_element(By.CSS_SELECTOR, ".text-danger")
    assert error.is_displayed()
    time.sleep(2)


# Test négatif : Soumission d'un formulaire vide
def test_submit_empty_form(driver):
    step("Soumission d'un formulaire vide")
    driver.get(BASE_URL + "index.php?route=account/register")
    time.sleep(2)  

    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(2)  

    errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
    assert len(errors) > 0
    time.sleep(2)


# Test négatif : Tentative de SQL Injection dans la barre de recherche
def test_sql_injection_search(driver):
    step("Tentative SQL Injection dans la recherche")
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)
    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "search"))
    )

    search_box.send_keys("' OR 1=1 --")
    search_box.send_keys(Keys.ENTER) 
    
    step("Vérification de la résilience à l'injection")
    wait.until(
        EC.title_contains("Search") 
    )

    expected_safe_message = "There is no product that matches the search criteria"
    assert expected_safe_message in driver.page_source
    step(f"Vérifié : Le message d'absence de produit indique que l'injection a été bloquée.")

# Test négatif : Accès à une page privée sans être connecté
def test_access_private_page_without_login(driver):
    step("Accès à une page privée sans login")
    driver.get(BASE_URL + "index.php?route=account/edit")
    time.sleep(2) 

    assert "Account Login" in driver.title
    time.sleep(1) 
