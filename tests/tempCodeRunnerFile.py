def test_search_product(driver):
    step("Recherche d'un produit : MacBook")
    driver.get(BASE_URL)

    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys("MacBook")
    search_box.submit()

    step("Vérification de l'affichage du résultat")
    wait = WebDriverWait(driver, 10)
    products = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
    )
    assert len(products) > 0