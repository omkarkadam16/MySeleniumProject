from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the Chrome WebDriver and open the browser."""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def switch_to_iframe(self, element_id):
        """Switch to the iframe that contains the specified element."""
        driver = self.driver
        driver.switch_to.default_content()

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframes):
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

    def test_commodity(self):
        """Perform login and navigate to the Commodity Master section."""
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # Enter credentials and log in
        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()

        # Wait for the Transportation menu to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("✅ Login successful!")

        # Navigate through menu items
        menu_items = [
            ("Transportation", "Transportation"),
            ("Transportation Master »", "Transportation Master"),
            ("Common Masters »", "Common Masters"),
            ("Commodity", "Commodity Masters"),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"✅ {description} link clicked successfully")

        # Switch to iframe containing 'New Record' button
        if self.switch_to_iframe("btn_NewRecord"):
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
            ).click()
            print("✅ New Record button clicked successfully")

        # Switch to iframe containing 'MasterName' field
        if self.switch_to_iframe("MasterName"):
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "MasterName"))
            ).send_keys("TEST8")
            print("✅ Commodity Name field filled")

            driver.find_element(By.ID, "Code").send_keys("T8")
            print("✅ Commodity Code field filled")

            driver.find_element(By.ID, "mysubmit").click()
            print("✅ Commodity saved successfully")

    @classmethod
    def tearDownClass(cls):
        """Close the browser after all tests are completed."""
        cls.driver.quit()
        print("🔒 Browser closed.")


if __name__ == "__main__":
    unittest.main()
