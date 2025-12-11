from selenium.webdriver.common.by import By

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_btn = (By.ID, "button-cart")
        self.success_alert = (By.CSS_SELECTOR, ".alert-success")

    def add_to_cart(self):
        self.driver.find_element(*self.add_to_cart_btn).click()

    def get_success_message(self):
        return self.driver.find_element(*self.success_alert).text
