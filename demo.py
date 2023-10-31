"""demo.py"""

import faker
from boxsdk.exception import BoxAPIException
import logging
from app.config import AppConfig

from app.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def demo():
    """
    Simple script to create demo data
    """

    client = get_client(conf)

    # Create a Faker instance
    fake = faker.Faker()

    try:
        # If the folder exists, delete it
        for item in client.folder('0').get_items():
            if item.name == 'Human Resources':
                print(f"Found the human resources folder with id: {item.id}")
                item.delete()
                print(f"Deleted the folder with id: {item.id}")
    except BoxAPIException as e:
        print(f"An error occurred while deleting the 'Human Resources' folder: {e}")

    try:
        # Create 'Human Resources' folder in the root directory
        hr_folder = client.folder('0').create_subfolder('Human Resources')
        # Read the .env file and replace the PARENT_FOLDER_ID line
        with open(".env", "r") as file:
            lines = file.readlines()
        with open(".env", "w") as file:
            for line in lines:
                if line.startswith("PARENT_FOLDER_ID"):
                    file.write(f"PARENT_FOLDER_ID = {hr_folder.id}\n")
                else:
                    file.write(line)
    except BoxAPIException as e:
        print(f"An error occurred while creating the 'Human Resources' folder: {e}")

    try:
        # Create 'employees' folder inside 'Human Resources' folder
        employees_folder = hr_folder.create_subfolder('Employees')
    except BoxAPIException as e:
        print(f"An error occurred while creating the 'employees' folder: {e}")

    # Create employee folders with unique names
    for _ in range(10):
        employee_name = fake.name()  # Generate a unique employee name
        try:
            employee_folder = employees_folder.create_subfolder(employee_name)
            # Create 'personnel' and 'confidential' folders inside each employee folder
            personnel_folder = employee_folder.create_subfolder('Personnel')
            confidential_folder = employee_folder.create_subfolder('Confidential')

             # Upload files to each folder
            for _ in range(5):
                with open('./dummy.pdf', 'rb') as f:
                    personnel_folder.upload_stream(f, fake.file_name(extension='pdf'))
                    confidential_folder.upload_stream(f, fake.file_name(extension='pdf'))
        except BoxAPIException as e:
            print(f"An error occurred while creating folders for employee '{employee_name}': {e}")


if __name__ == "__main__":
    demo()

