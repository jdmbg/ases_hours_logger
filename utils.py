import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def login(browser: webdriver, username: str, password: str):
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

    # Press the down arrow 5 times to reach the 6th item
    for _ in range(5):
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
    z_atoss_buttons = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'z-atossbutton'))
    )
    log_hours_page_button_ref = z_atoss_buttons[6]
    ActionChains(browser).move_to_element(
        log_hours_page_button_ref).click().perform()


def send_keys_and_wait(actions: ActionChains, keys: str, buffer_time: int):
    actions.send_keys(keys)
    actions.pause(buffer_time)


def fill_out_table(browser: webdriver, time_slots: dict, buffer_time: int):

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
            print(
                f"\nDay {date_cell.text} is in the weekend" +
                " or a vacation day.\nIGNORED\n")

        # Ignore if already set
        elif (":" in from_cell.text):
            print(
                f"\nDay {date_cell.text} is already set.\nIGNORED\n")

        # Fill out table
        else:
            print(
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

            print("DONE\n")
