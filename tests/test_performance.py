import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://demowebshop.tricentis.com/"

# -------------------------------------------------------
# Fonctions utilitaires
# -------------------------------------------------------
def step(message):
    print(f"\n===== STEP: {message} =====")
    time.sleep(1)

def slow(seconds=2):
    """Ralentit l'exécution pour suivre visuellement les tests."""
    time.sleep(seconds)


# =======================================================
# 🔵 TEST TC12 — Performance Homepage Load
# =======================================================
def test_performance_homepage_load(driver):
    """
    TC12 – Performance Test: Homepage Loading Time
    Objectif :
        Mesurer le temps de chargement de la page d’accueil.
    Résultat attendu :
        Le site doit se charger en moins de 5 secondes.
    """
    step("Opening Homepage")
    start_time = time.time()
    driver.get(BASE_URL)

    step("Waiting for Search Box to be visible")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-box-button"))
    )
    end_time = time.time()

    load_time = end_time - start_time
    print(f"Homepage Load Time: {load_time:.2f}s")

    assert load_time < 5.0, f"⚠️ Performance issue: load time = {load_time:.2f}s"
    slow(2)


# =======================================================
# 🔵 TEST TC13 — Performance Search Time
# =======================================================
def test_performance_search(driver):
    """
    TC13 – Performance Test: Product Search Response Time
    Objectif :
        Mesurer le temps de réponse lors d’une recherche produit.
    Résultat attendu :
        Résultats affichés en moins de 4 secondes.
    """
    step("Opening Homepage")
    driver.get(BASE_URL)
    slow(1)

    step("Typing product name 'computer'")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("computer")

    step("Measuring Search Response")
    start_time = time.time()
    driver.find_element(By.CSS_SELECTOR, ".search-box-button").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item"))
    )
    end_time = time.time()

    response_time = end_time - start_time
    print(f"Search Response Time: {response_time:.2f}s")

    assert response_time < 4.0, "⚠️ Search too slow!"
    slow(2)


# =======================================================
# 🔵 TEST — Stress Test Navigation
# =======================================================
def test_stress_load_multiple_pages(driver):
    """
    TC14 – Stress Test: Navigation lourde
    Objectif :
        Charger plusieurs pages rapidement pour simuler une charge.
    Résultat attendu :
        Aucune erreur de chargement.
    """
    step("Navigating through multiple pages")

    urls = [
        BASE_URL,
        BASE_URL + "computers",
        BASE_URL + "login",
    ]

    for url in urls:
        step(f"Loading: {url}")
        driver.get(url)
        slow(2)


# =======================================================
# 🔵 TEST — Stress Add To Cart Repeatedly
# =======================================================
@pytest.mark.stress
def test_stress_add_to_cart(driver):
    """
    TC15 – Stress Test: Add to Cart Repeatedly
    Objectif :
        Simuler une charge en ajoutant plusieurs fois le même produit.
    Résultat attendu :
        Le panier doit accepter les clics répétés (≥ 5 items).
    """
    step("Opening product page")
    driver.get(BASE_URL + "141-inch-laptop")
    slow(1)

    add_btn = driver.find_element(By.CSS_SELECTOR, ".add-to-cart-button")

    step("Stress test: clicking Add to Cart rapidly")
    for i in range(5):
        add_btn.click()
        slow(0.5)
        try:
            WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.ID, "bar-notification"))
            )
        except:
            pass

    step("Validating cart quantity")
    qty_text = driver.find_element(By.CSS_SELECTOR, ".cart-qty").text

    import re
    qty = int(re.search(r'\d+', qty_text).group())

    assert qty >= 5, "Cart did not register repeated additions"
    slow(2)
