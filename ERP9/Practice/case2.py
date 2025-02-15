import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_drag_and_drop_slider(driver):
    """Test Case: Drag slider from 5 to 95 and validate"""

    # Step 1: Open LambdaTest Playground
    driver.get("https://www.lambdatest.com/selenium-playground")

    # Step 2: Click "Drag & Drop Sliders"
    driver.find_element(By.LINK_TEXT, "Drag & Drop Sliders").click()

    # Step 3: Locate slider and range value element
    slider = driver.find_element(By.XPATH, "//input[@type='range']")
    range_value = driver.find_element(By.XPATH, "//output[@id='range']")

    # Print initial slider value
    initial_value = range_value.text
    print(f"Initial Slider Value: {initial_value}")

    # Step 4: Move slider using ActionChains
    action = ActionChains(driver)

    # Get slider width
    slider_width = slider.size["width"]

    # Calculate approximate offset to reach 95
    total_range = 95 - int(initial_value)
    move_per_step = slider_width / 20  # Divide to move gradually

    for _ in range(20):
        action.click_and_hold(slider).move_by_offset(
            move_per_step, 0
        ).release().perform()

        # Fire JavaScript events after each move
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", slider)
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));", slider
        )

        # Retrieve updated slider value
        current_value = driver.execute_script("return arguments[0].value;", slider)
        print(f"Updated Slider Value: {current_value}")

        if current_value == "95":
            break

    # Step 5: Wait for range value to update
    WebDriverWait(driver, 10).until(
        lambda d: driver.execute_script("return arguments[0].value;", slider) == "95"
    )

    # Step 6: Validate final slider value
    final_value = driver.execute_script("return arguments[0].value;", slider)
    assert final_value == "95", f"Expected '95', but got '{final_value}'"

    print(f"✅ Test Passed: Slider moved to {final_value}")
