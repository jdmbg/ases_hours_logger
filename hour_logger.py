import sys
import json
import time
from utils import login, go_to_log_hours_page, fill_out_table


# Check requirements have been installed
try:
    import getpass
    from pykeepass import PyKeePass
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options

except ModuleNotFoundError:
    print("\nA required module was not found." +
          "\nPlease run 'pip3 install -r requirements.txt'\n")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)


def load_credentials(use_ases_credentials: bool,
                     ases_username: str,
                     ases_password: str,
                     use_keypass_credentials: bool,
                     keepass_database_file_path: str,
                     keepass_entry_title: str):

    if len(sys.argv) < 3 and use_keypass_credentials is False and use_ases_credentials is False:
        print('Usage: python script.py "USERNAME" "PASSWORD"')
        sys.exit(1)
    if use_keypass_credentials is True:
        # Get credentials from Keypass
        pswd = getpass.getpass('\nPlease enter your KeePass master password:')
        kp = PyKeePass(keepass_database_file_path, password=pswd)
        entry = kp.find_entries(title=keepass_entry_title, first=True)
        return entry.username, entry.password
    if use_ases_credentials is True:
        return ases_username, ases_password
    else:
        # Get credentials from command line arguments
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
    settings_to_check = ["ASES_URL", "USE_ASES_CREDENTIALS", "ASES_USERNAME", "ASES_PASSWORD", "BUFFER_TIME", "LOGIN_DROP_DOWN_INDEX",
                         "FINAL_WAIT_IN_SEC", "TIME_SLOTS", "AUTOSAVE",
                         "VERBOSE", "USE_KEEPASS_CREDENTIALS",
                         "KEEPASS_DATABASE_FILE_PATH", "KEEPASS_ENTRY_TITLE"]

    # Access and check all the settings data
    for setting in settings_to_check:
        if data.get(setting) is None:
            print(f"Error: {setting} is missing in the settings.json file.")
            sys.exit(1)

    return data


def main():

    # Load settings
    settings = load_settings()
    ASES_URL = settings.get("ASES_URL")
    USE_ASES_CREDENTIALS = settings.get("USE_ASES_CREDENTIALS")
    ASES_USERNAME = settings.get("ASES_USERNAME")
    ASES_PASSWORD = settings.get("ASES_PASSWORD")
    BUFFER_TIME = settings.get("BUFFER_TIME")
    LOGIN_DROP_DOWN_INDEX = settings.get("LOGIN_DROP_DOWN_INDEX")
    FINAL_WAIT_IN_SEC = settings.get("FINAL_WAIT_IN_SEC")
    TIME_SLOTS = settings.get("TIME_SLOTS")
    AUTOSAVE = settings.get("AUTOSAVE")
    VERBOSE = settings.get("VERBOSE")
    USE_KEEPASS_CREDENTIALS = settings.get("USE_KEEPASS_CREDENTIALS")
    KEEPASS_DATABASE_FILE_PATH = settings.get("KEEPASS_DATABASE_FILE_PATH")
    KEEPASS_ENTRY_TITLE = settings.get("KEEPASS_ENTRY_TITLE")

    # Load credentials
    USERNAME, PASSWORD = load_credentials(USE_ASES_CREDENTIALS,
                                          ASES_USERNAME,
                                          ASES_PASSWORD,
                                          USE_KEEPASS_CREDENTIALS,
                                          KEEPASS_DATABASE_FILE_PATH,
                                          KEEPASS_ENTRY_TITLE)

    # Disable search engine choice screen with Chrome and selenium 
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    browser = webdriver.Chrome(options=chrome_options)

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
