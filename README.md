# ases_hours_logger

**Python Selenium-Based Hour Logger for ASES**

## Description

This tool is designed to streamline the process of booking work hours for employees using the [ASES tool from ATOSS](https://www.atoss.com/en). It is optimized for websites in German.

### Key Features

- **Time-Saving Automation:** The tool automates the process of logging hours, aiming to save employees valuable time.
- **Intelligent Booking:** It excludes vacation days and weekends from the booking process, ensuring hours are only logged on available workdays.
- **Error Prevention:** The script avoids duplicating entries on days that have already been booked, minimizing errors in the logging process.

### Usage Instructions

Run the script, taking note of the following considerations:
   - **Language Assumption:** The tool assumes the website language is German. Adjust if necessary.
   - **Post-Script Verification:** After running the script, it is essential for the employee to verify the accuracy of the logged hours, make any necessary adjustments, and **manually click on the SAVE button**.

By leveraging this tool, employees can enhance efficiency in the hours booking process while maintaining control over the final submission. Feel free to customize settings and provide feedback for further improvements.

## Setup

To run the script, follow these steps:

1. Install the required dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

2. Adjust your settings in the `settings.json` file:

    - **ASES_URL**: The URL to access the ASES webpage of your employer.
    - **TIME_SLOTS**: Define the time slots you want to log. These assume an 8-hour shift with a 1-hour lunch break each day. On Fridays only 7 hours are booked. You can adjust this at will.
    - **BUFFER_TIME**: The time that passes between each browser action. We need a bit of time between actions for performance reasons. Only adjust if needed, for example, if your internet connection is slow. The default is 0.3 seconds.
    - **FINAL_WAIT_IN_SEC**: The time that the browser window will remain open after completing all booking actions. The default is 60 seconds.

3. Run the script:

    ```bash
    python3 hour_logger.py "ASES_USERNAME" "ASES_PASSWORD"
    ```

4. See the magic happen 🧙.
5. Ensure everything was logged correctly and **manually click on the "SAVE" button**.

Feel free to customize the settings to match your specific needs. If you encounter any issues, consider adjusting the waiting times or reaching out for support. Happy logging!