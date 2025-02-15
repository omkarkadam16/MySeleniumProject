from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.maximize_window()

driver.get("https://www.google.com")

search_Box = driver.find_element(By.NAME,"q")
search_Box.send_keys("Hero Isl")    

time.sleep(2)

search_Box.send_keys(Keys.RETURN)

time.sleep(2)

driver.quit()


