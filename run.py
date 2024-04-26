import requests
import os

# Replace with the actual URL of your Flask application
url = "url/process_image"

# Path to the image you want to process
image_path = "./image.png"  # Replace with your actual image path

# Open the image in binary mode
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

# Prepare the multipart form data with the image
files = {'image': (os.path.basename(image_path), image_data)}

# Send the POST request with the image data
response = requests.post(url, files=files)

# Check for successful response
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    for result in data['results']:
        for x in result[0]:
            print(f'{x}', end='')
else:
    print(f"Error processing image: {response.text}")