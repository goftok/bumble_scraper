import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "dev": False,  # True if you want to run the bot in dev mode
    "version": "0.4.3",  # Version of the bot
    "limit": 10000,  # Number of profiles to swipe
    "scroll_times": 6,  # Number of times to scroll down (for loading images)
    "scroll_sleep_time": 0.30,  # Time to sleep between scrolls
    "implicitly_wait": 1,  # Time to wait for the page to load
    "main_db_name": "data/main.db",  # Name of the main database
    "image_db_name": "data/image.db",  # Name of the image database
    "cookies_file_name": "data/cookies.json",  # Name of the cookies file
    "chrome_driver_path": os.getenv("CHROME_DRIVER_PATH"),  # Path to the chrome driver
    "chrome_path": os.getenv("CHROME_PATH"),  # Path to chrome
    "profile_name": os.getenv("PROFILE_NAME"),  # Name of the chrome profile
    "bumble_path": r"https://bumble.com/",  # Bumble URL
}
