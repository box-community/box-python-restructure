import logging
from app.config import AppConfig
from boxsdk.exception import BoxAPIException
from app.box_client import get_client
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()

def main(parent_folder_id, folder_name, subfolder_names):
    """
    Simple script to demonstrate how to restructure a folder tree
    """

    # Load variables from .env
    load_dotenv()

    client = get_client(conf)

    try:
        # Get folder object of parent_folder_id
        parent_folder = client.folder(folder_id=parent_folder_id).get()
    except BoxAPIException as e:
        print(f"Error getting parent folder: {e}")
        return

    # Iterate over the items in the parent folder
    for item in client.folder(folder_id=parent_folder.id).get_items():
        if item.name == folder_name:
            target_folder = item

            # Create subfolders under target_folder
            subfolder_parents = create_subfolders(client, target_folder, subfolder_names)

            # Iterate over all items in target_folder
            for item in client.folder(folder_id=target_folder.id).get_items():
                if item.type == 'folder' and item.name not in subfolder_names:  # this is a target subfolder
                    target_subfolder = item

                    # Move and rename folders
                    move_and_rename_folders(client, subfolder_parents, target_subfolder)

                    # Delete the original target subfolder after moving its contents
                    delete_original_folder(client, target_subfolder)


def create_subfolders(client, target_folder, subfolder_names):
    subfolder_parents = {}
    for name in subfolder_names:
        try:
            subfolder_parent = client.folder(target_folder.id).create_subfolder(name)
            subfolder_parents[name] = subfolder_parent
        except BoxAPIException as e:
            print(f"Error creating '{name}' folder: {e}")
            return None

    return subfolder_parents


def move_and_rename_folders(client, subfolder_parents, target_subfolder):
    for item in client.folder(folder_id=target_subfolder.id).get_items():
        if item.type == 'folder' and item.name in subfolder_parents.keys():
            move_and_rename(client, item, subfolder_parents[item.name], target_subfolder.name)


def move_and_rename(client, folder_to_move, parent_folder, new_name):
    try:
        client.folder(folder_to_move.id).move(parent_folder=parent_folder, name=new_name)
    except BoxAPIException as e:
        print(f"An error occurred while moving folders: {e}")


def delete_original_folder(client, folder_to_delete):
    try:
        client.folder(folder_to_delete.id).delete()
    except BoxAPIException as e:
        print(f"Error deleting '{folder_to_delete.name}' folder: {e}")


if __name__ == "__main__":
    parent_folder_id = os.getenv("PARENT_FOLDER_ID")
    folder_name = 'Employees'
    subfolder_names = ['Personnel', 'Confidential']
    
    main(parent_folder_id, folder_name, subfolder_names)
