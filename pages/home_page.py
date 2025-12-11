from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.NAME, "search")
        self.menu = (By.ID, "menu")

    def open(self, url):
        self.driver.get(url)

    def search_product(self, product_name):
        self.driver.find_element(*self.search_box).send_keys(product_name)
        self.driver.find_element(*self.search_box).submit()
