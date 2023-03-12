import filecmp
import hashlib
import logging
import os
import shutil
import sys
from apscheduler.schedulers.background import BackgroundScheduler

src_folder_path = input("Enter Source Folder Path: ")
replica_folder_path = input("Enter Replica Folder Path: ")
path = '/Users/Josef/Projects/SycnTwoFolderWithPython/'

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s (%(levelname)s) : %(message)s",
                    filemode="w")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.info("synchronisation has started .....")


def rewrite_file(src_path, des_path, file, user_message):
    try:
        shutil.copy(src_path, des_path)
        logging.info(user_message + " " + file + " is done successfully in " + des_path)
    except ValueError:
        logging.info(user_message + file + " in " + des_path + "didn't happened with an exception, please check again!")


def calculate_md5(src_path):
    try:
        hasher = hashlib.md5()
        with open(src_path, 'rb') as open_file:
            content = open_file.read()
            hasher.update(content)
        return hasher.hexdigest()
    except NotADirectoryError as e:
        logging.info(" An Error:", e, "\n Please try again!")


def create_report():
    comparison = filecmp.dircmp(src_folder_path, replica_folder_path)
    source_files = ','.join(comparison.left_only)
    replica_files = ','.join(comparison.right_only)

    common_files = ','.join(comparison.common)
    logging.info("\n\n Report To check Unmatched Folders/Files.\n")
    logging.info("Common Files : \n" + common_files + "\n")
    logging.info("\n Source File contains : \n" + source_files + "\n")
    logging.info("\n Replica Folder contains :\n" + replica_files + "\n")


# This Check Fun will check the Content of the file after Copying/Creating to confirm that no changing after the
# process is done.
def check_content(src_path, des_path, file, user_message):
    if calculate_md5(src_path) != calculate_md5(des_path + '/' + file):
        logging.info("The Content of " + file + " has changed by some one 'Hacker' during " + user_message
                     + " the file, ReWrite the file in progress.")
        rewrite_file(src_path, des_path, file, user_message)


def remove_unmatched_files(des_path, src_path):
    for folders, subFolders, items in os.walk(des_path):
        for item in items:
            src_path_replaced = folders.replace(des_path, src_path)
            src_file_path = src_path_replaced + '/' + item
            des_file_path = folders + '/' + item
            if not (os.path.exists(src_file_path)):
                os.remove(des_file_path)
                logging.info(item + " has Removed from " + folders)


def remove_unmatched_dirs(des_path, src_path):
    for folders, sub_folders, items in os.walk(des_path):
        src_file_path = folders.replace(des_path, src_path)
        for folder in sub_folders:
            try:
                if not os.path.exists(src_file_path + '/' + folder):
                    shutil.rmtree(folders + '/' + folder)
                    logging.info(folder + " has Removed from " + folders)
                else:
                    continue
            except FileNotFoundError:
                logging.info("An Error with removing " + folders)


# Create a Message box:
def message_box(user_message):
    system_event = '"System Events"'
    title = '"synchronisation Process"'
    os.system("osascript -e " +
              '\'Tell application {0} to display dialog {1} with title {2}\''.format(system_event, user_message, title))


# Copy the content of the first file in
def select_items(src_path, des_path):
    for dirs, sub_dirs, files in os.walk(src_path):
        for subdir in sub_dirs:
            des_sub_dir_path_replaced = dirs.replace(src_path, des_path)
            try:
                os.mkdir(des_sub_dir_path_replaced + '/' + subdir)
                logging.info("The " + subdir + " has Created in " + des_sub_dir_path_replaced)
            except:
                logging.info("The Folder " + subdir + " is already in " + des_sub_dir_path_replaced)

        for file in files:
            des_file_path_replaced = dirs.replace(src_path, des_path)
            src_file_path = dirs + '/' + file
            des_file_path = des_file_path_replaced + '/' + file
            if os.path.exists(des_file_path):
                if calculate_md5(src_file_path) != calculate_md5(des_file_path):
                    logging.info("The Content of " + file +
                                 " has changed in the SourceFolder so it's going to Copy the updates.")
                    rewrite_file(src_file_path, des_file_path_replaced, file, "Copying")
                    check_content(src_file_path, des_file_path_replaced, file, "Copying")

                else:
                    logging.info(file + " is already in " + des_file_path_replaced + " with all contents")
                    check_content(src_file_path, des_file_path_replaced, file, "Copying")
            else:
                rewrite_file(src_file_path, des_file_path_replaced, file, "Creating")
                check_content(src_file_path, des_file_path_replaced, file, "Creating")

    remove_unmatched_files(des_path, src_path)
    remove_unmatched_dirs(des_path, src_path)
    create_report()


def starter():
    try:
        if not os.path.exists(src_folder_path) or not os.path.exists(replica_folder_path):
            logging.error("Source Folder Path/ Replica Folder Path doesn't exist, please check them again!")
            message_box('"The paths you have provided are not correct \n Please check and try again!"')
        else:
            select_items(src_folder_path, replica_folder_path)
            logging.info("The synchronization process has been done successfully")
            message_box('"synchronisation process has been done successfully !'
                        '\n please check log.txt to see all details."')

    except FileNotFoundError as e:
        logging.info("These is an Error: ", e)
        message_box('"Error {}"'.format(e))


starter()
scheduler: BackgroundScheduler = BackgroundScheduler()
scheduler.add_job(starter, 'interval', seconds=3600, end_date="2023-03-10 00:00:00")
scheduler.start()


