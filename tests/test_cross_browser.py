import pytest
from selenium import webdriver

@pytest.fixture
def driver(request):
    browser = request.param  

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Browser {browser} not supported")

    driver.maximize_window()
    yield driver
    driver.quit()

# Paramétrisation pour plusieurs navigateurs
@pytest.mark.parametrize("driver", ["chrome", "firefox", "edge"], indirect=True)
def test_homepage_title(driver):
    driver.get("https://demowebshop.tricentis.com/")
    assert "Demo Web Shop" in driver.title
