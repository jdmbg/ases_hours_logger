import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def login(browser: webdriver,
          ases_url: str,
          username: str,
          password: str,
          drop_down_index: int):
    # Wait for the iframe to be present on the page
    iframe = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'applicationIframe'))
    )
    # Switch to the iframe
    browser.switch_to.frame(iframe)

    # Get necessary elements
    input_fields = browser.find_elements(By.TAG_NAME, 'input')
    buttons = browser.find_elements(By.TAG_NAME, "button")

    user_field = input_fields[0]
    password_field = input_fields[1]
    drop_down = input_fields[2]
    login_button = buttons[1]

    # Fill out form and login
    user_field.send_keys(username)
    password_field.send_keys(password)
    drop_down.click()

    # If ClientNo not specified in the ases_url -> select manually
    if "ClientNo" not in ases_url:
        # Press the down arrow drop_down_index times to reach the desired item
        for _ in range(drop_down_index):
            drop_down.send_keys(Keys.ARROW_DOWN)
        drop_down.send_keys(Keys.ENTER)
    login_button.click()


def go_to_log_hours_page(browser: webdriver):
    # Click on nav_menu button
    nav_menu = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, 'nav_menu'))
    )
    nav_menu.click()

    # Click on log_hours button
    log_hours_page_button_xpath = "//span[@class='btn-label' \
                and text()='Erfassen Zeitbuchung']"
    log_hours_page_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, log_hours_page_button_xpath))
    )
    ActionChains(browser).move_to_element(
        log_hours_page_button).click().perform()


def send_keys_and_wait(actions: ActionChains, keys: str, buffer_time: int):
    actions.send_keys(keys)
    actions.pause(buffer_time)


def fill_out_table(browser: webdriver,
                   time_slots: dict,
                   buffer_time: int,
                   autosave: bool,
                   verbose: bool):

    # Locate the table element
    table = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'grid-canvas'))
    )
    rows = table.find_elements(By.CLASS_NAME, "slick-row")
    number_or_rows = len(rows)

    # Iterate over rows
    for i in range(number_or_rows):
        table = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'grid-canvas')))
        row = table.find_elements(By.CLASS_NAME, "slick-row")[i]

        # Get Cell information
        cells = row.find_elements(By.CLASS_NAME, "slick-cell")
        date_cell = cells[0]
        weekday_cell = cells[1]
        absence_code_cell = cells[-1]
        from_cell = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(cells[4]))

        # Ignore if weekend or vacation day
        if (weekday_cell.text == 'Sa'
            or weekday_cell.text == 'So'
                or absence_code_cell.text == 'U'):
            showMessage(verbose,
                f"\nDay {date_cell.text} is in the weekend" +
                " or a vacation day.\nIGNORED\n")

        # Ignore if already set
        elif (":" in from_cell.text):
            showMessage(verbose,
                f"\nDay {date_cell.text} is already set.\nIGNORED\n")

        # Fill out table
        else:
            showMessage(verbose,
                f"\nFilling out day {date_cell.text}" +
                f" with {time_slots[weekday_cell.text]} ...")

            # Click on cell
            from_cell.click()
            from_cell.click()

            # Wait for pop up window to appear
            button_xpath = "//button[@class='z-button' \
                and text()='Übernehmen']"
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, button_xpath)))

            # Fill in hours
            actions = ActionChains(browser)
            for i in range(4):
                send_keys_and_wait(actions, Keys.TAB, buffer_time)
                send_keys_and_wait(
                    actions, time_slots[weekday_cell.text][i], buffer_time)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(buffer_time)

    if autosave:
        save_button_xpath = '//a[@class="z-toolbarbutton" and \
            .//span[contains(text(), "Speichern")]]'
        save_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, save_button_xpath)))
        save_button.click()
        print("\nSaved changes. Done.")
    else:
        print("\nDone with booking. Please click on the save button.")


def showMessage(verbose: bool, msg: str):
    if verbose:
        print("\n", msg)