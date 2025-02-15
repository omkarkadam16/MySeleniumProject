# conftest.py - WebDriver Setup for LambdaTest
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

USERNAME = "omkarkadam058"
ACCESS_KEY = "PZJUAPczswU196TSMeRUYSMZy4hkyYmKSIShIHdaJoqkVEl5Pn"


@pytest.fixture(scope="class")
def driver():
    lt_options = {
        "build": "LambdaTest Selenium Playground Tests",
        "name": "Simple Form Demo Test",
        "platformName": "Windows 10",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "video": True,
        "console": "true",
        "network": True,
        "visual": True,
        "w3c": True,
        "plugin": "python-pytest",
    }

    options = Options()
    options.set_capability("LT:Options", lt_options)

    remote_url = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"
    driver = webdriver.Remote(command_executor=remote_url, options=options)

    yield driver
    driver.quit()


# test_simple_form_demo.py - Test Scenario 1
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("driver")
class TestSimpleFormDemo:
    def test_simple_form_demo(self, driver):
        driver.get("https://www.lambdatest.com/selenium-playground")
        driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
        assert "simple-form-demo" in driver.current_url

        message = "Welcome to LambdaTest"
        input_box = driver.find_element(By.ID, "user-message")
        input_box.send_keys(message)
        driver.find_element(By.CSS_SELECTOR, "#showInput").click()
        displayed_message = driver.find_element(By.ID, "message").text
        assert (
            displayed_message == message
        ), f"Expected '{message}', but got '{displayed_message}'"
