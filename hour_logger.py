import sys
import json
import time
from utils import go_to_log_hours_page, fill_out_table


# Check requirements have been installed
try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException, TimeoutException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

except ModuleNotFoundError:
    print("\nA required module was not found." +
          "\nPlease run 'pip3 install -r requirements.txt'\n")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)


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
    settings_to_check = ["ASES_URL", "COMPANY_EMAIL", "BUFFER_TIME",
                         "FINAL_WAIT_IN_SEC", "TIME_SLOTS", "AUTOSAVE", "VERBOSE"]

    for setting in settings_to_check:
        if data.get(setting) is None:
            print(f"Error: {setting} is missing in the settings.json file.")
            sys.exit(1)

    return data


def handle_sso_login(browser, company_email: str):
    """Wait for the Microsoft SSO email field, fill it in and click Next."""
    try:
        print("SSO: Waiting for email field...")
        email_field = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_field.clear()
        email_field.send_keys(company_email)
        print(f"SSO: Entered company email ({company_email}).")

        next_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        next_button.click()
        print("SSO: Clicked Next. Please select your certificate and click OK.")

    except TimeoutException:
        print("SSO: Email field not detected, skipping.")


def handle_stay_signed_in(browser):
    """Click the confirm button on the Stay signed in page if it appears.
    Uses the page ID instead of button text to be language-agnostic."""
    try:
        # Wait for the Stay signed in page by its unique form ID
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "KmsiCheckboxField"))
        )
        # Click the primary submit button (Yes/Ja) regardless of language
        yes_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        yes_button.click()
        print("Stay signed in: clicked confirm button.")
    except TimeoutException:
        pass  # Page did not appear, continue normally


def wait_for_ases_page(browser, ases_url: str):
    """Wait until the user has completed authentication and the ASES page is loaded."""
    print("Waiting for ASES page (user must complete certificate selection)...")
    WebDriverWait(browser, 120).until(EC.url_contains(ases_url))
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("ASES page loaded, continuing...")


def main():

    # Load settings
    settings = load_settings()
    ASES_URL = settings.get("ASES_URL")
    COMPANY_EMAIL = settings.get("COMPANY_EMAIL")
    BUFFER_TIME = settings.get("BUFFER_TIME")
    FINAL_WAIT_IN_SEC = settings.get("FINAL_WAIT_IN_SEC")
    TIME_SLOTS = settings.get("TIME_SLOTS")
    AUTOSAVE = settings.get("AUTOSAVE")
    VERBOSE = settings.get("VERBOSE")

    # Use Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    browser = webdriver.Chrome(options=chrome_options)

    try:
        browser.get(ASES_URL)

        # Step 1: Auto-fill SSO email and click Next
        handle_sso_login(browser, COMPANY_EMAIL)

        # Step 2: User manually selects certificate and clicks OK
        # Step 2b: Automatically click Yes on "Stay signed in?" if it appears
        handle_stay_signed_in(browser)

        # Step 3: Wait until ASES page is fully loaded, then run the script
        wait_for_ases_page(browser, ASES_URL)

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