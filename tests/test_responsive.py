import time
from selenium.webdriver.common.by import By

def step(message):
    print(f"STEP: {message}")


# Test : Vérification de l'affichage du menu en résolution desktop
def test_desktop_view(driver):
    step("Redimensionnement de la fenêtre pour desktop (1920x1080)")
    driver.set_window_size(1920, 1080)
    time.sleep(1)  # Pause pour observer le changement de taille

    step("Ouverture de la page d'accueil")
    driver.get("https://demowebshop.tricentis.com/")
    time.sleep(2)  # Pause pour observer le chargement

    step("Vérification de l'affichage du menu")
    assert driver.find_element(By.CSS_SELECTOR, ".top-menu").is_displayed()
    time.sleep(1)

# Test : Vérification de l'affichage du menu en résolution tablette
def test_tablet_view(driver):
    step("Redimensionnement de la fenêtre pour tablette (1366x768)")
    driver.set_window_size(1366, 768)
    time.sleep(1) 

    step("Ouverture de la page d'accueil")
    driver.get("https://demowebshop.tricentis.com/")
    time.sleep(2) 

    step("Vérification de l'affichage du menu")
    assert driver.find_element(By.CSS_SELECTOR, ".top-menu").is_displayed()
    time.sleep(1) 

# Test : Vérification de l'affichage du menu en résolution mobile
def test_mobile_view(driver):
    step("Redimensionnement de la fenêtre pour mobile (375x667)")
    driver.set_window_size(375, 667)
    time.sleep(1) 

    step("Ouverture de la page d'accueil")
    driver.get("https://demowebshop.tricentis.com/")
    time.sleep(2)  

    step("Vérification de l'affichage du menu")
    # On mobile, it might be the same menu or a different one depending on the site implementation.
    # For DemoWebShop, checking existence of top-menu or header-menu is a safe bet for existence.
    assert driver.find_element(By.CSS_SELECTOR, ".top-menu").is_displayed() or driver.find_element(By.CSS_SELECTOR, ".header-menu").is_displayed()
    time.sleep(1) 
