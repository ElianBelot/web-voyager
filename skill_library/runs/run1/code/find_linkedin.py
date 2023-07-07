def find_linkedin_profile(driver, name):
    # Navigate to LinkedIn homepage
    driver.get("https://www.linkedin.com")

    # Input name into search bar
    search_bar = driver.find_element(By.ID, "search-bar")
    search_bar.send_keys(name)

    # Click the search button
    search_button = driver.find_element(By.ID, "search-button")
    search_button.click()

    # Click the first result
    first_result = driver.find_elements(By.CLASS_NAME, "result")[0]
    first_result.click()

    # Extract and return the profile description
    description = driver.find_element(By.ID, "profile-description").text
    return description
