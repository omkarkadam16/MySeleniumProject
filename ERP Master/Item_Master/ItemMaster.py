from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome WebDriver service
        service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(30)  # Implicit wait to handle minor delays

    def test_item_master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")  # Open the login page

        # Login Process
        driver.find_element(
            By.ID, "Login"
        ).clear()  # Clear the input field before entering text
        driver.find_element(By.ID, "Login").send_keys("Riddhi")  # Enter username
        driver.find_element(By.ID, "Password").clear()  # Clear the password field
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")  # Enter password
        driver.find_element(By.ID, "btnLogin").click()  # Click login button

        # Wait for page to load after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("Login successful!")

        # Navigate to 'Transportation' section
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transportation"))
        ).click()
        print("Transportation link clicked successfully")

        # Navigate through menu items step by step
        menu_items = [
            ("Transportation Master »", "Transportation "),
            ("Common Masters »", "Common "),
            ("Item Master", "Item "),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"{description} link clicked successfully")

        # Handle iframe switching dynamically to locate 'New Record' button
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for index, iframe in enumerate(iframes):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(
                    By.ID, "btn_NewRecord"
                ):  # Verify button exists in iframe
                    print(f"Switched to correct iframe at index {index}")
                    break
            except:
                driver.switch_to.default_content()

        # Click the 'New Record' button
        new_record_btn = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
        )
        new_record_btn.click()
        print("New Record button clicked successfully")

        # Locate the iframe containing 'TransportProductName' input field
        driver.switch_to.default_content()
        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(
                    By.ID, "TransportProductName"
                ):  # Check if field exists
                    print(
                        f"Switched to correct iframe at index {index} for TransportProductName"
                    )
                    break
            except:
                driver.switch_to.default_content()

        # Enter Product Name into the input field
        try:
            product_name = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.ID, "TransportProductName"))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView();", product_name
            )  # Scroll to field
            driver.execute_script(
                "arguments[0].click();", product_name
            )  # Click field before input
            print("TransportProductName clicked successfully")
            product_name.send_keys("Oil")  # Enter the product name
            print("TransportProductName field updated successfully")
        except Exception as e:
            print(f"Error interacting with TransportProductName: {str(e)}")

        # Locate the iframe containing 'CommodityTypeId' dropdown
        driver.switch_to.default_content()
        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(
                    By.ID, "CommodityTypeId"
                ):  # Verify dropdown exists
                    print(
                        f"Switched to correct iframe at index {index} for CommodityTypeId"
                    )
                    break
            except:
                driver.switch_to.default_content()

        # Select 'FOOD ITEMS' from the CommodityType dropdown
        try:
            commodity_type = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "CommodityTypeId"))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView();", commodity_type
            )  # Scroll to dropdown
            driver.execute_script(
                "arguments[0].click();", commodity_type
            )  # Click dropdown
            print("CommodityTypeId dropdown clicked successfully")

            # Select option "FOOD ITEMS"
            select = Select(driver.find_element(By.ID, "CommodityTypeId"))
            select.select_by_visible_text("FOOD ITEMS")  # Select food category
            print("Commodity type selected successfully")
        except Exception as e:
            print(f"Error interacting with CommodityTypeId: {str(e)}")

        # Submit the form
        try:
            submit_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "mysubmit"))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView();", submit_btn
            )  # Scroll to button
            driver.execute_script(
                "arguments[0].click();", submit_btn
            )  # Click submit button
            print("Form submitted successfully")
        except Exception as e:
            print(f"Error clicking submit button: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # Close the browser session


if __name__ == "__main__":
    unittest.main()  # Run the test
