import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "dev": False,
    "version": "0.4.0",
    "limit": 964,
    "scroll_times": 6,
    "scroll_sleep_time": 0.30,
    "implicitly_wait": 1,
    "main_db_name": "data/main.db",
    "image_db_name": "data/image.db",
    "cookies_file_name": "data/cookies.json",
    "chrome_driver_path": os.getenv("CHROME_DRIVER_PATH"),
    "chrome_path": os.getenv("CHROME_PATH"),
    "profile_name": os.getenv("PROFILE_NAME"),
    "bumble_path": r"https://bumble.com/",
}
