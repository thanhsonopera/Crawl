from selenium import webdriver
import time
import os
import re
import json
from tqdm import tqdm
"""
    Format place_tree.js
    {
        place1 : {
            second_place : [{src_place : src, type: int}, {}],
            third_place : [{src_place : src, type: int}, {}],
            number_place_second : int,
            number_place_third : int
        },
        place2 : {
            ...
        }
    }

"""
os.environ['WDM_SSL_VERIFY'] = '0'


def getSource(link, type):
    if (type == 1):
        object_list = []
        try:
            driver = webdriver.Chrome(
                executable_path=r'C:\Users\thanh\Desktop\CRAWL\Selenium\chromedriver\chromedriver.exe')
            # Login
            driver.get(
                "https://id.foody.vn/account/login?returnUrl={}".format(link))
            time.sleep(3)
            driver.find_element_by_xpath(
                "//input[@id='Email']").send_keys('tachien2003@gmail.com')
            driver.find_element_by_xpath(
                "//input[@id='Password']").send_keys('S0ngm4im4i@')
            driver.find_element_by_xpath("//input[@id='bt_submit']").click()

            time.sleep(8)

            # ul = driver.find_element_by_xpath(
            #     "//body/div[@id='FoodyApp']/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]")
            # cnt = 0
            # for child in ul.find_elements_by_xpath(".//div[@class='content-item ng-scope']"):
            #     cnt += 1
            # print(cnt)
            # time.sleep(1)
            high_before = driver.execute_script(
                "return document.body.scrollHeight")

            while True:
                # driver.execute_script(
                #     "window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(3)
                # high_after = driver.execute_script(
                #     "return document.body.scrollHeight")
                # print(high_before, high_after)
                try:
                    btn = driver.find_element_by_xpath(
                        ".//a[@class='fd-btn-more']")
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true); window.scrollBy(0, -200);", btn)
                    print(btn.get_attribute('outerHTML'))
                    time.sleep(5)
                    btn.click()
                    time.sleep(10)
                except:
                    print('No button')
                    break

            time.sleep(3)
            try:
                ul = driver.find_element_by_xpath(
                    "//body/div[@id='FoodyApp']/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]")
                cnt = 0
                time.sleep(1)
                for child in ul.find_elements_by_xpath(".//div[@class='content-item ng-scope']"):
                    cnt += 1
                    href = ''
                    src = ''
                    name = ''
                    address = ''
                    user_href = ''
                    user_src = ''
                    user_name = ''
                    user_comment = ''
                    comment = ''
                    check_in = ''
                    try:
                        avatar = child.find_element_by_xpath(
                            ".//div[@class='avatar']")
                        a = avatar.find_element_by_xpath(".//a")
                        href = a.get_attribute('href')
                        img = a.find_element_by_xpath(".//img")
                        src = img.get_attribute('src')

                    except:
                        pass

                    try:
                        second = child.find_element_by_xpath(
                            ".//div[@class='items-content hide-points']")
                        a = second.find_element_by_xpath(".//a")
                        name = a.get_attribute('text')
                        div = second.find_element_by_xpath(
                            ".//div[contains(@class, 'fd-text-ellip') and contains(@class, 'ng-binding')]")
                        address = div.text

                    except:
                        pass

                    try:
                        review = child.find_element_by_xpath(
                            ".//div[@class='items-review ng-scope']")
                        avatar = review.find_element_by_xpath(
                            ".//div[@class='avatar']")
                        a = avatar.find_element_by_xpath(".//a")
                        user_href = a.get_attribute('href')
                        img = a.find_element_by_xpath(".//img")
                        user_src = img.get_attribute('src')
                        content = review.find_element_by_xpath(
                            ".//div[contains(@class, 'users-content')]")
                        k = 1
                        for c in content.find_elements_by_xpath(".//a"):
                            if (k == 1):
                                user_name = c.text
                                k += 1
                            else:
                                user_comment = c.text
                    except:
                        pass
                    try:
                        interact = child.find_element_by_xpath(
                            ".//div[@class='items-count']")
                        k = 1
                        for child in interact.find_elements_by_xpath(".//a"):
                            span = child.find_element_by_xpath(".//span")
                            if (k == 1):
                                comment = span.text
                            elif (k == 2):
                                check_in = span.text
                            else:
                                break
                            k += 1
                    except:
                        pass

                    object_list.append({
                        'href': href,
                        'src': src,
                        'name': name,
                        'address': address,
                        'user_href': user_href,
                        'user_src': user_src,
                        'user_name': user_name,
                        'user_comment': user_comment,
                        'comment': comment,
                        'check_in': check_in
                    })
                    # print(
                    #     f'{href} : {src} : {name} : {address} : {user_href} : {user_src} : {user_name} : {user_comment} : {comment} : {check_in}')

                print(cnt)
            except:
                print('No review')
        finally:
            driver.quit()
        return object_list
    else:
        pass


if __name__ == '__main__':

    with open('place_tree.json', 'r') as f:
        data_loaded = json.load(f)
    check = False
    for place_name, place_data in tqdm(data_loaded.items()):
        print(place_name)

        if (check):
            place_object_second = []
            for second_place in tqdm(place_data['second_place']):
                print(second_place['src_place'])
                object_list = getSource(
                    second_place['src_place'], second_place['type'])
                place_object_second.append(
                    {second_place['src_place']: object_list})

            print('---------------------------------')
            folder = 'Place/' + place_name + '/second_place'
            if not os.path.exists(folder):
                os.makedirs(folder)
            filename = folder + '/second_place.json'
            with open(filename, 'w') as f:
                json.dump(place_object_second, f)

            for third_place in tqdm(place_data['third_place']):
                print(third_place['src_place'])

            print('---------------------------------')
        if (place_name == 'Kedah'):
            check = True
