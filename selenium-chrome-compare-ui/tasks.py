from celery import Celery
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import cv2
import numpy as np
import os

celery = Celery('tasks', broker='redis://redis:6379/0')

@celery.task
def capture_initial_screenshot(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Open the website
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Take screenshots by scrolling
    screenshots = []
    scroll_pause_time = 1  # Adjust the pause time between scrolls

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down in steps and take screenshots
    for i in range(0, total_height, 800):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(scroll_pause_time)
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(screenshot)

    # Save the screenshots as a single image
    final_image = np.zeros((total_height, driver.get_window_size()["width"], 3), dtype=np.uint8)

    current_y = 0
    for screenshot in screenshots:
        img = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)
        final_image[current_y:current_y + img.shape[0], :, :] = img
        current_y += img.shape[0]

    # Define path
    url_safe = url.replace('http://', '').replace('https://', '').replace('/', '_')
    initial_screenshot_path = f"/app/screenshots/initial/{url_safe}_initial.png"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(initial_screenshot_path), exist_ok=True)

    # Save the final image
    cv2.imwrite(initial_screenshot_path, final_image)

    # Close the browser
    driver.quit()

@celery.task
def compare_website_screenshots(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Open the website
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Take screenshots by scrolling
    screenshots = []
    scroll_pause_time = 1  # Adjust the pause time between scrolls

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down in steps and take screenshots
    for i in range(0, total_height, 800):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(scroll_pause_time)
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(screenshot)

    # Save the screenshots as a single image
    final_image = np.zeros((total_height, driver.get_window_size()["width"], 3), dtype=np.uint8)

    current_y = 0
    for screenshot in screenshots:
        img = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)
        final_image[current_y:current_y + img.shape[0], :, :] = img
        current_y += img.shape[0]

    # Define paths
    url_safe = url.replace('http://', '').replace('https://', '').replace('/', '_')
    result_path = f"/app/screenshots/results/{url_safe}_screenshot.png"
    expected_image_path = f"/app/screenshots/expected/{url_safe}_expected.png"
    result_diff_path = f"/app/screenshots/results/{url_safe}_screenshot_diff.png"
    expected_diff_path = f"/app/screenshots/results/{url_safe}_expected_diff.png"
    side_by_side_path = f"/app/screenshots/results/{url_safe}_side_by_side.png"

    # Save the final image
    cv2.imwrite(result_path, final_image)

    # Load the expected image
    expected_image = cv2.imread(expected_image_path)
    if expected_image is None:
        print(f"Expected image for {url} not found at {expected_image_path}")
        driver.quit()
        return

    # Convert images to grayscale
    gray_final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)
    gray_expected_image = cv2.cvtColor(expected_image, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = compare_ssim(gray_final_image, gray_expected_image, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Find contours of the differences
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Draw bounding boxes around the differences
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(final_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(expected_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save the final images with differences highlighted
    cv2.imwrite(result_diff_path, final_image)
    cv2.imwrite(expected_diff_path, expected_image)

    # Create side-by-side comparison
    side_by_side = np.hstack((expected_image, final_image))
    cv2.imwrite(side_by_side_path, side_by_side)

    # Print the percentage of difference
    print(f"SSIM for {url}: {score}")
    print(f"Difference for {url}: {(1 - score) * 100:.2f}%")

    # Close the browser
    driver.quit()
