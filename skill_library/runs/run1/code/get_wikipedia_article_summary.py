def get_wikipedia_article_summary(driver, article_title: str):
    # Navigate to the article
    url = f"https://en.wikipedia.org/wiki/{article_title}"
    print("Navigating to URL:", url)
    driver.get(url)

    # Find the first paragraph. Wikipedia typically structures the summary with 'p' tag after the first 'table' tag.
    summary_element = driver.find_element(selenium.webdriver.common.by.By.XPATH, "//table/following-sibling::p")

    # Extract and return the text
    summary_text = summary_element.text
    return summary_text
