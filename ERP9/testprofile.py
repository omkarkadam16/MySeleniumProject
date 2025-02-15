# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
import unittest

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "http://192.168.0.72/Rlogic9RLS/UserDesk#icon_dock_computer331"

    def test_admin_navigation(self):
        """Test case to navigate to 'Administration' and check its presence"""
        driver = self.driver
        driver.get(self.base_url)

        try:
            # Check if the page has iframes and switch to it
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                driver.switch_to.frame(iframes[0])  # Switch to first iframe
                print("Switched to iframe successfully!")

            # Wait for Administration link
            admin_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Administration"))
            )

            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView();", admin_link)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(admin_link)).click()

            print("Navigated to 'Administration' successfully!")

        except TimeoutException:
            print("Error: 'Administration' link was not found within the given time.")
            self.take_screenshot(driver, "admin_link_not_found.png")

        except NoSuchElementException:
            print("Error: 'Administration' element does not exist.")
            self.take_screenshot(driver, "admin_element_missing.png")

    def take_screenshot(self, driver, filename):
        """Take a screenshot for debugging"""
        driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
