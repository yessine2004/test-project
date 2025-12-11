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
    driver.get("https://tutorialsninja.com/demo/")
    time.sleep(2)  # Pause pour observer le chargement

    step("Vérification de l'affichage du menu")
    assert driver.find_element(By.ID, "menu").is_displayed()
    time.sleep(1)

# Test : Vérification de l'affichage du menu en résolution tablette
def test_tablet_view(driver):
    step("Redimensionnement de la fenêtre pour tablette (1366x768)")
    driver.set_window_size(1366, 768)
    time.sleep(1) 

    step("Ouverture de la page d'accueil")
    driver.get("https://tutorialsninja.com/demo/")
    time.sleep(2) 

    step("Vérification de l'affichage du menu")
    assert driver.find_element(By.ID, "menu").is_displayed()
    time.sleep(1) 

# Test : Vérification de l'affichage du menu en résolution mobile
def test_mobile_view(driver):
    step("Redimensionnement de la fenêtre pour mobile (375x667)")
    driver.set_window_size(375, 667)
    time.sleep(1) 

    step("Ouverture de la page d'accueil")
    driver.get("https://tutorialsninja.com/demo/")
    time.sleep(2)  

    step("Vérification de l'affichage du menu")
    assert driver.find_element(By.ID, "menu").is_displayed()
    time.sleep(1) 
