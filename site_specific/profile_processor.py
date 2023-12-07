import time
import json

from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from db_bot.utils.logging import logging
from db_bot.site_specific.badges_dict import badges_dict


class ProfileProcessor:
    def __init__(self, config: dict, driver: webdriver.Chrome) -> None:
        self.config = config
        self.driver = driver
        self.prev_url = set()

    def get_name(self) -> Optional[str]:
        try:
            name_elements = self.driver.find_elements(By.CLASS_NAME, "encounters-story-profile__name")
            if name_elements:
                return name_elements[0].get_attribute("textContent")
            else:
                logging.warning("Name not found.") if self.config["dev"] else None
                return None
        except Exception as e:
            logging.error(f"Error in get_name: {e}")
            return None

    def get_age(self) -> Optional[int]:
        try:
            age_elements = self.driver.find_elements(By.CLASS_NAME, "encounters-story-profile__age")
            if age_elements:
                age = age_elements[0].get_attribute("textContent")
                # site specific
                age = age.replace(",", "")
                return int(age)
            else:
                logging.warning("Age not found.") if self.config["dev"] else None
                return None
        except Exception as e:
            logging.error(f"Error in get_age: {e}")
            return None

    def get_city(self) -> Optional[str]:
        try:
            city_elements = self.driver.find_elements(By.CSS_SELECTOR, ".location-widget__town")
            if city_elements:
                return city_elements[0].get_attribute("textContent")
            else:
                logging.warning("City not found.") if self.config["dev"] else None
                return None
        except Exception as e:
            logging.error(f"Error in get_city: {e}")
            return None

    def get_education(self) -> Optional[str]:
        try:
            education_elements = self.driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__education")
            if education_elements:
                return education_elements[0].get_attribute("textContent")
            else:
                logging.warning("Education not found.") if self.config["dev"] else None
                return None
        except Exception as e:
            logging.error(f"Error in get_education: {e}")
            return None

    def get_occupation(self) -> Optional[str]:
        try:
            occupation_elements = self.driver.find_elements(By.CSS_SELECTOR, ".encounters-story-profile__occupation")
            if occupation_elements:
                return occupation_elements[0].get_attribute("textContent")
            else:
                logging.warning("Occupation not found.") if self.config["dev"] else None
                return None
        except Exception as e:
            logging.error(f"Error in get_occupation: {e}")
            return None

    def get_description(self) -> Optional[str]:
        try:
            description_elements = self.driver.find_elements(By.CLASS_NAME, "encounters-story-about__text")
            if description_elements:
                return description_elements[0].get_attribute("textContent")
            else:
                logging.warning("Description not found.") if self.config["dev"] else None
                return None
        except Exception as e:
            logging.error(f"Error in get_description: {e}")
            return None

    def get_verification(self) -> bool:
        verification_elements = self.driver.find_elements(By.CLASS_NAME, "encounters-story-profile__verification")
        return bool(verification_elements)

    def get_lives_in_(self) -> tuple[Optional[str], Optional[str]]:
        lives_in_ = None
        try:
            pill_titles = self.driver.find_elements(By.CLASS_NAME, "pill__title")
            for title in pill_titles:
                text = title.get_attribute("textContent")
                if "Lives in" in text:
                    lives_in_ = text.replace("Lives in ", "")
            if lives_in_ is None:
                logging.warning("Lives in not found.") if self.config["dev"] else None
            return lives_in_
        except Exception as e:
            logging.error(f"Error in lives_in_: {e}")
            return lives_in_

    def get_from_(self) -> Optional[str]:
        from_ = None
        try:
            pill_titles = self.driver.find_elements(By.CLASS_NAME, "pill__title")
            for title in pill_titles:
                text = title.get_attribute("textContent")
                if "From" in text:
                    from_ = text.replace("From ", "")
            if from_ is None:
                logging.warning("From not found.") if self.config["dev"] else None
            return from_
        except Exception as e:
            logging.error(f"Error in get_from_: {e}")
            return from_

    def get_images(self) -> list[str]:
        image_urls = set()
        try:
            image_elements = self.driver.find_elements(By.CLASS_NAME, "media-box__picture-image")
            for image in image_elements:
                src = image.get_attribute("src")
                if src not in self.prev_url:
                    image_urls.add(src)

            if not image_urls:
                logging.warning("No images found.") if self.config["dev"] else None

            self.prev_url = image_urls
            return list(image_urls)

        except Exception as e:
            logging.error(f"Error in get_images: {e}")
            self.prev_url = image_urls
            return list(image_urls)

    def get_badges(self) -> dict:
        badge_info = {
            "height": None,
            "exercise": None,
            "education": None,
            "drinking": None,
            "smoking": None,
            "intentions": None,
            "family_plans": None,
            "star_sign": None,
            "politics": None,
            "religion": None,
            "cannabis": None,
            "gender": None,
        }

        if len(badge_info) != len(badges_dict):
            raise ValueError("badges_dict and badge_info must have the same length.")

        try:
            badge_elements = self.driver.find_elements(By.CLASS_NAME, "encounters-story-about__badge")
            for badge in badge_elements:
                image = badge.find_element(By.CLASS_NAME, "pill__image")
                image_src = image.get_attribute("src").split("/")[-1]
                image_alt = image.get_attribute("alt")

                if image_src not in badges_dict:
                    logging.error(f"Unknown badge: {image_alt}")
                else:
                    badge_info[badges_dict[image_src]] = image_alt

            if not any(badge_info.values()):
                logging.warning("No badges found.") if self.config["dev"] else None
            return badge_info
        except Exception as e:
            logging.error(f"Error in get_badges: {e}")
            return badge_info

    def is_finish(self) -> bool:
        try:
            box_texts = self.driver.find_elements(By.CLASS_NAME, "cta-box__text")
            for box_text in box_texts:
                if (
                    "Come back later or try adjusting your filters to see more amazing bees in your area."
                    in box_text.get_attribute("textContent")
                ):
                    return True
            return False
        except NoSuchElementException:
            return False

    def click_button(self) -> None:
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, "[data-qa-role='encounters-action-dislike']")
            button.click()
        except NoSuchElementException:
            input("No button found. Press enter to continue...")
        except Exception as e:
            logging.error(f"Error in click_button: {e}")
            return None

    def fake_scroll(self, times: int, sleep_time: float) -> None:
        body = self.driver.find_element(By.TAG_NAME, "body")
        for _ in range(times):
            time.sleep(sleep_time)
            body.send_keys(Keys.ARROW_DOWN)
