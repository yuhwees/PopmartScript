import csv
from bs4 import BeautifulSoup

# Firefox and Chrome Drivers
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import time

# Set up the Chrome driver with options to disable WebRTC
options = webdriver.ChromeOptions()
options.add_argument("--disable-webrtc")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

#URLs for products
url = 'https://www.popmart.com/us'

driver.get(url)

def get_box_numbers(set_number):
    # Go to main page of the set
    url = f'https://www.popmart.com/us/pop-now/set/{set_number}'
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    box_numbers = set()
    # find all links or elements that match the product URL pattern
    for div in soup.find_all('div', class_='index_boxNumber__7k_Uf'):
        box_number = div.get_text(strip=True)
        if box_number:
            box_number = box_number.replace("No.", "").strip() #Remove "No."
            box_numbers.add(box_number)
    return box_numbers

def get_url(set_number, box_number):
    """
    This function takes a search term and returns the URL for that term.
    """
    base_url = 'https://www.popmart.com/us/pop-now/set/{}-{}'
    return base_url.format(set_number, box_number)

def is_in_stock(url):
    driver.get(url)
    time.sleep(2)
    try:
        # Check for the "Pick One to Shake" or "Buy Multiple Boxes" button
        # Looks for either button by their text, as shown in your screenshot
        driver.find_element(
            "xpath",
            "//button[span[contains(text(), 'Pick One to Shake')] or span[contains(text(), 'Buy Multiple Boxes')]]"
        )
        return True
    except NoSuchElementException:
        return False
    


# main method to check for stock
def main(set_number):
    try:
        while True:
            box_numbers = get_box_numbers(set_number)
            for box_number in box_numbers:
                url = get_url(set_number, box_number)
                if is_in_stock(url):
                    print(f'Box {box_number} from set {set_number} is in stock: {url}')
            #time.sleep(5)  # Wait for 5 seconds before checking again
    except KeyboardInterrupt:
        print("Script interrupted by user.")
        driver.quit()

input_set_number = input("Enter the set number to check: ")

main(input_set_number)