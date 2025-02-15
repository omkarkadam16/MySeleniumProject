from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument(
            "--disable-gpu"
        )  # Disable GPU (helps in headless mode)
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument(
            "--disable-dev-shm-usage"
        )  # Prevent resource issues

        service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(30)  # Implicit wait

    def test_item_master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # Login
        driver.find_element(By.ID, "Login").clear()
        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").clear()
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()

        # Wait for redirection after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("Login successful!")

        # Click on 'Transportation' link
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transportation"))
        ).click()
        print("Transportation link clicked successfully")

        # Navigate through menu items
        menu_items = [
            ("Transportation Master »", "Transportation Master"),
            ("Common Masters »", "Common Masters"),
            ("Item Master", "Item Master"),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"{description} link clicked successfully")

        # Handle iframe switching dynamically for New Record button
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for index, iframe in enumerate(iframes):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(By.ID, "btn_NewRecord"):
                    print(f"Switched to correct iframe at index {index}")
                    break
            except:
                driver.switch_to.default_content()

        # Click "New Record" button
        new_record_btn = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
        )
        new_record_btn.click()
        print("New Record button clicked successfully")

        # Switch to iframe for TransportProductName
        driver.switch_to.default_content()
        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(By.ID, "TransportProductName"):
                    print(
                        f"Switched to correct iframe at index {index} for TransportProductName"
                    )
                    break
            except:
                driver.switch_to.default_content()

        # Enter Product Name
        try:
            product_name = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.ID, "TransportProductName"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", product_name)
            driver.execute_script("arguments[0].click();", product_name)
            print("TransportProductName clicked successfully")
            product_name.send_keys("Vegetables")
            print("TransportProductName field updated successfully")
        except Exception as e:
            print(f"Error interacting with TransportProductName: {str(e)}")

        # **Switch to iframe for CommodityTypeId**
        driver.switch_to.default_content()
        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(index)
            try:
                if driver.find_element(By.ID, "CommodityTypeId"):
                    print(
                        f"Switched to correct iframe at index {index} for CommodityTypeId"
                    )
                    break
            except:
                driver.switch_to.default_content()

        # **Wait and click on CommodityTypeId dropdown**
        try:
            commodity_type = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "CommodityTypeId"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", commodity_type)
            driver.execute_script("arguments[0].click();", commodity_type)
            print("CommodityTypeId dropdown clicked successfully")

            # Select "FOOD ITEMS"
            select = Select(driver.find_element(By.ID, "CommodityTypeId"))
            select.select_by_visible_text("FOOD ITEMS")
            print("Commodity type selected successfully")

        except Exception as e:
            print(f"Error interacting with CommodityTypeId: {str(e)}")

        # Click Submit
        try:
            submit_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "mysubmit"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
            driver.execute_script("arguments[0].click();", submit_btn)
            print("Form submitted successfully")
        except Exception as e:
            print(f"Error clicking submit button: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
