import requests
from bs4 import BeautifulSoup
import torch
import io
# Replace this with your Google Drive file's sharing link
google_drive_link = "https://drive.google.com/file/d/1--sExrC6ZUDpqwrnwB-X6YRuvdh4jnOJ/view?usp=drive_link"

# Extract the file ID from the sharing link
file_id = google_drive_link.split("/file/d/")[1].split("/")[0]

# Construct the download link
download_link = f"https://drive.google.com/uc?id={file_id}"

# Send a GET request to the download link
response = requests.get(download_link)

if response.status_code == 200:
    # Check if the warning page is displayed
    if "virus scan warning" in response.text.lower():
        # Extract the confirmation token from the warning page
        soup = BeautifulSoup(response.text, 'html.parser')
        confirm_token = soup.find('form', {'id': 'download-form'}).input['value']

        # Construct the download URL with the confirmation token
        download_url = f"https://drive.google.com/uc?id={file_id}&confirm={confirm_token}"

        # Send another GET request to download the file
        response = requests.get(download_url)

    if response.status_code == 200:
        state_dict = torch.load(io.BytesIO(response.content), map_location='cuda')

        # Specify the local file name to save the downloaded content
        local_file_name = "model.pth"  # Replace with the desired file name and extension
        with open(local_file_name, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded as {local_file_name}")
    else:
        print("Failed to download the file.")
else:
    print("Failed to access the download link.")
