from db_bot.utils.logging import logging
from db_bot.utils.process_image import process_image
from db_bot.site_specific.profile_processor import ProfileProcessor
from db_bot.models import Gender, MainInformationModel, ImagesModel, get_session


class DatabaseManager:
    def __init__(self, config: dict, profile_processor: ProfileProcessor, main_db_path: str, image_db_path: str):
        self.config = config
        self.profile_processor = profile_processor
        self.main_session, self.image_session = get_session(main_db_path, image_db_path)

    def _save_images(self, profile_id: int) -> None:
        images_urls = self.profile_processor.get_images()
        for url in images_urls:
            try:
                image_data = process_image(url)

                if not image_data:
                    logging.error(f"Error fetching image from {url}", style="bold red")
                    continue

                new_record = ImagesModel(
                    main_info_id=profile_id,
                    image_data=image_data,
                    image_link=url,
                )

                self.image_session.add(new_record)
                self.image_session.commit()

            except Exception as e:
                logging.error(f"Error fetching image from {url}: {e}", style="bold red")

    def save_profile(self, gender_value: int) -> None:
        gender_enum = Gender(gender_value)

        # Add new main information record
        new_record = MainInformationModel(
            gender=gender_enum,
            name=self.profile_processor.get_name(),
            age=self.profile_processor.get_age(),
            city=self.profile_processor.get_city(),
            lives_in=self.profile_processor.get_lives_in_(),
            from_=self.profile_processor.get_from_(),
            education=self.profile_processor.get_education(),
            occupation=self.profile_processor.get_occupation(),
            description=self.profile_processor.get_description(),
            verification=self.profile_processor.get_verification(),
            badges=self.profile_processor.get_badges(),
            script_version=self.config["version"],
        )

        self.main_session.add(new_record)
        self.main_session.commit()

        self._save_images(new_record.id)

    def close_sessions(self):
        self.main_session.close()
        self.image_session.close()
