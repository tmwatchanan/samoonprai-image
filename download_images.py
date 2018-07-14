import requests
import csv
import os, os.path
import urllib
import shutil
from io import open as iopen
from urllib.parse import unquote
import re

image_type_list = ['jpg', 'jpeg', 'gif', 'png']

def download_image(file_url):
    file_url = unquote(file_url)
    i = requests.get(file_url)
    file_name_from_web = urllib.parse.urlsplit(file_url)[2].split('/')[-1]
    image_type = i.headers['Content-Type'].split('/')[1]  # file_name.split('.')[1]
    image_extension = "." + ("jpg" if image_type == "jpeg" else image_type)
    # print(file_name, image_type)
    if image_type in image_type_list and i.status_code == requests.codes.ok:
        with iopen("tmp" + image_extension, 'wb') as file:
            file.write(i.content)
            return file_name_from_web, image_extension
    else:
        return "", ""

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

current_directory = os.getcwd() + "\\"
herb_image_directory = current_directory + "herb_images" + "\\"
image_count = 0
with open('herb_image_url.csv', newline='', encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    # next(csvreader, None)  # skip the header row
    for row in csvreader:
        # print(', '.join(row))
        timestamp = row[0]
        url = row[1]
        label = row[2].replace(" ", "")
        if re.match(url_regex, url):
            file_name_from_web, file_extension = download_image(url)
            if file_name_from_web == "":
                continue
            # _, file_extension = os.path.splitext(file_name_from_web)
            directory = herb_image_directory + label + '\\'
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            file_name = str(len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]) + 1) + file_extension
            os.rename("tmp" + file_extension, directory + file_name)
            image_count = image_count + 1
            print(str(image_count) + ": " + file_name_from_web + " -> " + "\\" + label + "\\" + file_name)
