# ZIPLINE v2
# Authored by Trevor Snodgrass
# Compress Game Files and Redirect Shortcuts in one fowl swoop!
# AR3 U T00N ENUFF?
# 11/2/23

import os
import shutil

# Create error_log.txt if it doesn't exist
if not os.path.exists('error_log.txt'):
    with open('error_log.txt', 'w') as log_file:
        log_file.write("Error Log\n")

def get_game_directory():
    directory = "C:\\Program Files (x86)\\Toontown Rewritten - Copy" #Enter the Main Directory for the Game
    return directory

def get_backup_directory():
    backup_folder = "C:\\Program Files (x86)\\Toontown Rewritten - Backup" # Enter the Backup File Directory/Path/Name
    return os.path.join('C:\\', backup_folder)

def create_backup(game_directory, backup_folder):
    try:
        backup_path = os.path.join(backup_folder, 'backup_game_data.dat')

        if os.path.exists(backup_path):
            os.remove(backup_path)
            print(f"Removed previous backup: {backup_path}")

        if os.path.exists('compressed_game_data.dat'):
            shutil.move('compressed_game_data.dat', backup_path)
            print(f"Moved previous data to backup folder: {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"Error creating backup: {e}\n")

def should_compress_file(file_name):
    excluded_files = ['']  # Replace with actual names or extensions
    return file_name not in excluded_files

def export_compressed_data(data, export_path):
    try:
        with open(export_path, 'wb') as file:
            file.write(data)
        print(f"Data successfully exported to {export_path}.")
    except Exception as e:
        print(f"Error exporting data: {e}")
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"Error exporting data: {e}\n")

def read_files_in_directory(directory):
    binary_data = b''
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if should_compress_file(file_name):
                try:
                    with open(file_path, 'rb') as file:
                        binary_data += file.read()
                except Exception as e:
                    print(f"Error reading file '{file_path}': {e}")
                    with open('error_log.txt', 'a') as log_file:
                        log_file.write(f"Error reading file '{file_path}': {e}\n")
    return binary_data

def edit_shortcut_target(shortcut_path, new_target):
    try:
        with open(shortcut_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if 'TargetPath=' in line:
                    lines[i] = f'TargetPath={new_target}\n'

        with open(shortcut_path, 'w') as file:
            file.writelines(lines)
        
        print(f"Edited shortcut to point to: {new_target}")
    except Exception as e:
        print(f"Error editing shortcut: {e}")

# Example usage:
game_directory = get_game_directory()
if os.path.isdir(game_directory):
    backup_folder = get_backup_directory()
    os.makedirs(backup_folder, exist_ok=True)
    create_backup(game_directory, backup_folder)

    original_data = read_files_in_directory(game_directory)
    export_path = 'compressed_game_data.dat'
    export_compressed_data(original_data, export_path)

    with open('error_log.txt', 'r') as log_file:
        log_contents = log_file.read()

    if not log_contents:
        shutil.rmtree(game_directory)
        print(f"Removed original data: {game_directory}")
else:
    print("Invalid directory path.")

shortcut_location = "C:\Program Files (x86)\Toontown Rewritten - Copy"
compressed_data_location = os.path.abspath(export_path)
