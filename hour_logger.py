import sys
import json
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
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
                data.get("LOGIN_DROP_DOWN_INDEX"),
                data.get("FINAL_WAIT_IN_SEC"),
                data.get("TIME_SLOTS"),
                data.get("AUTOSAVE")):
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
    LOGIN_DROP_DOWN_INDEX = settings.get("LOGIN_DROP_DOWN_INDEX")
    FINAL_WAIT_IN_SEC = settings.get("FINAL_WAIT_IN_SEC")
    TIME_SLOTS = settings.get("TIME_SLOTS")
    AUTOSAVE = settings.get("AUTOSAVE")

    browser = webdriver.Chrome()

    try:
        browser.get(ASES_URL)
        login(browser, ASES_URL, USERNAME, PASSWORD, LOGIN_DROP_DOWN_INDEX)
        go_to_log_hours_page(browser)
        fill_out_table(browser, TIME_SLOTS, BUFFER_TIME, AUTOSAVE)

        print(f"Waiting {FINAL_WAIT_IN_SEC} before closing window.")
        time.sleep(FINAL_WAIT_IN_SEC)
    except WebDriverException as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            print("\nCaught net::ERR_NAME_NOT_RESOLVED exception."
                  "\nPlease check your internet connection or the "
                  "provided ASES_URL.\nYou may also need to connect "
                  "to your employer's VPN network.\n")

        else:
            print(f"Caught WebDriverException: {e}")

    finally:
        browser.quit()


if __name__ == "__main__":
    main()
