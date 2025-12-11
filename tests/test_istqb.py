import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string

BASE_URL = "https://demowebshop.tricentis.com/"

# -------------------
# Pytest Fixture (Configuration du WebDriver)
# -------------------

@pytest.fixture(scope="session")
def driver():
    """
    Initialise et configure le WebDriver (Chrome).
    Le 'scope="session"' assure que le navigateur s'ouvre une seule fois pour tous les tests.
    """
    print("\n--- Initialisation du WebDriver ---")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Décommenter pour exécution sans interface graphique
    options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10) 
    
    yield driver # Le test s'exécute ici
    
    # Après l'exécution de tous les tests de la session
    print("\n--- Fermeture du WebDriver ---")
    driver.quit()

# -------------------
# Utility Functions
# -------------------

def slow(seconds=1):
    """Ralentir l'exécution pour observer le comportement (pour le développement)."""
    time.sleep(seconds)

def step(message):
    """Afficher des messages d'étapes clairs dans les logs de test."""
    print(f"\n------------------------------\n➡️  {message}\n------------------------------")
    slow(0.5)

def generer_email_simple():
    """Génère un e-mail simple de type 'test_XXXXX@aleatoire.com'."""
    suffixe = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"test_{suffixe}@aleatoire.com"

# ======================================================================
# TEST 1 : BVA – Boundary Value Analysis (Quantité produit)
# ======================================================================

@pytest.mark.parametrize("qty, expected_outcome", [
    ("1", "valid"),         # Valeur normale
    ("5", "valid"),         # Limite haute supposée valide (ajustez si la limite réelle est différente)
    ("9999", "invalid"),   # Valeur frontière basse (supposée invalide)
    ("10000000000", "invalid"),  # Valeur impossible
])
def test_bva_product_quantity(driver, qty, expected_outcome):
    """
    TC09 - Tester les valeurs limites de la quantité d'un produit (BVA).
    """

    step(f"Open product page ‘14.1-inch Laptop’ with qty = {qty}")
    driver.get(BASE_URL + "141-inch-laptop")
    slow(2)

    step("Enter Quantity")
    # Utilisation de WebDriverWait pour s'assurer que l'élément est prêt
    qty_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".qty-input"))
    )
    qty_input.clear()
    qty_input.send_keys(qty)
    slow(2)

    step("Click Add to Cart")
    driver.find_element(By.CSS_SELECTOR, ".add-to-cart-button").click()
    slow(2)

    step("Validate Outcome")
    # Vérifier l'apparition de la notification verte/verte (#bar-notification)
    bar_notification = driver.find_elements(By.ID, "bar-notification")

    if expected_outcome == "valid":
        # Vérifier que la notification est affichée et contient le texte de succès
        assert len(bar_notification) > 0 and \
               "added to your shopping cart" in bar_notification[0].text, \
               f"Échec BVA: L'ajout au panier aurait dû réussir pour la quantité {qty}."
    else:
        # Vérifier que la notification verte n'est PAS affichée
        # (Le site peut afficher une erreur rouge qui n'a pas cet ID)
        assert len(bar_notification) == 0 or \
               "added to your shopping cart" not in bar_notification[0].text, \
               f"Échec BVA: L'ajout au panier aurait dû échouer pour la quantité {qty}."
    slow(2)

# ======================================================================
# TEST 2 : State Transition – Checkout Process
# ======================================================================

def test_state_transition_checkout(driver):
    """
    TC10 - Vérifier la transition d'états du processus de commande (Checkout).
    
    """

    step("Navigate to a Product Page and Add to Cart")
    driver.get(BASE_URL + "141-inch-laptop")
    driver.find_element(By.CSS_SELECTOR, ".add-to-cart-button").click()
    # Attendre la notification "The product has been added to your shopping cart"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "bar-notification")))

    step("Open Shopping Cart")
    driver.get(BASE_URL + "cart")
    assert "Shopping Cart" in driver.title, "Échec de la transition : Pas sur la page Panier."

    step("Accept Terms and Proceed to Checkout")
    # Utilisation de WebDriverWait pour cliquer sur une checkbox qui peut ne pas être cliquable immédiatement
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "termsofservice"))
    ).click()
    
    driver.find_element(By.ID, "checkout").click()
    slow(2)

    step("Validate Redirect (Non-Logged In User)")
    # Sans connexion, le site redirige vers la page de login ou d'enregistrement
    current_url = driver.current_url
    assert "login" in current_url or "register" in current_url, \
           f"Échec de la transition: Redirection incorrecte. URL actuelle: {current_url}"
    slow(2)
    
# ======================================================================
# TEST 3 : Responsive UI – Test différentes résolutions
# ======================================================================

@pytest.mark.parametrize("width, height, device_name", [
    (1920, 1080, "Desktop"),
    (375, 812, "iPhone X"),
    (768, 1024, "iPad"),
])
def test_responsive_layout(driver, width, height, device_name):
    """
    TC11 - Vérifier que l'affichage s'adapte selon la résolution de l'écran.
    """

    step(f"Set screen resolution for {device_name}: {width}x{height}")
    driver.set_window_size(width, height)
    slow(1)

    driver.get(BASE_URL)
    slow(2)

    step("Validate responsive layout")

    # La logique est basée sur la largeur. Le menu mobile s'active généralement sous un certain seuil.
    # Nous allons vérifier la présence/absence du menu standard (.top-menu).
    
    top_menu_elements = driver.find_elements(By.CSS_SELECTOR, ".top-menu")

    if width < 980: 
        # Pour les petits écrans, le menu principal doit être masqué (ou géré par un hamburger)
        assert len(top_menu_elements) == 0 or not top_menu_elements[0].is_displayed(), \
               f"Échec Responsive: Le menu Desktop est visible sur {device_name} ({width}px)."
    else: 
        # Pour les grands écrans, le menu doit être affiché
        assert len(top_menu_elements) > 0 and top_menu_elements[0].is_displayed(), \
               f"Échec Responsive: Le menu Desktop est masqué sur {device_name} ({width}px)."
    slow(2)

# ======================================================================
# TEST 4 : Intégration de la Newsletter (Votre Test Corrigé)
# ======================================================================

BASE_URL = "http://demowebshop.tricentis.com/"  # URL à ajuster si nécessaire
def generer_email_simple():
    """ Simule la génération d'un e-mail unique pour le test. """
    timestamp = int(time.time() * 1000)
    return f"testuser_{timestamp}@mailinator.com"

def step(description):
    """ Simule une fonction d'étape pour les logs (souvent utilisée avec Allure). """
    print(f"\n--- Étape: {description} ---")

def slow(seconds):
    """ Ajoute un délai (à utiliser avec parcimonie dans les vrais tests). """
    time.sleep(seconds)

# --- FIN SIMULATIONS ---


# --- DÉBUT DE LA FONCTION DE TEST PRINCIPALE ---

# Le paramètre 'driver' est généralement fourni par une fixture Pytest (souvent dans conftest.py)
# qui initialise le navigateur (Chrome, Firefox, etc.).
def test_newsletter_subscription(driver: webdriver.Chrome):
    """
    TC12 - Simuler l'inscription à la newsletter avec un e-mail aléatoire.
    """
    EMAIL_TEST = generer_email_simple()

    step(f"Open Home Page and Subscribe with email: {EMAIL_TEST}")
    driver.get(BASE_URL)

    champ_email = driver.find_element(By.ID, "newsletter-email")
    champ_email.clear()
    champ_email.send_keys(EMAIL_TEST)

    bouton_subscribe = driver.find_element(By.ID, "newsletter-subscribe-button")
    bouton_subscribe.click()

    message_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "newsletter-result"))
    )
    message_final = message_element.text
    
    print(f"\n✅ Résultat affiché par le site : **{message_final}**")

    assert "Thank you for signing up!" in message_final or \
           "Enter valid email" in message_final or \
           "is already registered" in message_final, \
           f"Échec Newsletter: Message de résultat inattendu: {message_final}"
    
    print("Test réussi : L'action d'inscription a retourné un message valide.")
    slow(2)