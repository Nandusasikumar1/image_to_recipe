from torch.utils.data import Dataset, DataLoader
import glob
from PIL import Image
import torch
from transformers import AutoProcessor, BlipForConditionalGeneration

# import transformers

# print(transformers.__version__)
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
# model.load_state_dict(torch.load('model.pth'))
# model.to(device)
import requests
from bs4 import BeautifulSoup
import torch
import io

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
        model.load_state_dict(torch.load(io.BytesIO(response.content)))


def recipe_name_generator(img):

        pil_img = Image.open(img)
        inputs = processor(images=pil_img, return_tensors="pt").to(device)
        pixel_values = inputs.pixel_values
     
        generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
        generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_caption



# name = recipe_name_generator(r"C:\project_c\image_scrapping\items_scrapped_train\4 layer vanillachocolate raspberry bars2.jpg")
# print(name)

