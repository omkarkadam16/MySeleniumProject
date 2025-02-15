import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Correct file path (Use r"" or \\)
service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")  
driver = webdriver.Chrome(service=service)

# Open a webpage
driver.get("https://www.google.com")

# Sleep for page to load
time.sleep(2)

# Find the search box element and type query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium WebDriver")

# Press enter to search
search_box.submit()

# Sleep for page to load
time.sleep(2)   

# Print the page title
print("Page title:", driver.title)  

# Find the first search result
first_result = driver.find_element(By.CSS_SELECTOR, "h3.LC20lb.DKV0Md")
print("First search result:", first_result.text)

# Click on the first search result
first_result.click()

# Sleep for page to load
time.sleep(2)

# Print the page title
print("Page title after clicking:", driver.title)

# Close the browser
driver.quit()
