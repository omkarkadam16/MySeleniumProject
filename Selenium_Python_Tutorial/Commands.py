from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set up the Chrome WebDriver
service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the website
driver.get("https://www.example.com")

# Get and print the page title
page_title = driver.title
print(f"Page Title: {page_title}")

# Get and print the current URL
current_url = driver.current_url
print(f"Current URL: {current_url}")

# Get and print the page source (optional, as it can be very large)
# print(f"Page Source: {driver.page_source}")

# Find a text box and enter text
try:
    text_box = driver.find_element(By.ID, "TextBox")
    text_box.send_keys("GeeksForGeeks")
except:
    print("TextBox element not found!")

# Check if an element is displayed
try:
    element = driver.find_element(By.ID, "gfg")
    is_displayed = element.is_displayed()
    print(f"Element is displayed: {is_displayed}")
except:
    print("Element not found!")

# Check if a checkbox is selected
try:
    checkbox = driver.find_element(By.ID, "software-testing")
    is_selected = checkbox.is_selected()
    print(f"Checkbox is selected: {is_selected}")
except:
    print("Checkbox not found!")

# Submit a form
try:
    submit_button = driver.find_element(By.ID, "SubmitButton")
    submit_button.submit()
except:
    print("Submit button not found!")

# Check if an element is enabled
try:
    is_enabled_element = driver.find_element(By.ID, "GFG")
    is_enabled = is_enabled_element.is_enabled()
    print(f"Element is enabled: {is_enabled}")
except:
    print("Element not found!")

# Get element location
try:
    location_element = driver.find_element(By.ID, "Selenium")
    x_coordinate = location_element.location['x']
    y_coordinate = location_element.location['y']
    print(f"X Coordinate: {x_coordinate}, Y Coordinate: {y_coordinate}")
except:
    print("Location element not found!")

# Clear input field
try:
    clear_element = driver.find_element(By.ID, "edittext")
    clear_element.clear()
except:
    print("Clearable element not found!")

# Get element size
try:
    size_element = driver.find_element(By.ID, "SubmitButton")
    element_height = size_element.size['height']
    element_width = size_element.size['width']
    print(f"Element Height: {element_height}, Element Width: {element_width}")
except:
    print("Size element not found!")

# Get an element's attribute
try:
    attribute_element = driver.find_element(By.ID, "Submit")
    attribute_value = attribute_element.get_attribute("id")
    print(f"Attribute Value: {attribute_value}")
except:
    print("Attribute element not found!")

# Click a button or link
try:
    click_element = driver.find_element(By.ID, "GeeksForGeeks")
    click_element.click()
except:
    print("Clickable element not found!")

# Close the browser window
driver.close()

# Quit the WebDriver session
driver.quit()
