# DB Bot for Bumble

DB Bot is an automated script for interacting with Bumble profiles. It's built using Selenium and Python, designed to mine profile data for analysis.

## Prerequisites

Before you start, ensure you have the following:

- Python 3.x
- Google Chrome
- ChromeDriver compatible with your Chrome version

## Installation

1. **Clone the Repository:**

   ```bash
   git clone [URL of your repository]
   cd db_bot
   ```
2. **Install Dependencies:**
   - This project uses Poetry for dependency management.
     ```shell
     poetry install
     ```

3. **ChromeDriver Setup:**
   - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) matching your Chrome version.
   - Extract and place `chromedriver` in a known directory.

4. **Environment Variables:**
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```
     CHROME_DRIVER_PATH=/path/to/chromedriver
     CHROME_PATH=/path/to/chrome
     PROFILE_NAME=YourChromeProfileName
     ```
   - Replace `/path/to/chromedriver` with the actual path to ChromeDriver.
   - Replace `/path/to/chrome` with the actual path to Chrome.
   - `PROFILE_NAME` is your Chrome user profile name.

5. **Configure the Script:**
   - Check and modify `config.py` as needed.
     - Set developer mode, swipe limits, etc.

## Usage

1. **Account and Safety:**
   - It's recommended to use a new Bumble account and a VPN for anonymity.
   - Logging information is saved in `app.log` in the project directory.

2. **Running the Bot:**
   - Execute the script:
     ```shell
     python3 -m db_bot.main
     ```
   - Follow the instructions in the console for logging into Bumble and selecting preferences.

3. **Location Spoofing (Optional):**
   - Consider using the Location Guard extension for Chrome to set a custom location.

4. **Monitoring:**
   - Monitor the console for any messages, especially regarding swipe button availability or swipe limits.

## Important Notes

- The script was tested with the current configuration and successfully mined 10k profiles without being blocked.
- Remember to select the correct gender preference in Bumble after starting the bot.

## TODO

- Improve image handling for more accurate data extraction.
- Explore running multiple Selenium instances for parallel processing. Reference: [Reddit Discussion](https://www.reddit.com/r/learnpython/s/5ggJP5QYOi)
