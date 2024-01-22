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
    # Try to read the settings.json file
    json_file_path = "settings.json"
    
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

    except FileNotFoundError:
        print("Error: settings.json file not found.")
        sys.exit(1)
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the settings.json file.")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Access and check all the settings data
    if data.get("ASES_URL") is None:
        print("Error: ASES_URL is missing in the settings.json file.")
        sys.exit(1)

    if data.get("BUFFER_TIME") is None:
        print("Error: BUFFER_TIME is missing in the settings.json file.")
        sys.exit(1)

    if data.get("LOGIN_DROP_DOWN_INDEX") is None:
        print("Error: LOGIN_DROP_DOWN_INDEX is missing in the settings.json file.")
        sys.exit(1)
        
    if data.get("FINAL_WAIT_IN_SEC") is None:
        print("Error: FINAL_WAIT_IN_SEC is missing in the settings.json file.")
        sys.exit(1)
        
    if data.get("TIME_SLOTS") is None:
        print("Error: TIME_SLOTS is missing in the settings.json file.")
        sys.exit(1)
        
    if data.get("AUTOSAVE") is None:
        print("Error: AUTOSAVE is missing in the settings.json file.")
        sys.exit(1)
        
    if data.get("VERBOSE") is None:
        print("Error: VERBOSE is missing in the settings.json file.")
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
    VERBOSE = settings.get("VERBOSE")

    browser = webdriver.Chrome()

    try:
        browser.get(ASES_URL)
        login(browser, ASES_URL, USERNAME, PASSWORD, LOGIN_DROP_DOWN_INDEX)
        go_to_log_hours_page(browser)
        fill_out_table(browser, TIME_SLOTS, BUFFER_TIME, AUTOSAVE, VERBOSE)

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