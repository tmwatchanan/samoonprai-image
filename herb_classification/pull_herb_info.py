import requests
from bs4 import BeautifulSoup, Comment
import re
import unicodedata
import json
import os


def remove_html_tags(input_text):
    filtered = re.sub('<[^>]*>', '', input_text)
    return filtered

med_thai_uri = "https://medthai.com"
herb_table_of_contents_url = "https://medthai.com/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%AA%E0%B8%A1%E0%B8%B8%E0%B8%99%E0%B9%84%E0%B8%9E%E0%B8%A3/"
main_response = requests.get(herb_table_of_contents_url)
main_soup = BeautifulSoup(main_response.content.decode('utf-8', 'ignore'), "html.parser")
main_content = main_soup.find_all("div", {"class": "main-content page-content"})
main_content = main_content[0]
# print(main_content)
section_list = main_content.select('div[id^=หมวด-]')
herb_json_array = []
all_herb_names = set()
for section in section_list:
    # print(section)
    ul_children = section.ul.findChildren()
    for ul_child in ul_children:
        for a in ul_child.find_all('a', href=True):
            if a.text:
                herb_object = {}
                herb_object['thaiNameList'] = []
                herb_object['sourceUrl'] = med_thai_uri + a["href"]
                herb_full_name = a.parent.text
                cleaned_herb_full_name = re.sub(r'\[[^)]*\]', '', herb_full_name)  # remove square brackets []
                if cleaned_herb_full_name.find(" (") == -1:  # not found ()
                    herb_object['thaiNameList'].append(cleaned_herb_full_name)
                else:  # found () extra name(s)
                    herb_object['thaiNameList'].append(cleaned_herb_full_name[:cleaned_herb_full_name.find(" (")])
                    herb_name_extra_re = re.search(r'\((.*?)\)', cleaned_herb_full_name)
                    herb_name_extra = herb_name_extra_re.group(1)
                    herb_object['thaiNameList'] = herb_object['thaiNameList'] + [x.strip() for x in herb_name_extra.split(',')]
                # print(herb_object['thaiNameList'])
                existed = True
                for name in herb_object['thaiNameList']:
                   if name not in all_herb_names:
                       existed = False
                       all_herb_names.add(name)
                if not existed:
                    herb_json_array.append(herb_object)
print("#Total herbs from medthai = " + str(len(herb_json_array)))

# for herb in herb_json_array:
#     print(herb)

empty_herb_list = []
herb_number = 1
for herb_object in herb_json_array:
    print(str(herb_number) + ": " + herb_object['thaiNameList'][0] + " fetching data from " + herb_object['sourceUrl'])
    response = requests.get(herb_object['sourceUrl'])
    herb_soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")
    # print(soup.prettify())

    content = herb_soup.find(id="single-post-content")
    # print(content)

    # herb_common_name_element = content.find(lambda tag:tag.name=="strong" and "ชื่อสามัญ" in tag.text)
    # herb_common_name = ''.join(herb_common_name_element.parent.contents[1:]).strip()
    # print(herb_common_name)
    #
    # herb_scientific_name_element = content.find(lambda tag:tag.name=="strong" and "ชื่อวิทยาศาสตร์" in tag.text)
    # herb_scientific_name_element = herb_scientific_name_element.parent.contents[1:]
    # herb_scientific_name = "".join([str(item) for item in herb_scientific_name_element]).strip()
    # herb_scientific_name = remove_html_tags(herb_scientific_name)
    # print(herb_scientific_name)

    benefit_list = []
    property_list = []

    count = 1
    for h3 in content.find_all("h3"):
        # print(str(count) + ": " + h3.text + h3.find_next_sibling().text)
        header_text = h3.text.strip()
        ref_list = None
        if "ประโยชน์" in header_text:
            ref_list = benefit_list
        elif "สรรพคุณ" in header_text:
            ref_list = property_list
        else:
            continue
        order_list_element = h3.find_next_sibling()
        lists = order_list_element.find_all("li")
        for list in lists:
            list_text = unicodedata.normalize("NFKD", list.text)  # remove unwanted \xa string
            list_text = re.sub(r'\[[^)]*\]', '', list_text)  # remove square brackets []
            list_text = list_text.strip()
            ref_list.append(list_text)
        count = count + 1
    for h4 in content.find_all("h4"):
        # print(str(count) + ": " + h3.text + h3.find_next_sibling().text)
        header_text = h4.text.strip()
        ref_list = None
        if "ประโยชน์" in header_text:
            ref_list = benefit_list
        elif "สรรพคุณ" in header_text:
            ref_list = property_list
        else:
            continue
        order_list_element = h4.find_next_sibling()
        lists = order_list_element.find_all("li")
        for list in lists:
            list_text = unicodedata.normalize("NFKD", list.text)  # remove unwanted \xa string
            list_text = re.sub(r'\[[^)]*\]', '', list_text)  # remove square brackets []
            list_text = list_text.strip()
            ref_list.append(list_text)
        count = count + 1

    print(benefit_list)
    print(property_list)

    if (not benefit_list) and (not property_list):
        empty_herb_list.append(herb_object)

    herb_object['herbId'] = herb_number
    herb_object['benefitList'] = benefit_list
    herb_object['propertyList'] = property_list
    herb_number = herb_number + 1

with open(os.path.join('data', 'herb_data.json'), 'w', encoding="utf-8") as outfile:
    json.dump(herb_json_array, outfile, ensure_ascii=False)
with open(os.path.join('data', 'herb_data_empty.json'), 'w', encoding="utf-8") as outfile:
    json.dump(empty_herb_list, outfile, ensure_ascii=False)

# for element in soup.findAll(lambda tag: tag.name in ['head', 'script', 'link', 'meta', 'style']):
#     element.extract()
# for element in soup.find_all(text=lambda text: isinstance(text, Comment)):
#     element.extract()
