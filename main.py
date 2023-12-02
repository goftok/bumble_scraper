import os
import json
import requests

from io import BytesIO
from selenium import webdriver
from dotenv import load_dotenv
from rich.console import Console
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from models import MainInformationModel, ImagesModel, Gender, get_session
from cookies import check_and_load_cookies, save_cookies
from image import process_image

load_dotenv()

VERSION = "0.1.0"
LIMIT = 100
console = Console()

# Get the path to the chromedriver executable
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
chrome_profile_path = os.getenv("CHROME_PROFILE_PATH")
bumble_path = r"https://bumble.com/"

console.print("Starting Bumble bot...", style="bold green")
console.print(f"Chrome driver path: {chrome_driver_path}")
console.print(f"Chrome profile path: {chrome_profile_path}")

# Initialize the chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=/Users/goftok/Library/Application Support/Google/Chrome")
chrome_options.add_argument("--profile-directory=Default")

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
db_file_path = os.path.join(data_folder_path, "database.db")
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

while LIMIT > 0:
    # wait for the page to load
    driver.implicitly_wait(4)

    image_urls = []

    images_divs = driver.find_elements(by="class name", value="encounters-album__story")

    # Iterate over each story element and find images within
    for image_div in images_divs:
        images = image_div.find_elements(By.TAG_NAME, "img")
        for image in images:
            src = image.get_attribute("src")

            # Check if the src starts with the desired URL
            if (
                src
                and src.startswith("https://fr1.bumbcdn.com/")
                and not src.startswith("https://fr1.bumbcdn.com/i/big/assets/")
            ):
                image_urls.append(src)

    name, age, city, education, occupation, description, verification = None, None, None, None, None, None, None

    # Extracting name
    name_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__name")
    if name_elements:
        name = name_elements[0].get_attribute("textContent")
    else:
        # console.print("No elements found with the specified class name.", style="bold yellow")
        pass

    # Extracting age
    age_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__age")
    if age_elements:
        age_text = age_elements[0].get_attribute("textContent")

        if "," in age_text:
            age = age_text.replace(",", "")
    else:
        # console.print("No elements found with the specified class age.", style="bold yellow")
        pass

    # Extracting city information
    city_elements = driver.find_elements(By.CSS_SELECTOR, ".location-widget__town")
    if city_elements:
        city = city_elements[0].get_attribute("textContent")
    else:
        # console.print("No elements found with the specified class city.", style="bold yellow")
        pass

    # Extracting education information
    education_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__education")
    if education_elements:
        education = education_elements[0].get_attribute("textContent")
    else:
        # console.print("No elements found with the specified class education.", style="bold yellow")
        pass

    # Extracting occupation information
    occupation_elements = driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__occupation")
    if occupation_elements:
        occupation = occupation_elements[0].get_attribute("textContent")
    else:
        # console.print("No elements found with the specified class occupation.", style="bold yellow")
        pass

    # Extracitnd description
    description_elements = driver.find_elements(By.CLASS_NAME, "encounters-story-about__text")
    if description_elements:
        description = description_elements[0].get_attribute("textContent")
    else:
        # console.print("No elements found with the specified class description.", style="bold yellow")
        pass

    # Extracting verification
    verification_elements = driver.find_elements(By.CLASS_NAME, "encounters-story-profile__verification")
    if verification_elements:
        verification = True
    else:
        verification = False
        # console.print("No elements found with the specified class verification.", style="bold yellow")
        pass

    # Extract badges
    badge_elements = driver.find_elements(By.CLASS_NAME, "encounters-story-about__badge")
    badge_info = []

    # Iterate over each badge element
    for badge in badge_elements:
        # Find the image within the badge and get its 'alt' attribute
        image = badge.find_element(By.CLASS_NAME, "pill__image")
        image_alt = image.get_attribute("alt")
        image_src = image.get_attribute("src")

        # Add the extracted information to the list
        badge_info.append({"image_src": image_src, "image_alt": image_alt})

    if not badge_info:
        # console.print("No badges found.", style="bold red")
        pass

    badge_info_json = json.dumps(badge_info)

    # Add new main information record
    new_record = MainInformationModel(
        gender=gender_enum,
        name=name,
        age=age,
        city=city,
        education=education,
        occupation=occupation,
        description=description,
        verification=verification,
        badges=badge_info_json,
        script_version=VERSION,
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

    # input("Press enter to continue...")

    # Click the button
    button = driver.find_element(By.CSS_SELECTOR, "[data-qa-role='encounters-action-dislike']")
    if not button:
        input("No button found. Press enter to continue...")

    button.click()

    # if input is q then quit
    # if input("Press q to quit, any other key to continue: ") == "q":
    #     break
    LIMIT -= 1


# Save the cookies
save_cookies(driver, cookies_file_path)

# Close the session when done
session.close()
