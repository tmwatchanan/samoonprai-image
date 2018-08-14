import requests
import csv
import os, os.path
import urllib
import shutil
from io import open as iopen
from urllib.parse import unquote
import re
import json
import pathlib

image_type_list = ['jpg', 'jpeg', 'gif', 'png']

def download_image(file_url):
    file_url = unquote(file_url)
    try:
        i = requests.get(file_url, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        # return 'Server taking too long. Try again later'
        return '',''
    else:
        file_name_from_web = urllib.parse.urlsplit(file_url)[2].split('/')[-1]
        ext_from_url = file_name_from_web.split(".")[-1]
        content_type = i.headers.get('Content-Type')
        image_type = None
        if content_type:
            image_type = content_type.split('/')[1]  # file_name.split('.')[1]
        else:
            image_type = ext_from_url
        image_extension = "." + ('jpg' if image_type == 'jpeg' else image_type)
        # print(file_name, image_type)
        if image_type in image_type_list and i.status_code == requests.codes.ok:
            with iopen("tmp" + image_extension, 'wb') as file:
                file.write(i.content)
                return file_name_from_web, image_extension
        else:
            return '', ''

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


herb_json_array = None
with open(os.path.join('data', 'herb_data.json'), encoding="utf-8") as f:
    herb_json_array = json.load(f)

herb_image_directory = os.path.join(os.getcwd(), "herb_images")
image_count = 0
with open(os.path.join('data', 'herb_image_url.csv'), newline='', encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    # next(csvreader, None)  # skip the header row
    for row in csvreader:
        # print(', '.join(row))
        timestamp = row[0]
        url = row[1]
        label = row[2]#.replace(" ", "")
        if re.match(url_regex, url):
            file_name_from_web, file_extension = download_image(url)
            if file_name_from_web == '':
                print("SKIPPED:", url, "->", label)
                continue
            # _, file_extension = os.path.splitext(file_name_from_web)
            # name_list = set([x.strip() for x in label.split('|')])
            name_list = re.split(', |\|', label)
            matched_herb_object_list = [x for x in herb_json_array if set(x['thaiNameList']) == set(name_list)]
            matched_herb_object = matched_herb_object_list[0]
            if matched_herb_object['thaiNameList'].count == 0:
                continue
            herb_id = matched_herb_object['herbId']
            directory = os.path.join(herb_image_directory, str(herb_id))
            print(directory)
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
            # os.makedirs(os.path.dirname(directory), exist_ok=True)
            file_name = str(len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]) + 1) + file_extension
            os.rename("tmp" + file_extension, os.path.join(directory, file_name))
            image_count = image_count + 1
            print(str(image_count) + ": " + file_name_from_web + " -> " + "/" + str(herb_id) + "/" + file_name)
