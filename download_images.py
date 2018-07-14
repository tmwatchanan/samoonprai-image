import requests
import csv
import os, os.path

current_directory = os.getcwd() + "\\"
herb_image_directory = current_directory + "herb_images" + "\\"
image_count = 0
with open('herb_image_url.csv', newline='', encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader, None)  # skip the header row
    for row in csvreader:
        # print(', '.join(row))
        timestamp = row[0]
        url = row[1]
        label = row[2].replace(" ", "")
        r = requests.get(url, allow_redirects=True)
        if "\<http" in r.content:
            continue
        if url.find('/'):
            file_name_from_web = url.rsplit('/', 1)[1]
            file_extension = file_name_from_web.rpartition(".")[-1]
            fitlered_file_extension = file_extension[0:3] # substring for extra query
            file_extension = "." + fitlered_file_extension
            if file_name_from_web.find(".") == -1: # not found
                file_extension = ".jpg"
            # print(file_name_from_web, file_name_with_path)
            directory = herb_image_directory + label + '\\'
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            file_name = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]) + 1
            open(directory + str(file_name) + file_extension, 'wb').write(r.content)
            image_count = image_count + 1
            print(str(image_count) + ": " + file_name_from_web)
