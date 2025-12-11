import pytest
from selenium import webdriver

@pytest.fixture
def driver(request):
    browser = request.param  # récupère le navigateur depuis parametrize

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
    driver.get("https://tutorialsninja.com/demo/")
    assert "Your Store" in driver.title
