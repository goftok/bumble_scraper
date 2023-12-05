import os
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from db_bot.utils.logging import logging


class DriverManager:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.driver = None
        self.start_driver()

    def start_driver(self) -> webdriver.Chrome:
        # Initialize the chrome options
        chrome_options = webdriver.ChromeOptions()

        logging.info(f"Using Chrome path: {self.config['chrome_path']}")
        logging.info(f"Using Profile name: {self.config['profile_name']}")

        chrome_options.add_argument(f"--user-data-dir={self.config['chrome_path']}")
        chrome_options.add_argument(f"--profile-directory={self.config['profile_name']}")

        logging.info(f"Using Chrome driver path: {self.config['chrome_driver_path']}")
        # Initialize the chrome service
        chrome_service = Service(executable_path=self.config["chrome_driver_path"])

        # Initialize the webdriver
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def load_cookies(self, location: str):
        if os.path.exists(location):
            with open(location, "rb") as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

    def get_url(self, url: str):
        self.driver.get(url)

    def save_cookies(self, location: str):
        with open(location, "wb") as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def close_driver(self):
        self.driver.close()
