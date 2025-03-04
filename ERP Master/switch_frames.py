def switch_frames(self, element_id):
    """Switches to the correct iframe containing the specified element."""
    driver = self.driver
    driver.switch_to.default_content()

    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        driver.switch_to.frame(iframe)
        if driver.find_elements(By.ID, element_id):
            return True
        print(f"Switched to iframe containing {element_id}")

        driver.switch_to.default_content()
    print(f"Unable to locate {element_id} in any iframe!")
    return False
