# May you find the light you're looking for. 

import requests
import json
from datetime import datetime
from tqdm import tqdm
from PIL import Image
import glob
import shutil
from io import BytesIO
import os

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

def download_aurora_frames(json_url, output_folder):
    # Step 1: Fetch JSON data
    response = requests.get(json_url)
    response.raise_for_status()
    data = response.json()
    # print(data)


    # Step 2: Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Step 3: Loop through each image entry
    with tqdm(total=len(data), desc="Downloading images") as pbar:
        for entry in data:
            # Step 4: Fetch image data
            image_url = entry['url']
            image_url = "https://services.swpc.noaa.gov" + image_url
            time_tag = entry['time_tag']

            # Step 5: Format time_tag for a valid filename
            timestamp = datetime.fromisoformat(time_tag.replace("Z","+00:00"))
            filename = timestamp.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

            # Step 6: Save image data
            try:
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                image_path = os.path.join(output_folder, filename)
                with open(image_path, 'wb') as file:
                    file.write(img_response.content)
                pbar.update(1)
            except requests.RequestException as e:
                print(f"Failed to Download {image_path}: {e}")
                pbar.update(1)

    print("Download complete.")

def resize_images(input_folder, output_folder, size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_paths = sorted(glob.glob(f"{input_folder}/*.jpg"))
    if not image_paths:
        print(f"No images found in {input_folder}")
        return

    for image_path in tqdm(image_paths, desc="Resizing images", unit="images"):
        try:
            img = Image.open(image_path)
            img = img.resize(size)
            output_path = os.path.join(output_folder, os.path.basename(image_path))
            img.save(output_path)
        except Exception as e:
            print(f"Failed to resize {image_path}: {e}")

def create_gif_from_frames(input_folder, output_folder,display_folder, output_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    frames = []
    image_paths = sorted(glob.glob(f"{input_folder}/*.jpg"))
    if not image_paths:
        print(f"No images found in {input_folder}")
        return
    
    for image_paths in tqdm(image_paths, desc="Loading images",unit="images"):
        try:
            frames.append(Image.open(image_paths))
        except Exception as e:
            print(f"Failed to load {image_paths}: {e}")

    output_path = os.path.join(output_folder, output_file)

    print(f"Saving GIF to {output_path}, this takes about 3 minutes")
    try:
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
        print(f"GIF saved as {output_path}")
    except Exception as e:
        print(f"Failed to save GIF: {e}")

    try:
        shutil.copy(output_path, display_folder)
        print(f"GIF copied to {display_folder}")
    except Exception as e:
        print(f"Failed to copy GIF: {e}")

clear_folder("/home/wskwok1999/Documents/Python_Scripts/aurora_north_images")
clear_folder("/home/wskwok1999/Documents/Python_Scripts/aurora_south_images")
clear_folder("/home/wskwok1999/Documents/Python_Scripts/aurora_north_gif_gen")
clear_folder("/home/wskwok1999/Documents/Python_Scripts/aurora_south_gif_gen")

north_json_url = "https://services.swpc.noaa.gov/products/animations/ovation_north_24h.json"
south_json_url = "https://services.swpc.noaa.gov/products/animations/ovation_south_24h.json"
north_img_output_folder = "/home/wskwok1999/Documents/Python_Scripts/aurora_north_images"
south_img_output_folder = "/home/wskwok1999/Documents/Python_Scripts/aurora_south_images"

north_gif_output_folder = "/home/wskwok1999/Documents/Python_Scripts/aurora_north_gif_gen"
south_gif_output_folder = "/home/wskwok1999/Documents/Python_Scripts/aurora_south_gif_gen"

north_gif_display_folder = "/home/wskwok1999/Documents/Python_Scripts/aurora_north_gif_display"
south_gif_display_folder = "/home/wskwok1999/Documents/Python_Scripts/aurora_south_gif_display"

download_aurora_frames(north_json_url, north_img_output_folder)
download_aurora_frames(south_json_url, south_img_output_folder)

resize_images(north_img_output_folder, north_img_output_folder, size=(400, 400))
resize_images(south_img_output_folder, south_img_output_folder, size=(400, 400))

create_gif_from_frames(north_img_output_folder, north_gif_output_folder, north_gif_display_folder, "aurora_north.gif")
create_gif_from_frames(south_img_output_folder, south_gif_output_folder, south_gif_display_folder, "aurora_south.gif")