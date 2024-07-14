import requests
from bs4 import BeautifulSoup

url = 'https://www.foody.vn/ha-noi'

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())

selected_elements = soup.select(
    'body > div#FoodyApp > div:nth-of-type(4) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2)')
print(selected_elements)
