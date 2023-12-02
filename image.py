import requests
from io import BytesIO
from PIL import Image


def process_image(image_url):
    response = requests.get(image_url, timeout=10)
    if response.status_code == 200:
        # Open the image using BytesIO object
        image = Image.open(BytesIO(response.content))

        # Save the processed image to a BytesIO object
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="JPEG", quality=50)
        img_byte_arr = img_byte_arr.getvalue()

        return img_byte_arr
    return None
