from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from bs4 import BeautifulSoup

# Firefox and Chrome Drivers
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import datetime

import threading

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# Replace with your path to credentials.json file within the credntials folder
# Ensure you have the correct path to your credentials file
SERVICE_ACCOUNT_FILE = 'replace with your path to credentials.json'
# Replace with your Google Sheets ID
SPREADSHEET_ID = 'replace with your Google Sheets ID'
# range of cells to read and write data, example template will be within the README file
RANGE_NAME = 'Main!B2:E'

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Set up the Chrome driver with options to disable WebRTC
options = webdriver.ChromeOptions()
options.add_argument("--disable-webrtc")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

stop_event = threading.Event()

# Gets box numbers
def get_box_numbers(url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    box_numbers = []
    for div in soup.find_all('div', class_='index_boxNumber__7k_Uf'):
        box_number = div.get_text(strip=True).replace("No.", "").strip()
        if box_number:
            box_numbers.append(box_number)
    return box_numbers

def is_in_stock(url):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    try:
        # Check for the "Pick One to Shake" or "Buy Multiple Boxes" button
        driver.find_element(
            "xpath",
            "//button[span[contains(text(), 'Pick One to Shake')] or span[contains(text(), 'Buy Multiple Boxes')] or span[contains(text(), 'ADD TO BAG')]]"
        )
        return True
    except NoSuchElementException:
        return False

# main method to check for stock
def main():
    # setup
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get('values', [])
    updates = []

    for idx, row in enumerate(rows, start=2):
        url = row[0]
        box_numbers = get_box_numbers(url)
        first_box_number = box_numbers[0] if box_numbers else ""
        status = "In Stock" if is_in_stock(url) else "Out of Stock"
        date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Prepare the update for the columns C, D, E
        updates.append({
            'range': f'Main!C{idx}:E{idx}',
            'values': [[date_checked, status, first_box_number]]
        })

    # Update to Sheets
    body = {'valueInputOption': 'RAW', 'data': updates}
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()

def main_loop():
    print("Starting the script. Press 'q' then Enter to quit.")
    while not stop_event.is_set():
        main()
        # wait for 5 minutes or until stop_event is set
        stop_event.wait(timeout=300)
    driver.quit()

def wait_for_quit():
    while True:
        if input().strip().lower() == 'q':
            stop_event.set()
            print("Stopping the script...")
            break

if __name__ == "__main__":
    threading.Thread(target=wait_for_quit, daemon=True).start()
    main_loop()