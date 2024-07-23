from selenium import webdriver
import time
import os
import re
import json


def save_json(data, type=1):
    # Type 1: InitData
    # Type 2: ReviewData
    if (type == 1):
        filename = 'initData.json'
        log = 'initData'
    else:
        filename = 'reviewData.json'
        log = 'reviewData'
    if data:
        # Extract the matched object
        data_obj = data.group(1)
        try:
            # Convert the string to a Python dictionary
            data = json.loads(data_obj)

            # Write the dictionary to a file as JSON
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Data saved to {filename}")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

        print(f"Found {log} object:", data_obj)
    else:
        print(f"{log} object not found.")


os.environ['WDM_SSL_VERIFY'] = '0'
# https://stackoverflow.com/questions/76614392/getting-error-when-i-run-selenium-script-value-error-timeout-value-connect-was
driver = webdriver.Chrome(
    executable_path='chromedriver/chromedriver.exe')

try:
    # Login
    # driver.get(
    #     "https://id.foody.vn/account/login?returnUrl=https://www.foody.vn/ha-noi")
    # time.sleep(3)
    # driver.find_element_by_xpath(
    #     "//input[@id='Email']").send_keys('tachien2003@gmail.com')
    # driver.find_element_by_xpath(
    #     "//input[@id='Password']").send_keys('S0ngm4im4i@')
    # driver.find_element_by_xpath("//input[@id='bt_submit']").click()
    # time.sleep(3)

    driver.get("https://www.foody.vn/ha-noi")

    # Wait for the page to load
    time.sleep(3)
    # Get Place
    # driver.find_element_by_xpath(
    #     '//header/div[2]/div[1]/div[1]/div[1]').click()
    # time.sleep(5)
    # placeHtml = driver.find_element_by_xpath(
    #     "//header/div[2]/div[1]/div[1]/div[2]/ul[1]/li[1]/ul[1]")
    # # li / {ul / li} / a
    # place = set()
    # for range in placeHtml.find_elements_by_xpath(".//li"):
    #     a_tags = range.find_elements_by_xpath(".//a")

    #     for a in a_tags:
    #         s = a.get_attribute('href').split('/')
    #         place.add(s[-1])

    # place_str = list(place)
    # data_to_save = {'place': place_str}

    # Read Place from file

    # filename = 'place.json'

    # with open(filename, 'w') as f:
    #     json.dump(data_to_save, f)

    # filename = 'place.json'
    # with open(filename, 'r') as f:
    #     data_loaded = json.load(f)

    # print(len(data_loaded['place']))

    # Get Service
    driver.find_element_by_xpath(
        "//div[@id='head-navigation']").click()
    time.sleep(2)

    ul_1 = driver.find_element_by_xpath(
        '//header/div[2]/div[1]/div[2]/div[2]/ul[1]')
    all_href_menu_1 = []
    all_href_menu_2 = {}
    for level1 in ul_1.find_elements_by_xpath(".//li[@data-id]"):
        href = level1.find_element_by_xpath(".//a").get_attribute('href')
        all_href_menu_1.append(href)

        all_href_menu_2[href] = []
        ul_2 = level1.find_element_by_xpath("//ul[@id='nav-place-1']")

        for level2 in ul_2.find_elements_by_xpath(".//li"):

            href_2 = level2.find_element_by_xpath(
                ".//a").get_attribute('href')
            all_href_menu_2[href].append(href_2)

    print(all_href_menu_1)
    print(all_href_menu_2)
    filename = 'menu_category.json'

    with open(filename, 'w') as f:
        json.dump(all_href_menu_2, f)

    # element = driver.find_element_by_xpath(
    #     "//body/div[@id='FoodyApp']/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]")
    # child_elements = element.find_elements_by_xpath(
    #     "./*[contains(@class, 'content-item ng-scope')]")
    # cnt = 0
    # for child in child_elements:
    #     a_tags = child.find_elements_by_xpath(".//a")
    #     print(f'Group {cnt}')
    #     for a in a_tags:
    #         s = a.get_attribute('href')
    #         if (s and 'binh-luan' in s):
    #             print(s)
    #     cnt += 1

    # script_elements = driver.find_elements_by_tag_name('script')
    # js_scripts = [script for script in script_elements if script.get_attribute(
    #     'type') == 'text/javascript']

    # for script in js_scripts:
    #     pattern_reviewData = r"var initDataReviews = (\{.*?\}\]\})"
    #     pattern_initData = r"var initData = (\{.*?\});"

    #     str = script.get_attribute('innerHTML')

    #     match_reviewData = re.search(pattern_reviewData, str, re.DOTALL)
    #     match_initData = re.search(pattern_initData, str, re.DOTALL)

    #     save_json(match_reviewData, 2)
    #     save_json(match_initData, 1)
finally:
    # Clean up: close the browser window
    driver.quit()


def ReadJsonReview():
    file_path = 'reviewData.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(data['Items'][0]["Title"])
        print(data['Items'][0]["Description"])
        print(data['Items'][0]["TypeName"])
        print(data['Items'][0]["AvgRating"])
