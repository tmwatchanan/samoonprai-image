import requests
from bs4 import BeautifulSoup, Comment
import re
import unicodedata


def remove_html_tags(input_text):
    filtered = re.sub('<[^>]*>', '', input_text)
    return filtered


page_link = "https://medthai.com/%E0%B8%AB%E0%B8%8D%E0%B9%89%E0%B8%B2%E0%B8%AB%E0%B8%A7%E0%B8%B2%E0%B8%99/"
response = requests.get(page_link)
soup = BeautifulSoup(response.content, "html.parser")
# print(soup.prettify())

content = soup.find(id="single-post-content")
# print(content)
herb_name = content.h2.string
print(herb_name)

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
    print(header_text)
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
        list_text = list.text.strip()
        list_text = unicodedata.normalize("NFKD", list_text)  # remove unwanted \xa string
        ref_list.append(list_text)
    count = count + 1

print(benefit_list)
print(property_list)

herb_data = {}
herb_data['thaiName'] = herb_name
herb_data['benefitList'] = benefit_list
herb_data['propertyList'] = property_list
print(herb_data)


# for element in soup.findAll(lambda tag: tag.name in ['head', 'script', 'link', 'meta', 'style']):
#     element.extract()
# for element in soup.find_all(text=lambda text: isinstance(text, Comment)):
#     element.extract()


