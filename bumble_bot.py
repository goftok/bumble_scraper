import os

from db_bot.utils.logging import logging
from db_bot.drivers.chrome_driver import DriverManager
from db_bot.database_utils.db_manager import DatabaseManager
from db_bot.site_specific.profile_processor import ProfileProcessor


class BumbleBot:
    def __init__(self, config):
        self.config = config
        self.cookies_path, self.main_db_path, self.image_db_path = self.get_paths()
        self.driver_manager = DriverManager(config)
        self.profile_processor = ProfileProcessor(config, self.driver_manager.driver)
        self.db_manager = DatabaseManager(config, self.profile_processor, self.main_db_path, self.image_db_path)

    def get_paths(self) -> tuple:
        base_path = os.path.dirname(os.path.realpath(__file__))
        cookies_path = os.path.join(base_path, self.config["cookies_file_name"])
        main_db_path = os.path.join(base_path, self.config["main_db_name"])
        image_db_path = os.path.join(base_path, self.config["image_db_name"])

        logging.info(f"Using cookies path: {cookies_path}")
        logging.info(f"Using main db path: {main_db_path}")
        logging.info(f"Using image db path: {image_db_path}")

        return cookies_path, main_db_path, image_db_path

    def run(self):
        logging.info("Starting Bumble bot...")
        logging.info("Configuration:")
        logging.info(self.config)

        self.driver_manager.load_cookies(self.cookies_path)
        self.driver_manager.get_url(self.config["bumble_path"])

        logging.info("Please login to Bumble")
        input("Press enter to continue when you will be on a scroll page...")

        gender_input = input("Select gender: 0 - male, 1 - female, 2 - non-binary, 3 - other: ")

        continue_running = True

        while self.config["limit"] > 0 and continue_running:
            try:
                logging.info("Starting to process number " + str(self.config["limit"]), style="bold green")

                self.driver_manager.driver.implicitly_wait(self.config["implicitly_wait"])
                self.profile_processor.fake_scroll()
                self.db_manager.save_profile(int(gender_input))

                input("Press enter to continue...") if self.config["dev"] else None

                self.profile_processor.click_button()
                self.config["limit"] -= 1
            except Exception as e:
                logging.error(f"Error fetching profile: {e}", style="bold red")
                continue_running = False

        self.driver_manager.save_cookies(self.cookies_path)
        self.db_manager.close_sessions()
        self.driver_manager.close_driver()
