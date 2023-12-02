import io
import os
from PIL import Image

from models import MainInformationModel, ImagesModel, get_session

# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the 'data' folder
data_folder_path = os.path.join(script_dir, "data")

# Ensure the 'data' folder exists, create if it doesn't
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

# Specify the database file within the 'data' folder
db_file_path = os.path.join(data_folder_path, "database.db")

# Create a session
session = get_session(db_file_path)

new_record = MainInformationModel(name="John Doe", age=30, description="Sample description")
session.add(new_record)
session.commit()

result = session.query(MainInformationModel).filter_by(name="John Doe").first()
print(result.name, result.age, result.description)


# Close the session when done
session.close()
