from selenium import webdriver
import time
import os
import json
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException

os.environ['WDM_SSL_VERIFY'] = '0'

start_time = time.time()

missing_place = ['binh-duong']

for place in tqdm(missing_place):
    print('\n', place)
    try:
        driver = webdriver.Chrome(
            executable_path=r'C:\Users\thanh\Desktop\CRAWL\Selenium\chromedriver\chromedriver.exe')

        driver.get("https://www.foody.vn" + '/' + place)
        time.sleep(5)

        folder = 'Place/' + place
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Get Service
        driver.find_element_by_xpath(
            "//div[@id='head-navigation']").click()
        time.sleep(3)
        try:
            ul_1 = driver.find_element_by_xpath(
                '//header/div[2]/div[1]/div[2]/div[2]/ul[1]')
            all_href_menu_1 = []
            all_href_menu_2 = {}

            for level1 in ul_1.find_elements_by_xpath(".//li[@data-id]"):
                href = level1.find_element_by_xpath(
                    ".//a").get_attribute('href')
                all_href_menu_1.append(href)

                all_href_menu_2[href] = []
                ul_2 = level1.find_element_by_xpath("//ul[@id='nav-place-1']")

                for level2 in ul_2.find_elements_by_xpath(".//li"):

                    href_2 = level2.find_element_by_xpath(
                        ".//a").get_attribute('href')
                    all_href_menu_2[href].append(href_2)

            filename = folder + '/all_category.json'

            with open(filename, 'w') as f:
                json.dump(all_href_menu_2, f)

        except NoSuchElementException:
            print('\n', place, 'Not found')
    finally:
        driver.quit()

end_time = time.time()

elapsed_time = end_time - start_time
all_mins = int(elapsed_time / 60)
all_secs = int(elapsed_time - (all_mins * 60))

print(f"Elapsed time: {all_mins} mins {all_secs} secs")
