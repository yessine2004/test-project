from selenium.webdriver.common.by import By

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def remove_all_items(self):
        remove_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-danger")
        for btn in remove_buttons:
            btn.click()
