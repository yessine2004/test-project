import time
def step(message):
    print(f"STEP: {message}")


# Test de performance : Temps de chargement de la page d'accueil
def test_homepage_load_time(driver):
    step("Mesure du temps de chargement de la page d'accueil")
    start = time.time()
    driver.get("https://demowebshop.tricentis.com/")
    load_time = time.time() - start
    print(f"Homepage load time: {load_time:.2f}s")
    assert load_time < 5
    time.sleep(2)

# Test de charge/stress : Navigation sur plusieurs pages

def test_stress_load_multiple_pages(driver):
    step("Navigation sur plusieurs pages du site")
    urls = [
        "https://demowebshop.tricentis.com/",
        "https://demowebshop.tricentis.com/computers",
        "https://demowebshop.tricentis.com/login",
    ]
    for url in urls:
        driver.get(url)
        time.sleep(5) 
