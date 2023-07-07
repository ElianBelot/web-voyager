def scroll(driver, direction: str):
    # Get the height of the current window
    window_height = driver.execute_script("return window.innerHeight")
    if direction == "up":
        window_height = -window_height

    # Scroll by 1 window height
    driver.execute_script(f"window.scrollBy(0, {window_height})")
    print(f"Scrolled {direction} by {window_height}px")
