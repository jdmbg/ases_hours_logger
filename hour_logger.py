import sys
import json
import time
from selenium import webdriver
from utils import login, go_to_log_hours_page, fill_out_table


def load_credentials():
    # Check the number of command-line arguments
    if len(sys.argv) < 3:
        print('Usage: python script.py "USERNAME" "PASSWORD"')
        sys.exit(1)

    return sys.argv[1], sys.argv[2]


def load_settings():
    # Read settings
    json_file_path = "settings.json"
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Access the settings data
    if None in (data.get("ASES_URL"),
                data.get("BUFFER_TIME"),
                data.get("FINAL_WAIT_IN_SEC"),
                data.get("TIME_SLOTS")):
        print("Error: Invalid or missing settings in the configuration file.")
        sys.exit(1)

    return data


def main():

    # Load credentials
    USERNAME, PASSWORD = load_credentials()

    # Load settings
    settings = load_settings()
    ASES_URL = settings.get("ASES_URL")
    BUFFER_TIME = settings.get("BUFFER_TIME")
    FINAL_WAIT_IN_SEC = settings.get("FINAL_WAIT_IN_SEC")
    TIME_SLOTS = settings.get("TIME_SLOTS")

    browser = webdriver.Chrome()

    try:
        browser.get(ASES_URL)
        login(browser, USERNAME, PASSWORD)
        go_to_log_hours_page(browser)
        fill_out_table(browser, TIME_SLOTS, BUFFER_TIME)
        time.sleep(FINAL_WAIT_IN_SEC)
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
