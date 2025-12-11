import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService



from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser: chrome, firefox, edge")


@pytest.fixture
def driver(request):
    # 1️⃣ Browser par défaut (chrome)
    browser = request.config.getoption("--browser")

    # 2️⃣ Si le test utilise @pytest.mark.parametrize("browser")
    if hasattr(request.node, "callspec"):
        if "browser" in request.node.callspec.params:
            browser = request.node.callspec.params["browser"]

    # 3️⃣ Création du driver selon le navigateur final
    if browser == "chrome":
        print(">>> Running on Chrome")
        driver = webdriver.Chrome(service=ChromeService())

    elif browser == "firefox":
        print(">>> Running on Firefox")
        driver = webdriver.Firefox(service=FirefoxService())

    elif browser == "edge":
        print(">>> Running on Edge")
        driver = webdriver.Edge(service=EdgeService())

    else:
        raise ValueError("Browser not supported")

    driver.maximize_window()
    yield driver
    driver.quit()
