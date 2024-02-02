import cv2
import os
import shutil
import time
import subprocess
import re
import shlex

SCALE_FACTOR = 9

class ImageProcessor:
    DEFAULT_IMAGE_FORMAT = ".png"
    INTERPOLATION_METHOD = cv2.INTER_AREA

    @staticmethod
    def read_image(image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise IOError(f"Could not open or find the image {image_path}.")
        return image

    @staticmethod
    def resize_image(image, scale_factor):
        new_width = int(image.shape[1] * scale_factor)
        new_height = int(image.shape[0] * scale_factor)
        return cv2.resize(image, (new_width, new_height), interpolation=ImageProcessor.INTERPOLATION_METHOD)

    @staticmethod
    def save_image(image, image_path, format=DEFAULT_IMAGE_FORMAT):
        base, _ = os.path.splitext(image_path)
        new_path = f"{base}_resized{format}"
        cv2.imwrite(new_path, image)
        return new_path

    @staticmethod
    def convert_to_jpg(image_path):
        file_name, ext = os.path.splitext(image_path)
        if ext.lower() in ['.jpeg', '.png', '.bmp']:
            output_file = f"{file_name}.jpg"
            subprocess.run(["convert", image_path, output_file], check=True)
            return output_file
        return image_path

def process_image(file_path, scale_factor=SCALE_FACTOR):
    try:
        image = ImageProcessor.read_image(file_path)
        resized_image = ImageProcessor.resize_image(image, scale_factor)
        resized_image_path = ImageProcessor.save_image(resized_image, file_path)
        converted_image_path = ImageProcessor.convert_to_jpg(resized_image_path)
        print(f"Processed {file_path}: Resized to {resized_image_path}, Converted to {converted_image_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

watched_directory = os.path.dirname(os.path.realpath(__file__))

def find_min_missing_folder_number(path):
    existing_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    folder_numbers = set()
    for folder in existing_folders:
        match = re.match(r"(\d+)", folder)
        if match:
            folder_numbers.add(int(match.group(1)))

    missing_number = 1
    while missing_number in folder_numbers:
        missing_number += 1

    return missing_number

def create_folder_and_move_image(image_path, folder_counter):
    file_name = os.path.basename(image_path)
    folder_name = f"{folder_counter}. {os.path.splitext(file_name)[0]}"
    new_folder_path = os.path.join(watched_directory, folder_name)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    new_image_path = os.path.join(new_folder_path, file_name)
    shutil.move(image_path, new_image_path)
    process_image(new_image_path)

    # Создание текстового файла "Описание.txt" в папке
    description_file_path = os.path.join(new_folder_path, "Описание.json")
    with open(description_file_path, 'w') as description_file:
        description_file.write("")

existing_files = set(os.listdir(watched_directory))

while True:
    current_files = set(os.listdir(watched_directory))
    new_files = current_files - existing_files

    for file in new_files:
        full_file_path = os.path.join(watched_directory, file)
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            folder_counter = find_min_missing_folder_number(watched_directory)
            create_folder_and_move_image(full_file_path, folder_counter)

    existing_files = current_files
    time.sleep(5)
