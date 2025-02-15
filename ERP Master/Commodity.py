from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class CommodityMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Chrome WebDriver"""
        service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)

    def login(self, username, password):
        """Logs into the system with the provided credentials."""
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # Enter username and password
        driver.find_element(By.ID, "Login").clear()
        driver.find_element(By.ID, "Login").send_keys(username)
        driver.find_element(By.ID, "Password").clear()
        driver.find_element(By.ID, "Password").send_keys(password)

        # Click login button
        driver.find_element(By.ID, "btnLogin").click()

        # Wait until the Transportation menu is visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("✅ Login successful!")

    def navigate_to_commodity_master(self):
        """Navigates through the menu to reach the Commodity Master section."""
        self.navigate_menu(
            [
                ("Transportation", "Transportation"),
                ("Transportation Master »", "Transportation Master"),
                ("Common Masters »", "Common Masters"),
                ("Commodity", "Commodity"),
            ]
        )

    def navigate_menu(self, menu_items):
        """Navigates through a list of menu items."""
        for link_text, description in menu_items:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"✅ {description} link clicked successfully")

    def switch_to_iframe_containing_element(self, element_id):
        """Switches to the iframe that contains the specified element."""
        driver = self.driver
        driver.switch_to.default_content()

        # Iterate through iframes to locate the desired element
        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(By.ID, element_id):
                    print(
                        f"✅ Switched to iframe containing {element_id} (Index {index})"
                    )
                    return True
            except:
                driver.switch_to.default_content()

        print(f"❌ Unable to locate {element_id} in any iframe!")
        return False

    def add_new_commodity(self):
        """Fills in the Commodity Master form and saves the record."""
        driver = self.driver

        # Click 'New Record' button
        if self.switch_to_iframe_containing_element("btn_NewRecord"):
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
            ).click()
            print("✅ New Record button clicked successfully")

        # Enter 'Footwear' in 'MasterName' field
        if self.switch_to_iframe_containing_element("MasterName"):
            self.fill_text_field("MasterName", "TEST4", "Commodity Name")
            self.fill_text_field("Code", "T4", "Commodity Code")

            # Click 'Save' button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "mysubmit"))
            ).click()
            print("✅ Commodity saved successfully")

    def fill_text_field(self, field_id, value, description):
        """Fills a text field with the given value."""
        driver = self.driver
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )

        # Scroll to the field, click, and enter value
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)
        driver.execute_script(f"arguments[0].value = '{value}';", element)
        print(f"✅ {description} field updated successfully with '{value}'")

    def test_commodity_master(self):
        """Main test case: Logs in, navigates, and adds a new commodity."""
        self.login("Riddhi", "OMSGN9")
        self.navigate_to_commodity_master()
        self.add_new_commodity()

    @classmethod
    def tearDownClass(cls):
        """Closes the browser session after tests are completed."""
        cls.driver.quit()
        print("🔒 Browser closed.")


if __name__ == "__main__":
    unittest.main()
