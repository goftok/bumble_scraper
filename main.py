import os
import json
import time
import requests

from selenium import webdriver
from dotenv import load_dotenv
from rich.console import Console
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from models import MainInformationModel, ImagesModel, Gender, get_session
from cookies import check_and_load_cookies, save_cookies
from image import process_image

load_dotenv()

console = Console()

config = {
    "dev": False,
    "version": "0.3.1",
    "limit": 964,
    "arrow_down": 6,
    "implicitly_wait": 1,
    "time_sleep": 0.30,
}

# Get the path to the chromedriver executable
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
chrome_path = os.getenv("CHROME_PATH")
profile_name = os.getenv("PROFILE_NAME")
bumble_path = r"https://bumble.com/"

console.print("Starting Bumble bot...", style="bold green")
console.print(f"Chrome driver path: {chrome_driver_path}")
console.print(f"Chrome path: {chrome_path}")
console.print(f"Profile name: {profile_name}")

# Initialize the chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={chrome_path}")
chrome_options.add_argument(f"--profile-directory={profile_name}")

# Initialize the chrome service
chrome_service = Service(executable_path=chrome_driver_path)

# Initialize the webdriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the 'data' folder
data_folder_path = os.path.join(script_dir, "data")

# Ensure the 'data' folder exists, create if it doesn't
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

# Specify the database file within the 'data' folder
db_file_path = os.path.join(data_folder_path, "database0.3.0.db")
cookies_file_path = os.path.join(data_folder_path, "cookies.json")

# Create a session
session = get_session(db_file_path)

# Check if the cookies file exists
check_and_load_cookies(driver, cookies_file_path, bumble_path)

driver.get(bumble_path)

console.print("Please login to Bumble", style="bold yellow")

input("Press enter to continue...")

gender_input = input("Select gender: 0 - male, 1 - female, 2 - non-binary, 3 - other: ")
gender_value = int(gender_input)

# Map the integer value to the corresponding Gender enum
gender_enum = Gender(gender_value)

"""
Some issues with the code (Probelm 1). When we trying to get the image urls, we are getting additional
urla from the previous iteration. TODO
"""
prev_url = set()
image_urls = set()
continue_running = True

while config["limit"] > 0 and continue_running:
    try:
        # wait for the page to load
        console.print("Starting to process number " + str(config["limit"]), style="bold green")

        driver.implicitly_wait(config["implicitly_wait"])

        body = driver.find_element(By.TAG_NAME, "body")
        for i in range(config["arrow_down"]):
            time.sleep(config["time_sleep"])
            body.send_keys(Keys.ARROW_DOWN)

        prev_url = image_urls
        image_urls = set()

        images_divs = driver.find_elements(By.CLASS_NAME, value="media-box__picture-image")
        # Iterate over each story element and find images within
        for image_div in images_divs:
            src = image_div.get_attribute("src")
            # TODO (Probelm 1)
            if src not in prev_url:
                image_urls.add(src)

        name = None
        age = None
        city = None
        lives_in = None
        from_ = None
        education = None
        occupation = None
        description = None
        verification = None
        badge_info = []

        # Extracting name
        name_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__name")
        if name_elements:
            name = name_elements[0].get_attribute("textContent")
        else:
            console.print("NOT FOUND name.", style="bold yellow") if config["dev"] else None

        # Extracting age
        age_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__age")
        if age_elements:
            age_text = age_elements[0].get_attribute("textContent")
            # Remove the comma from the age
            age = age_text.replace(",", "")
        else:
            console.print("NOT FOUND age.", style="bold yellow") if config["dev"] else None

        # Extracting city information
        city_elements = driver.find_elements(By.CSS_SELECTOR, ".location-widget__town")
        if city_elements:
            city = city_elements[0].get_attribute("textContent")
        else:
            console.print("NOT FOUND city.", style="bold yellow") if config["dev"] else None

        # Extracting education information
        education_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__education")
        if education_elements:
            education = education_elements[0].get_attribute("textContent")
        else:
            console.print("NOT FOUND education.", style="bold yellow") if config["dev"] else None

        # Extracting occupation information
        occupation_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__occupation")
        if occupation_elements:
            occupation = occupation_elements[0].get_attribute("textContent")
        else:
            console.print("NOT FOUND occupation.", style="bold yellow") if config["dev"] else None

        # Extracitnd description
        description_elements = driver.find_elements(By.CLASS_NAME, "encounters-story-about__text")
        if description_elements:
            description = description_elements[0].get_attribute("textContent")
        else:
            console.print("NOT FOUND description.", style="bold yellow") if config["dev"] else None

        # Extracting verification
        verification_elements = driver.find_elements(By.CLASS_NAME, "encounters-story-profile__verification")
        if verification_elements:
            verification = True
        else:
            verification = False
            console.print("NOT FOUND verification.", style="bold yellow") if config["dev"] else None

        pill_titles = driver.find_elements(By.CLASS_NAME, "pill__title")
        for title in pill_titles:
            text = title.get_attribute("textContent")
            if "Lives in" in text:
                lives_in = text.replace("Lives in ", "")
            if "From" in text:
                from_ = text.replace("From ", "")

        console.print("NOT FOUND lives_in.", style="bold yellow") if config["dev"] and not lives_in else None

        # Extract badges
        badge_elements = driver.find_elements(By.CLASS_NAME, "encounters-story-about__badge")

        # Iterate over each badge element
        for badge in badge_elements:
            # Find the image within the badge and get its 'alt' attribute
            image = badge.find_element(By.CLASS_NAME, "pill__image")
            image_alt = image.get_attribute("alt")
            image_src = image.get_attribute("src")

            # Add the extracted information to the list
            badge_info.append({"image_src": image_src, "image_alt": image_alt})

        if not badge_info:
            console.print("No badges found.", style="bold red") if config["dev"] else None

        badge_info_json = json.dumps(badge_info)

        # Add new main information record
        new_record = MainInformationModel(
            gender=gender_enum,
            name=name,
            age=age,
            city=city,
            lives_in=lives_in,
            from_=from_,
            education=education,
            occupation=occupation,
            description=description,
            verification=verification,
            badges=badge_info_json,
            script_version=config["version"],
        )

        session.add(new_record)
        session.commit()

        # Now new_record has an id assigned by the database
        main_info_id = new_record.id

        for img_url in image_urls:
            try:
                proccessed_image = process_image(img_url)

                if proccessed_image:
                    image_record = ImagesModel(
                        main_info_id=main_info_id,
                        image_data=proccessed_image,
                        image_link=img_url,
                    )

                    session.add(image_record)
                else:
                    console.print(f"Error fetching image from {img_url}", style="bold red")

            except requests.RequestException as e:
                console.print(f"Error fetching image from {img_url}: {e}", style="bold red")

        session.commit()

        input("Press enter to continue...") if config["dev"] else None

        # Click the button
        try:
            button = driver.find_element(By.CSS_SELECTOR, "[data-qa-role='encounters-action-dislike']")
            button.click()
        except NoSuchElementException:
            input("No button found. Press enter to continue...")

        if config["dev"] and input("Press q to quit, any other key to continue: ") == "q":
            break

        config["limit"] -= 1

    except KeyboardInterrupt:
        # This block executes when a KeyboardInterrupt (Ctrl+C) occurs
        print("Interrupt received, stopping...")
        continue_running = False

# Save the cookies
save_cookies(driver, cookies_file_path)

# Close the session when done
session.close()
