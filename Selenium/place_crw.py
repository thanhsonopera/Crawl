from selenium import webdriver
import time
import os
import json

os.environ['WDM_SSL_VERIFY'] = '0'
# https://stackoverflow.com/questions/76614392/getting-error-when-i-run-selenium-script-value-error-timeout-value-connect-was
driver = webdriver.Chrome(
    executable_path=r'C:\Users\thanh\Desktop\CRAWL\Selenium\chromedriver\chromedriver.exe')

try:

    driver.get("https://www.foody.vn")

    # Wait for the page to load
    time.sleep(3)

    driver.find_element_by_xpath(
        '//header/div[2]/div[1]/div[1]/div[1]').click()

    time.sleep(3)

    placeHtml = driver.find_element_by_xpath(
        "//header/div[2]/div[1]/div[1]/div[2]/ul[1]/li[1]/ul[1]")
    # li / {ul / li} / a
    place = set()
    place.add('')
    for range in placeHtml.find_elements_by_xpath(".//li"):
        a_tags = range.find_elements_by_xpath(".//a")

        for a in a_tags:
            s = a.get_attribute('href').split('/')
            place.add(s[-1])

    place_str = list(place)
    data_to_save = {'place': place_str}

    filename = 'place.json'

    with open(filename, 'w') as f:
        json.dump(data_to_save, f)

    # filename = 'place.json'
    # with open(filename, 'r') as f:
    #     data_loaded = json.load(f)

    # print(len(data_loaded['place']))


finally:

    driver.quit()
