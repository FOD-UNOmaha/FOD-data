from operator import delitem
import sys
import os
import re
import json
import argparse
import cv2
import csv
import ffmpeg
from pathlib import Path
from pathvalidate.argparse import validate_filepath_arg

# IMPORTANT: Only add to the end of these lists. Doing otherwise could break the annotations.
weather_types = ['Dry', 'Wet']
light_types = ['Bright', "Dim", "Dark"]

def create_directory(output_file_location, target_video):
    i = 0
    try: 
        # Create a folder based on the file name.
        while(True):
            i += 1
            new_path = create_frame_filepath(output_file_location, target_video, i)

            if not os.path.exists(new_path):
                os.makedirs(new_path)
                break
        return new_path
    except: 
        print ("An error occurred when creating a directory for frame output at " + output_file_location +" for target file " + target_video + ".")
        quit()

def create_frame_filepath(directory, target_name, incrementer):
    try:  
        video_name_stem = Path(target_name).stem + str(incrementer)
        return directory + os.sep + video_name_stem + os.sep + "frame"
    except:
        print("An error occured when creating a new directory name at " + directory +".")
        quit()

def trim_video(video_file_location, target_filename, start_time, end_time, video_format='mp4'):
    trim_process = (
        ffmpeg
        .input(video_file_location)
        .trim(start=start_time, end=end_time)
        .filter('fps', fps=15, round='up')
        .setpts('PTS-STARTPTS')
        .output(filename=target_filename, format=video_format)
        .run_async())
    trim_process.communicate()
    return target_filename

def create_frames(video_file_location, output_directory, arguments, utilities_directory, categorization_file, csv_headers):
    try:
        validate_video_file(video_file_location)
        validate_output_filepath(output_directory)
        current_frame = 0
        video = create_video_capture(video_file_location)
        
        # Process frames until there are no frames left.
        print("Creating frames...")
        print("IMPORTANT: Do not open categorization annotations csv file.")
        while(True): 
            ret, frame = video.read() 
        
            if ret:  
                # Write the current frame to disk.
                
                frame_name = output_directory + os.sep + "frame_" + str(current_frame).zfill(6) + '.PNG' 
                rel_path_file_path = os.path.split(frame_name)[1]
                rel_path_sublevel_1 = os.path.split(os.path.split(frame_name)[0])[1]
                rel_path_sublevel_2 = os.path.split(os.path.split(os.path.split(frame_name)[0])[0])[1]
                rel_path = os.path.join(rel_path_sublevel_2, rel_path_sublevel_1, rel_path_file_path)
                cv2.imwrite(frame_name, frame)
                
                # Write the frame information to file.
                write_image_info(utilities_directory, categorization_file, csv_headers, rel_path, arguments.weather, arguments.light)

                current_frame += 1
            else: 
                break
        
        # Release all space and windows once frame creation is complete.
        video.release() 
        cv2.destroyAllWindows()
        print("Done!\nFrames are located at: " + output_directory)
    except:
        print("An error occurred when seperating the video into frames for the video at " + output_directory + ".")
        quit()

def write_image_info(csv_file_location, categorization_file_name, csv_headers, image_location, weather, light):
    try:
        path = os.path.join(csv_file_location, categorization_file_name)
        is_new_csv_file = False
        
        # If annotation file does not exist create it and add column names.
        try:
            if not os.path.isfile(path):
                is_new_csv_file = True

            with open(path, 'a', newline='') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if is_new_csv_file:
                    filewriter.writerow(csv_headers)
                filewriter.writerow([image_location, weather, light])
        except:
            print("Please close CSV File.")
            quit()
    except:
        print("An error occurred when creating categorization annotations.")
        quit()

def validate_time(time):
    try:
        time = str(time)
        min_sec_pattern = re.compile('(^\d{1,2}):(\d{1,2}):(\d{1,2})$')
        if (time == '0'):
            return 0
        elif (min_sec_pattern.match(time)):
            return convert_to_seconds(time)
        elif (float(time)):
            return round(float(time), 2)
        else:
            raise ValueError
    except ValueError:
        print("Error: Time format not found for input " + str(time) + ", please check -h (help) for appropriate formats.")
        quit()

def validate_weather(weather):
    try:
        weather = str(weather).lower()
        weather_list = list(map(str.lower, weather_types))
        return weather_list.index(weather)
    except ValueError:
        print("Weather must be one of the following: ")
        print(weather_types)
        quit()

def validate_light(light):
    try:
        light = str(light).lower()
        light_list = list(map(str.lower, light_types))
        return light_list.index(light)
    except ValueError:
        print("Light must be one of the following: ")
        print(light_types)
        quit()

def create_video_capture(filepath):
    return cv2.VideoCapture(filepath)

def convert_to_seconds(time_string):
    try:
        # Convert string HH:MM:SS to seconds, validation should occur before this function is called.
        time_array = time_string.split(':')
        return round(float(time_array[0])*60*60 + float(time_array[1])*60 + float(time_array[2]), 2)
    except:
        print("An error occured when converting the input time into seconds.")
        quit()

def get_args():
    parser = argparse.ArgumentParser(description="Process a video")
    parser.add_argument('-c', action='store_true', required=False, help="Change settings before outputting video", dest="settings", )
    parser.add_argument('-i', type=validate_filepath_arg, required=True, help="File path for the input video", dest="filepath")
    parser.add_argument('-s', type=validate_time, required=False, default=0, help="Start trim time (optional) -- valid formats: HH:MM:SS or a decimal value in seconds (ex 0.5 = 500 milliseconds)", dest="start_time")
    parser.add_argument('-e', type=validate_time, required=False, default=-1, help="End trim time (optional) -- valid formats: HH:MM:SS or a decimal value in seconds (ex 0.2 = 200 milliseconds)", dest="end_time")
    parser.add_argument('-w', type=validate_weather, required=True, help="Weather setting in video (Dry, Wet)", dest="weather")
    parser.add_argument('-l', type=validate_light, required=True, help="Light setting in video (Bright, Dim, Dark)", dest="light")
    args = parser.parse_args()

    # Modify settings if -c is passed.
    if (args.settings):
        change_settings()

    if not (os.path.isfile(args.filepath)):
        print("Error: Inputted filepath is not a file.")
        quit()

    # Calculate the length of the video to verify inputs
    if not (validate_video_file(args.filepath)):
        print("Error: Video file at " + args.filepath + " is not a valid mp4 file.")
        quit()

    video = create_video_capture(args.filepath)
    video_length = validate_time(video.get(cv2.CAP_PROP_FRAME_COUNT) / int(video.get(cv2.CAP_PROP_FPS)))

    if (args.end_time == -1):      
        args.end_time = video_length
    if (args.end_time < 0 or args.start_time < 0):
        print("Error: Trim time cannot be less than 0 seconds.")
        quit()
    if (args.end_time <= args.start_time):
        print("Error: End time must be greater than start time.")
        quit()
    if (args.end_time > video_length):
        print("Error: End time is longer than the length of the video.")
        quit()
    return args

def get_settings(settings_filename, output_path_index):
    full_filepath = os.path.join(sys.path[0], settings_filename)
    if not (os.path.isfile(full_filepath)):
        print("Settings file does not exist, we must create one first.")
        create_settings(settings_filename, output_path_index)
    with open(full_filepath) as input_file:
        settings = json.load(input_file)

    # Check to make sure the output filepath exists before returning it
    if not (validate_settings_filepath(settings, output_path_index)):
        print("Output file path is corrupted, please enter a new one.")
        create_settings(settings_filename, output_path_index)
        return get_settings(settings_filename, output_path_index)
    return settings

def change_settings():
    create_settings(SETTINGS_FILENAME, OUTPUT_PATH_INDEX)
    
def create_settings(settings_filename, output_index):
    settings_dict = {}

    while (True):
        output_path = input("Enter a default output folder: ")
        setup_complete = os.path.isdir(output_path)

        if (setup_complete):
            # Clean up the file path by inputting it into pathlib. 
            settings_dict[output_index] = str(Path(output_path).absolute())
            break
        else:
            print("Inputted folder location does not exist, please try again.")

    # Add all settings to the settings json file.
    with open (settings_filename, 'w') as output_file:
        json.dump(settings_dict, output_file, indent=4)

def validate_settings_filepath(settings, output_path_index):
    return os.path.isdir(settings[output_path_index])

def validate_output_filepath(filepath):
    return os.path.isdir(filepath)

def validate_video_file(filepath):
    return Path(filepath).suffix.lower() == ".mp4"

def validate_folder_structure(dataset_location, dataset_util_foldername):
    path = os.path.join(dataset_location, dataset_util_foldername)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def print_categorization_information(util_dir, category_file_name):
    path = os.path.join(util_dir, category_file_name)
    with open(path, "w") as txtfile:
        txtfile.write("The indice of the list correspondes to the label in the category annotation file (e.g. the list [clear, rainy] means clear = 0 and rainy = 1).\n")
        txtfile.write("Weather: [")
        for weather in weather_types:
            txtfile.write(weather + ',')
        txtfile.write(']\n')
        txtfile.write("Light: [")
        for light in light_types:
            txtfile.write(light + ',')
        txtfile.write(']\n')

# Entrance into the application.
SETTINGS_FILENAME = 'settings.json'
OUTPUT_PATH_INDEX = 'output_location'
dataset_utilities_folder = 'All_Dataset_Utility_Files'
categorization_csv_file_name = 'FOD_categorization_annotations.csv'
csv_headers = ['File', 'Weather', 'Light']
categorization_information_file = 'category_information.txt'

arguments = get_args()
settings = get_settings(SETTINGS_FILENAME, OUTPUT_PATH_INDEX)
util_dir = validate_folder_structure(settings[OUTPUT_PATH_INDEX], dataset_utilities_folder)
print_categorization_information(util_dir, categorization_information_file)
output_directory = create_directory(settings[OUTPUT_PATH_INDEX], arguments.filepath)
output_file = str(Path(output_directory).parent) + os.sep + os.path.basename(arguments.filepath)
create_frames(trim_video(arguments.filepath, output_file, arguments.start_time, arguments.end_time), output_directory, arguments, util_dir, categorization_csv_file_name, csv_headers)