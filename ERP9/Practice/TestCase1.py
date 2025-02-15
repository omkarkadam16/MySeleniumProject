import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = "omkarkadam058"
ACCESS_KEY = "PZJUAPczswU196TSMeRUYSMZy4hkyYmKSIShIHdaJoqkVEl5Pn"

capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "platformName": "Windows 10",
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "platformName": "macOS Catalina",
    },
]


@pytest.fixture(params=capabilities, scope="class")
def driver(request):
    lt_options = {
        "build": "LambdaTest Selenium Playground Tests",
        "name": "Test Execution Omkar",
        "video": True,
        "console": "true",
        "network": True,
    }
    options = (
        webdriver.ChromeOptions()
        if request.param["browserName"] == "Chrome"
        else webdriver.SafariOptions()
    )
    options.set_capability("LT:Options", lt_options)

    remote_url = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"
    driver = webdriver.Remote(command_executor=remote_url, options=options)

    yield driver
    driver.quit()


# Test Case 1: Simple Form Demo
def test_simple_form_demo(driver):
    driver.get("https://www.lambdatest.com/selenium-playground")
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
    assert "simple-form-demo" in driver.current_url

    message = "Welcome to LambdaTest"
    input_box = driver.find_element(By.ID, "user-message")
    input_box.send_keys(message)
    driver.find_element(By.ID, "showInput").click()

    displayed_message = driver.find_element(By.ID, "message").text
    assert (
        displayed_message == message
    ), f"Expected '{message}', but got '{displayed_message}'"


# Test Case 2: Drag & Drop Sliders (Fixed)
def test_drag_and_drop_slider(driver):
    driver.get("https://www.lambdatest.com/selenium-playground")
    driver.find_element(By.LINK_TEXT, "Drag & Drop Sliders").click()

    # Select slider
    slider = driver.find_element(By.XPATH, "//input[@value='15']")

    # Using JavaScript to set the value to 95
    driver.execute_script(
        "arguments[0].value = '95'; arguments[0].dispatchEvent(new Event('input'));",
        slider,
    )

    # Wait for the value to update
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "range"), "95")
    )

    # Validate range value
    range_value = driver.find_element(By.ID, "range").text
    assert range_value == "95", f"Expected '95', but got '{range_value}'"


# Test Case 3: Input Form Submit
def test_input_form_submit(driver):
    driver.get("https://www.lambdatest.com/selenium-playground")
    driver.find_element(By.LINK_TEXT, "Input Form Submit").click()

    # Click Submit without filling in the form
    driver.find_element(By.XPATH, "//button[text()='Submit']").click()

    # Validate error message
    error_msg = driver.find_element(
        By.XPATH, "//input[@name='name']/following-sibling::div"
    ).text
    assert "Please fill out this field." in error_msg

    # Fill the form
    driver.find_element(By.NAME, "name").send_keys("John Doe")
    driver.find_element(By.NAME, "email").send_keys("john.doe@example.com")
    driver.find_element(By.NAME, "country").send_keys("United States")

    # Submit the form
    driver.find_element(By.XPATH, "//button[text()='Submit']").click()

    # Validate success message
    success_msg = driver.find_element(By.CLASS_NAME, "success-msg").text
    assert "Thanks for contacting us, we will get back to you shortly." in success_msg
