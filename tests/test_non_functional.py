import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://demowebshop.tricentis.com/"

# ==========================================
# 1. Performance Testing (Response Time)
# ==========================================

def test_performance_homepage_load(driver):
    start_time = time.time()
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-box-button")))
    end_time = time.time()
    
    load_time = end_time - start_time
    print(f"Homepage Load Time: {load_time:.2f}s")
    
    # Assert load time is acceptable (e.g., < 3 seconds)
    assert load_time < 5.0, f"Performance degrades: {load_time}s > 5s"

def test_performance_search(driver):
    driver.get(BASE_URL)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("computer")
    
    start_time = time.time()
    driver.find_element(By.CSS_SELECTOR, ".search-box-button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item")))
    end_time = time.time()
    
    response_time = end_time - start_time
    print(f"Search Response Time: {response_time:.2f}s")
    assert response_time < 4.0

# ==========================================
# 2. Stress Testing
# ==========================================

@pytest.mark.stress
def test_stress_add_to_cart(driver):
    """
    Stress test: Add to cart 5 times in rapid succession.
    Real stress testing usually requires tools like JMeter, but we simulate user fatigue here.
    """
    driver.get(BASE_URL + "141-inch-laptop")
    
    add_btn = driver.find_element(By.CSS_SELECTOR, ".add-to-cart-button")
    
    for i in range(5):
        add_btn.click()
        # Wait for "Adding..." overlay or logic to clear might be needed, 
        # but for stress we hit it fast.
        # However, Webdriver might be too fast, so we wait for the bar to appear/disappear or just notification.
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "bar-notification")))
            # Optional: wait for it to disappear to click again clean, but stress means pushing it.
            # Using a small sleep to emulate fast user clicking
            time.sleep(0.5) 
        except:
            pass
    
    # Verification: Cart quantity should be at least 5 (or logic handled correctly)
    qty_val = driver.find_element(By.CSS_SELECTOR, ".cart-qty").text
    # Extract number from "(5)"
    import re
    qty = int(re.search(r'\d+', qty_val).group())
    assert qty >= 5

# ==========================================
# 3. Responsive Testing (Mobile/Desktop)
# ==========================================

@pytest.mark.parametrize("width, height, view_mode", [
    (1920, 1080, "Desktop"),
    (414, 896, "Mobile")
])
def test_responsive_elements(driver, width, height, view_mode):
    driver.set_window_size(width, height)
    driver.get(BASE_URL)
    time.sleep(1) # Wait for layout
    
    if view_mode == "Mobile":
        # Check if Side Category Menu is hidden or moved (Common in old responsive sites)
        # In DemoWebShop, left column might stack or disappear.
        # Let's check if the Search box is still visible and usable
        search = driver.find_element(By.NAME, "q")
        assert search.is_displayed()
        
        # Check specific mobile behavior if known. 
        # For this demo, we ensure main content is visible.
        main_col = driver.find_element(By.CSS_SELECTOR, ".master-wrapper-main")
        assert main_col.is_displayed()

    else:
        # Desktop specific check
        cat_nav = driver.find_element(By.CSS_SELECTOR, ".block-category-navigation")
        assert cat_nav.is_displayed()
