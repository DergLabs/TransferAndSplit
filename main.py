# Written by Dragon Enjoyer
# Goal of this program is to access SD Card and split JPEG and RAW files into their own folders one at a time

import os
import shutil
import logging
from time import sleep
from tqdm import tqdm

revision = "1.1.0"  # <-- Update me every time a change is made

USER_PATH = os.path.expanduser('~')

JPEG_EXTENSION = ".JPG"
RAW_EXTENSION = ".RAF"


def validate_input(userinput, type):
    if type == "exit":
        while True:
            try:
                if userinput == "Y" or userinput == "N":
                    break
                else:
                    print("Invalid input.")
                    userinput = input("Exit?: Y/N")
            except:
                print("Invalid input.")

    elif type == "filename":
        while True:
            try:
                if userinput in available_folders:
                    return userinput
                    break
                else:
                    print("No folders match that name")
                    userinput = input("Enter name of fuji folder to transfer files from: ")
                    userinput = userinput.upper()
            except:
                print("Invalid input")


def transfer_jpeg(jpeg_total_size, jpeg_file_size, SD_PATH, JPEG_FOLDER_PATH):
    with tqdm(desc="JPG Transfer Progress", total=jpeg_total_size, initial=0, unit="B", unit_divisor=1024, leave=True,
              unit_scale=True) as jpg_progress:
        for i, file_name in enumerate(selected_jpg):
            shutil.copy(os.path.join(SD_PATH, file_name), JPEG_FOLDER_PATH)
            jpg_progress.update(jpeg_file_size)


def transfer_raw(raw_total_size, raw_file_size, SD_PATH, RAW_FOLDER_PATH):
    with tqdm(desc="RAW Transfer Progress", total=raw_total_size, initial=0, unit="B", unit_divisor=1024, leave=True,
              unit_scale=True) as raw_progress:
        for i, file_name in enumerate(selected_raw):
            shutil.copy(os.path.join(SD_PATH, file_name), RAW_FOLDER_PATH)
            raw_progress.update(raw_file_size)


if __name__ == '__main__':
    print("Written By: Dragon Enjoyer :3")
    print("Program Version: {}\n".format(revision))

    jpg_folder_name = input("Enter Folder name for JPEG's: ")
    raw_folder_name = input("Enter Folder name for RAW's: ")

    JPEG_FOLDER_PATH = USER_PATH + "/Desktop/" + jpg_folder_name
    RAW_FOLDER_PATH = USER_PATH + "/Desktop/" + raw_folder_name

    try:  # Check and see if the folders for LDCM and impedance board already exist, if so just keep going on
        os.mkdir(JPEG_FOLDER_PATH)  # Created the directory for the impedance board files
        os.mkdir(RAW_FOLDER_PATH)  # Create the directory for the LDCM measurements
    except OSError as error:
        logging.warning("Filepaths already exist")

    run = True
    while run:
        SD_PATH = "/Volumes/Untitled/DCIM/"
        available_folders = os.listdir(SD_PATH)

        print("Available Folders for File Transfer: {}".format(available_folders))

        fuji_folder_name = input("Enter name of fuji folder to transfer files from: ")
        fuji_folder_name = fuji_folder_name.upper()
        fuji_folder_name = validate_input(fuji_folder_name, "filename")

        SD_PATH = SD_PATH + fuji_folder_name

        sd_files = os.listdir(SD_PATH)

        selected_jpg = [jpg for jpg in sd_files if jpg.endswith(JPEG_EXTENSION)]
        selected_raw = [raw for raw in sd_files if raw.endswith(RAW_EXTENSION)]

        jpeg_cnt = len(selected_jpg)
        raw_cnt = len(selected_raw)

        print("{} JPEG Files".format(jpeg_cnt))
        print("{} RAW Files".format(raw_cnt))

        jpeg_file_size = (os.path.getsize(SD_PATH + "/" + selected_jpg[0]))
        raw_file_size = (os.path.getsize(SD_PATH + "/" + selected_raw[0]))

        jpeg_total_size = (os.path.getsize(SD_PATH + "/" + selected_jpg[0])) * jpeg_cnt
        raw_total_size = (os.path.getsize(SD_PATH + "/" + selected_raw[0])) * raw_cnt

        print("\nTransferring JPG Files")
        transfer_jpeg(jpeg_total_size, jpeg_file_size, SD_PATH, JPEG_FOLDER_PATH)
        print("JPEG File transfer Complete\n")
        sleep(1)

        print("\nTransferring RAW Files")
        transfer_raw(raw_total_size, raw_file_size, SD_PATH, RAW_FOLDER_PATH)
        print("RAW File transfer Complete\n")
        sleep(1)

        leave = input("Exit?: Y/N\n")
        leave = leave.upper()
        validate_input(leave, "exit")
        if leave == "Y":
            break
