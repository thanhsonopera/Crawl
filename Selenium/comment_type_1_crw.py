from selenium import webdriver
import os
import json
from tqdm import tqdm
from glob import glob
import time
import re
"""
    Place/*/second_place/*.json
    -> [
            {
                key :
                    [
                        {
                            "href" : link,

                        }, as shop
                        {
                        }
                    ] as val
            },
            {
            }  as data_shop
            , ...
        ] as data_all_shop
"""


def getComment(href, num_comments):
    start = time.time()
    comments_shop = []
    cnt = 0
    info = {}
    logger = []
    menuL = []
    galleryL = []
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\thanh\Desktop\CRAWL\Selenium\chromedriver\chromedriver.exe')
    # Login
    driver.get(
        "https://id.foody.vn/account/login?returnUrl={}".format('https://www.foody.vn/'))
    time.sleep(3)
    driver.find_element_by_xpath(
        "//input[@id='Email']").send_keys('tachien2003@gmail.com')
    driver.find_element_by_xpath(
        "//input[@id='Password']").send_keys('S0ngm4im4i@')
    driver.find_element_by_xpath("//input[@id='bt_submit']").click()

    time.sleep(2)
    try:
        for attempt in range(7):
            driver.get(href)
            try:
                if "404" in driver.page_source:
                    print(
                        f"404 detected on attempt {attempt + 1}, retrying...")
                    continue
                else:
                    break
            except Exception as e:
                print('Error:', 'siu')
                break

        time.sleep(6)
        try:
            body = driver.find_element_by_css_selector(
                "div.micro-left-content")

            try:
                # Block 1
                menu_list = body.find_element_by_xpath(
                    ".//div[@class='delivery-dishes-group']")
                img = ''
                name = ''
                src = ''
                price = ''
                # print('MENU:', menu_list.get_attribute('outerHTML'))
                for menu in menu_list.find_elements_by_xpath(".//div[@class='delivery-dishes-item ng-scope']"):

                    img = menu.find_element_by_xpath(
                        ".//img[@class='img-box']").get_attribute('src')

                    name = menu.find_element_by_xpath(
                        ".//a[@class='title-name-food']").\
                        find_element_by_xpath(
                            ".//div[@class='title-name ng-binding ng-isolate-scope']").text

                    src = menu.find_element_by_xpath(
                        ".//a[@class='title-name-food']").get_attribute('href')

                    price = menu.find_element_by_xpath(
                        ".//span[@class='price ng-binding']").text

                    menuL.append({'img': img, 'name': name,
                                 'src': src, 'price': price})

            except Exception as e:
                logger.append({'Error THUC DON': str(e)})
                print('Error THUC DON:', e)

            try:
                # Block 2
                gallery_1 = body.find_element_by_xpath(
                    ".//div[@class='microsite-box']")
                # print('GALLERY:', gallery_1.get_attribute('outerHTML'))
                gallery_1_List = gallery_1.find_elements_by_xpath(
                    ".//div[@class='micro-home-album']")
                img = ''
                name = []
                for gl in gallery_1_List:

                    img = gl.find_element_by_xpath('.//img').get_attribute(
                        'src')
                    pattern = r'<div class="edit-album-title">\n*(.*?)\n*</div>'
                    name = re.findall(pattern, gl.find_element_by_xpath(
                        ".//div[@class='edit-album-title']").get_attribute('outerHTML'))
                    if name != []:
                        name = name[0]
                    else:
                        name = ''
                    galleryL.append({'img': img, 'name': name})

            except Exception as e:
                logger.append({'Error GAL': str(e)})
                print('Error GAL:', e)

            # Init
            isShare = ''
            exellent = ''
            good = ''
            average = ''
            bad = ''
            table_score = []
            eval = ''
            point_overall = ''
            name_shop = ''
            type_1_shop = ''
            type_2_shop = ''
            time_open_shop = ''
            price_shop_range = ''

            try:
                # Block 3
                review = body.find_element_by_xpath(
                    ".//div[contains(@class, 'microsite-reviews-box')]")

                stats = review.find_element_by_xpath(".//div[@class='stats']")
                rating_box = stats.find_element_by_xpath(
                    ".//div[@class='ratings-boxes']")
                isShare = rating_box.find_element_by_xpath(
                    ".//div[@class='summary']").text
                i = 0
                for ty in rating_box.find_elements_by_xpath(".//div[@class='ratings-numbers']"):
                    if (i == 0):
                        exellent = ty.find_element_by_xpath(
                            ".//b[@class='exellent']").text
                        # print('exellent:', exellent)
                    elif (i == 1):
                        good = ty.find_element_by_xpath(
                            ".//b[@class='good']").text
                    elif (i == 2):
                        average = ty.find_element_by_xpath(
                            ".//b[@class='average']").text
                    else:
                        bad = ty.find_element_by_xpath(
                            ".//b[@class='bad']").text
                    i += 1

                table_tbody = rating_box.find_element_by_xpath(
                    ".//div[@class='micro-home-static']").find_element_by_xpath('.//tbody')
                trs = table_tbody.find_elements_by_xpath('.//tr')
                i = 0
                for tr in trs:
                    if (i >= 1):
                        typ = tr.find_element_by_xpath('.//td').text
                        score = tr.find_element_by_xpath('.//td/b').text
                        table_score.append({typ: score})
                    i += 1

                overall = rating_box.find_element_by_xpath(
                    ".//div[@class='ratings-boxes-points']")
                eval = overall.find_element_by_xpath(
                    ".//div").text.split('-')[1]
                point_overall = overall.find_element_by_xpath(
                    ".//span/b").text

            except Exception as e:
                logger.append({'Error Block 3': str(e)})
                print('Error Block 3:', e)

            try:
                # Block 4
                header_i = driver.find_element_by_css_selector(
                    "div.micro-header")

                name_shop = header_i.find_element_by_xpath(
                    ".//div[@class='main-info-title']/h1").text

                type_1_shop = header_i.find_element_by_xpath(
                    ".//div[@class='category']/div[@class='category-items']/a").text

                type_2_shop = header_i.find_element_by_xpath(
                    ".//a[@class='microsite-cuisine']").text

                time_open_shop = header_i.find_element_by_xpath(
                    ".//div[@class='micro-timesopen']/span[@class='itsclosed']/following-sibling::span[1]").text

                spn = header_i.find_element_by_xpath(
                    ".//div[@class='res-common-minmaxprice']")
                price_shop_range = spn.find_element_by_xpath(
                    ".//span[@itemprop='priceRange']").text

            except Exception as e:
                logger.append({'Error Header': str(e)})
                print('Error Header:', e)

            try:
                # Block 5
                review = body.find_element_by_xpath(
                    ".//div[contains(@class, 'microsite-reviews-box')]")
                b_review = review.find_element_by_xpath(
                    ".//div[@class='lists list-reviews']").\
                    find_element_by_xpath(
                        ".//div[contains(@class, 'foody-box-review')]")

                review_list = b_review.find_element_by_xpath(
                    ".//ul[contains(@class, 'review-list')]").\
                    find_elements_by_xpath(
                        ".//li[contains(@class, 'review-item')]")

                load_more = 0
                while True:
                    try:
                        btn = b_review.find_element_by_xpath(
                            ".//div[contains(@class, 'pn-loadmore')]/a[@class='fd-btn-more']")
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true); window.scrollBy(0, -200);", btn)
                        load_more += 1
                        logger.append({'Load_more': load_more})
                        print('Load_more:', load_more)
                        time.sleep(5)
                        btn.click()
                        time.sleep(10)
                    except Exception as e:
                        logger.append({'No button': str(e)})
                        print('No button', e)
                        break

                review_list = b_review.find_element_by_xpath(
                    ".//ul[contains(@class, 'review-list')]").\
                    find_elements_by_xpath(
                        ".//li[contains(@class, 'review-item')]")

                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)

                for cb in review_list:
                    cnt += 1
                    try:
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true); window.scrollBy(0, -120);", cb)
                        time.sleep(2)
                        user_href = ''
                        user_avatar = ''
                        user_name = ''
                        user_timec = ''
                        user_ratingP = ''
                        user_title_comment = ''
                        user_comment = ''
                        user_tbscore = []
                        try:
                            # Content User:
                            user = cb.find_element_by_xpath(
                                ".//div[contains(@class, 'review-user')]")
                            user_href = user.find_element_by_xpath(".//div[@class='review-avatar']").\
                                find_element_by_xpath(
                                    ".//a").get_attribute('href')
                            user_avatar = user.find_element_by_xpath(".//div[@class='review-avatar']").\
                                find_element_by_xpath(
                                    ".//img").get_attribute('src')
                            user_name = user.find_element_by_xpath(
                                ".//div[@class='ru-row']/a").text
                            user_timec = user.find_element_by_xpath(
                                ".//div[@class='ru-stats']/a/span").text
                            user_ratingP = user.find_element_by_xpath(
                                ".//div[contains(@class, 'review-points')]/span").text
                        except Exception as e:
                            logger.append({'Error Content User': str(e)})
                            print('Error Content User:', e)

                        try:
                            # Content User Des
                            des = cb.find_element_by_xpath(
                                ".//div[contains(@class, 'review-des')]")
                            user_title_comment = des.find_element_by_xpath(
                                ".//a[contains(@class, 'rd-title')]").text
                            user_comment = des.find_element_by_xpath(
                                ".//div[contains(@class, 'rd-des')]").find_element_by_xpath(".//span").text
                        except Exception as e:
                            logger.append({'Error Content User Des': str(e)})
                            print('Error Content User Des:', e)

                        try:
                            user = cb.find_element_by_xpath(
                                ".//div[contains(@class, 'review-user')]")
                            try:
                                user.find_element_by_xpath(
                                    ".//div[contains(@class, 'review-points')]").click()
                            except Exception as e:
                                logger.append({'Error Review Click': str(e)})

                            time.sleep(3)
                            while True:
                                try:
                                    popup = driver.find_element_by_xpath(
                                        './/div[contains(@class, "review-rating-popup")]')

                                    table_tbody = popup.find_element_by_xpath(
                                        ".//div[@class='review-popup-point']/div[@class='review-point-static']/table/tbody")

                                    break
                                except Exception as e:
                                    logger.append({'Wait to load': str(e)})
                                    time.sleep(1)
                            wait = 0

                            while True:
                                wait += 1
                                i = 0
                                is_has = True
                                if (len(table_tbody.find_elements_by_xpath('.//tr')) <= 1):
                                    logger.append({"hihihi": wait})
                                    is_has = False
                                    time.sleep(1)
                                else:
                                    for tr in table_tbody.find_elements_by_xpath('.//tr'):
                                        if (i >= 1):
                                            typ = tr.find_element_by_xpath(
                                                './/td').text
                                            score = tr.find_element_by_xpath(
                                                './/td/b').text

                                            if (typ == '' or score == ''):
                                                logger.append({"hihihi": wait})
                                                is_has = False
                                                time.sleep(1)
                                                break
                                            user_tbscore.append({typ: score})
                                        i += 1
                                if is_has:
                                    break
                        except Exception as e:
                            logger.append({'Error Popup': str(e)})
                            print('Error Popup:', e)

                    except Exception as e:
                        logger.append({'Error in review list': str(e)})
                        print('Error in review list', e)
                    comments_shop.append({'user_href': user_href, 'user_avatar': user_avatar,
                                          'user_name': user_name, 'user_timec': user_timec,
                                          'user_rating': user_ratingP, 'user_titlec': user_title_comment,
                                          'user_comment': user_comment, 'user_tbscore': user_tbscore})
            except Exception as e:
                logger.append({'Error Content': str(e)})
                print('Error Content:', e)
            info = {
                'isShare': isShare,
                'exellent': exellent,
                'good': good,
                'average': average,
                'bad': bad,
                'table_score': table_score,
                'eval': eval,
                'point_overall': point_overall,
                'name_shop': name_shop,
                'type_1_shop': type_1_shop,
                'type_2_shop': type_2_shop,
                'time_open_shop': time_open_shop,
                'price_avg_shop': price_shop_range,
            }
        except Exception as e:
            logger.append({'Error body': str(e)})
            print('Error body:', e)
    except Exception as e:
        logger.append({'Error': str(e)})
        print('Error:', e)
    end = time.time()
    # print('INFO:', info)
    # print('MENU:', menuL)
    # print('GALLERY:', galleryL)
    # print('CountCM:', cnt)
    # print('COMMENTS:', comments_shop)
    process = end - start
    logger.append({'Time': str(process // 60) + ' ' + str(process % 60)})
    # with open('comment_{}.json'.format(num_comments), 'w') as f:
    #     json.dump(comments_shop, f)
    # with open('logger_{}.json'.format(num_comments), 'w') as f:
    #     json.dump(logger, f)

    driver.quit()

    return comments_shop, cnt, info, menuL, galleryL


if __name__ == '__main__':

    os.environ['WDM_SSL_VERIFY'] = '0'

    paths = glob('Place/*/second_place/*.json')
    pbar = tqdm(paths)
    for path in pbar:
        place = path.split('\\')[1]
        src = 'Place/' + place + '/second_place'
        print('\n', place)

        # comments_shop, cnt, info, menuL, galleryL = getComment(
        #     'https://www.foody.vn/ho-chi-minh/quan-co-ba-banh-can-banh-xeo-phan-rang', pbar.n)
        with open(path, 'r') as f:
            data_all_shop = json.load(f)

            for data_shop in tqdm(data_all_shop):

                for key, val in data_shop.items():
                    print('\n', key)
                    category = key.split('/')[-1]
                    # all_comments = []
                    if not (category == place):
                        category = place + '_' + category
                    num_comments = 0
                    if os.path.exists(src + '/comment_{}.json'.format(category)):
                        with open(src + '/comment_{}.json'.format(category), 'r') as f:
                            all_comments = json.load(f)
                    else:
                        all_comments = []
                    shop_order = 0
                    for shop in tqdm(val):
                        if shop_order > 64:
                            comments_shop, cnt, info, menuL, galleryL = getComment(
                                shop['href'], num_comments)

                            # num_comments += cnt

                            all_comments.append(
                                {shop['href']: comments_shop,
                                 'info': info,
                                 'menu': menuL,
                                 'gallery': galleryL,
                                 'shop_order': shop_order})

                        print('\n Shop order: ', shop_order)
                        shop_order += 1
                        # print('Number of comments: ', num_comments)

                        # if os.path.exists(src + '/comment_{}.json'.format(category)):
                        #     with open(src + '/comment_{}.json'.format(category), 'r') as f:
                        #         data = json.load(f)
                        #         data.extend(all_comments)

                        #     with open(src + '/comment_{}.json'.format(category), 'w') as f:
                        #         json.dump(data, f)
                        # else:
                        with open(src + '/comment_{}.json'.format(category), 'w') as f:
                            json.dump(all_comments, f)

                # print(src + '/comment_{}.json'.format(category))

        #     driver.quit()
