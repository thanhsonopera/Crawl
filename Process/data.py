import glob
import os
import re
import tqdm
import json
import copy
from datetime import datetime


def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


class Data:
    def __init__(self):
        self.path_folder = '../Puppeteer/Comment/Place'

    def reportCheck(self):
        number_place = 0
        all_place_comment = 0
        all_place_shop = 0
        all_place_shop_more_100 = 0
        self.have_place = []
        with open('report.json', 'r') as f:
            data = json.load(f)
            for item in data:
                number_place += 1
                self.have_place.append(list(item.keys())[0])
                for it in item.keys():
                    for i, ki in enumerate(item[it]):
                        if (i == 0):
                            all_place_comment += list(ki.values())[0]
                        if (i == 1):
                            all_place_shop += list(ki.values())[0]
                        if (i == 2):
                            all_place_shop_more_100 += list(ki.values())[0]

        print('Number Place : ', number_place)
        print('All Comment Place : ', all_place_comment)
        print('All Shop Place : ', all_place_shop)
        print('All Shop Have More 100 Comment Place : ', all_place_shop_more_100)
        print('Have Place : ', self.have_place)

    def checkPlace(self):
        path = '../Selenium/place.json'
        self.placeHaveCheck = []
        with open(path, 'r') as f:
            data = json.load(f)

            for key in data.keys():
                for pl in data[key]:
                    if (pl not in self.have_place):
                        self.placeHaveCheck.append(pl)

        with open('placeExit.json', 'w', encoding='utf-8') as f:
            json.dump(self.placeHaveCheck, f, ensure_ascii=False,
                      indent=4)

    def process(self):
        files = glob.glob(self.path_folder + '/*/*.json')
        report = []
        old_place = ''
        for file in tqdm.tqdm(files):
            file = file.replace("\\", "/")
            new_place = file.split('/')[4]
            print('Place :', new_place)
            if (old_place != '' and new_place != old_place):
                report.append({
                    old_place: [
                        {'all_comment': all_comment},
                        {'all_shop': all_shop},
                        {'all_shop_more_100_cm': all_shop_more_100_cm}
                    ]
                })
            if (new_place != old_place or new_place == ''):
                all_comment = 0
                all_shop = 0
                all_shop_more_100_cm = 0
                old_place = new_place

            with open(file, 'r') as f:
                data = json.load(f)

            number_shop, number_shop_more_100_cm, number_comment = self.extractL1(
                data, file)

            print('NumberShopHave 100 comments : ', number_shop_more_100_cm)
            print('NumberShop', number_shop)
            print('NumComment', number_comment)

            all_comment += number_comment
            all_shop += number_shop
            all_shop_more_100_cm += number_shop_more_100_cm

            # break
        # print('All Comment Ho Chi Minh', all_comment)
        with open('report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False,
                      indent=4)

    def extractL1(self, data, file):
        paths = file.split('/')
        new_paths = 'Repreprocess/'
        path_static = new_paths + 'static' + '/' + paths[-2] + '/'
        new_paths += paths[-3] + '/' + paths[-2] + '/'
        if not os.path.exists(os.path.dirname(new_paths)):
            os.makedirs(os.path.dirname(new_paths))
        if not os.path.exists(os.path.dirname(path_static)):
            os.makedirs(os.path.dirname(path_static))

        number_shop = 0
        number_comment = 0
        number_shop_more_100_cm = 0
        new_data = []
        new_static = []
        for shop in data:
            is_valid, shop_more_100_cm, num_comment, new_shop, static_shop = self.extractL2(
                shop)
            if (is_valid):
                number_shop += 1
                new_shop['shop_order'] = number_shop
                static_shop['shop_order'] = number_shop

                new_data.append(new_shop)
                new_static.append(static_shop)
                number_comment += num_comment
                if shop_more_100_cm:
                    number_shop_more_100_cm += 1

        with open(new_paths + paths[-1], 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False,
                      indent=4, default=default_serializer)

        with open(path_static + paths[-1], 'w', encoding='utf-8') as f:
            json.dump(new_static, f, ensure_ascii=False, indent=4)

        return number_shop, number_shop_more_100_cm, number_comment

    def extractL2(self, shop):
        func = [self.extractComment, self.extractInfoShop,
                self.extractMenu, self.extractGallery]

        new_shop = copy.deepcopy(shop)
        static_shop = copy.deepcopy(shop)
        shopValid = True
        shop_more_100_cm = False
        num_comment = 0

        for i, key in enumerate(shop.keys()):
            if (key == 'shop_order'):
                if (i < 4):
                    shopValid = False
                break
            static, new = func[i](shop[key])

            if (i == 0):
                if (len(new) == 0):
                    shopValid = False
                else:
                    num_comment += len(new)

            new_shop[key] = new
            static_shop[key] = static
            if (i == 1):
                if static['reInfo'] == True:
                    shop_more_100_cm = True

            # print('{}'.format(key), new)
        return shopValid, shop_more_100_cm, num_comment, new_shop, static_shop

    @staticmethod
    def stringPassInt(str):
        number_pattern = r'(\d+)'
        result = re.findall(number_pattern, str)
        if (len(result) > 0):
            return int(result[0])
        return 0

    def extractComment(self, comments):
        new_comments = []
        num_miss_scoreType1 = 0  # table_score = []
        # table_score = [{ : miss}, {: miss}, {:miss}, {:miss}, {:miss}]
        num_miss_scoreType2 = 0
        num_comment_option = 0
        typeOption = {}
        num_hashtag = 0
        num_imgreview = 0
        num_cmtofcmt = 0
        for item in comments:
            if (len(item['user_tbscore']) > 0):
                new_item = copy.deepcopy(item)
                isHaveOption = False
                isValid = True

                for i, key in enumerate(item.keys()):
                    if (i < 7):
                        if (i == 0):  # user_href
                            new_item[key] = item[key].replace(
                                'shopeefood', 'foody')

                        if (i == 1):  # user_avatar
                            new_img = item[key].split('@')
                            if (len(new_img) > 0):
                                new_item[key] = new_img[0]
                            else:
                                new_item[key] = item[key]

                        if (i == 2):  # user_name
                            name = re.sub(r'[@#/.]', '', item[key])
                            name2 = re.sub(r'\s+', ' ', name).strip()
                            new_item[key] = name2

                        if (i == 3):  # user_timec
                            date_str = re.sub(r'\s+', ' ', item[key]).strip()
                            new_item[key] = datetime.strptime(
                                date_str, "%d/%m/%Y %H:%M")

                        if (i == 4):  # user_rating
                            score = re.sub(r'\s+', ' ', item[key]).strip()
                            try:
                                new_item[key] = float(score)
                            except ValueError:
                                new_item[key] = float('nan')

                        if (i == 5 or i == 6):
                            new_item[key] = re.sub(
                                r'\s+', ' ', item[key]).strip()

                    if (key == 'user_tbscore'):
                        new_it = []
                        for it in new_item[key]:
                            for type in it.keys():
                                new_type = re.sub(
                                    r'\s+', ' ', type).strip()
                                score = re.sub(
                                    r'\s+', ' ', it[type]).strip()
                                try:
                                    new_score = float(score)
                                except ValueError:
                                    isValid = False
                                    break

                                new_it.append({new_type: new_score})

                        new_item[key] = new_it

                    # user_options
                    if (i == 8):
                        for j, it in enumerate(item[key]):
                            isHaveOption = True
                            for ki in it:
                                if (ki == 'Sẽ quay lại:'):
                                    kii = re.sub(r'[!]', '', it[ki]).strip()
                                    if ('Có' in kii):
                                        kii = 'Có thể'
                                    if ('Sure' in kii):
                                        kii = 'Chắc chắn'

                                    new_item[key][j] = {ki: kii}

                                    try:
                                        typeOption[kii] += 1
                                    except KeyError:
                                        typeOption.setdefault(kii, 1)
                    # user_hashtag
                    if (i == 9):
                        for it in item[key]:
                            num_hashtag += 1
                            if (it == 'tagName'):
                                new_item[key][it] = re.sub(
                                    r'[#]', '', item[key][it]).strip()
                            if (it == 'tagHref'):
                                new_item[key][it] = item[key][it].replace(
                                    'shopeefood', 'foody')
                    # user_imgReview
                    if (key == 'user_imgReview'):
                        for it in range(len(item[key])):
                            num_imgreview += 1
                            for ki in item[key][it].keys():
                                new_img = item[key][it][ki].split('@')
                                if (len(new_img) > 0):
                                    new_item[key][it] = {ki: new_img[0]}
                                break

                    # user CmtOfCmt
                    if (key == 'user_CmtOfCmt'):
                        for ki in item[key].keys():
                            if (ki == 'nameUserLikeText'):
                                str = re.sub(
                                    r'\s+', ' ', item[key][ki]).strip()
                                if ('&' in str):
                                    new_item[key][ki] = str.split('&')
                                elif ('người khác' in str):
                                    new_item[key][ki] = str.split(',')[:-1]
                            if (ki == 'allCmtInPost'):
                                for j, it in enumerate(item[key][ki]):
                                    for kii in it.keys():
                                        if (kii == 'userCmtAvatarRef'):
                                            new_img = it[kii].split('@')
                                            if (len(new_img) > 0):
                                                new_item[key][ki][j][kii] = new_img[0]
                                        if (kii == 'userCmtRef'):
                                            new_item[key][ki][j][kii] = it[kii].replace(
                                                'shopeefood', 'foody')
                                        if (kii == 'userCmtName'):
                                            new_item[key][ki][j][kii] = re.sub(
                                                r'\s+', ' ', it[kii]).strip()
                                        if (kii == 'userCmtText'):
                                            new_item[key][ki][j][kii] = re.sub(
                                                r'\s+', ' ', it[kii]).strip()
                                        if (kii == 'userDateText'):
                                            date_str = re.sub(
                                                r'\s+', ' ', it[kii]).strip()
                                            new_item[key][ki][j][kii] = datetime.strptime(
                                                date_str, "%d/%m/%Y %H:%M:%S")

                            if (ki == 'numberCmtOfPost'):
                                if isValid:
                                    num_cmtofcmt += item[key][ki]

                if isValid:
                    new_comments.append(new_item)
                    num_comment_option += 1 if isHaveOption == True else 0
                else:
                    num_miss_scoreType2 += 1

            else:
                num_miss_scoreType1 += 1

        static = {'num_miss_scoreType1': num_miss_scoreType1,
                  'num_miss_scoreType2': num_miss_scoreType2,
                  'num_comment_option': num_comment_option,
                  'typeOption': typeOption,
                  'num_hashtag': num_hashtag
                  }
        return static, new_comments

    def extractInfoShop(self, info):
        # key1 = [0 for _ in range(5)]
        # key2 = ['' for _ in range(8)]
        new_info = copy.deepcopy(info)
        score_nan = False
        point_nan = False
        for i, key in enumerate(info.keys()):
            if (i < 5):
                new_info[key] = self.stringPassInt(info[key])
            if (i == 5):
                new_item = []
                for item in new_info[key]:
                    for type in item.keys():
                        new_type = re.sub(r'\s+', ' ', type).strip()
                        score = re.sub(r'\s+', ' ', item[type]).strip()
                        try:
                            new_score = float(score)
                        except ValueError:
                            new_score = float('nan')
                            score_nan = True
                        new_item.append({new_type: new_score})
                new_info[key] = new_item

            if (i > 5):
                text = info[key].replace('#', '')
                new_info[key] = re.sub(r'\s+', ' ', text).strip()
                # price_avg_shop
                if (key == 'point_overall'):
                    try:
                        new_info[key] = float(new_info[key])
                    except ValueError:
                        new_info[key] = float('nan')
                        point_nan = True
        static = {}
        if (new_info['isShare'] > 100):
            static = {'reInfo': True, 'failScore': score_nan,
                      'failPoint': point_nan}
        else:
            static = {'reInfo': False, 'failScore': score_nan,
                      'failPoint': point_nan}
        return static, new_info

    @staticmethod
    def extractMenu(menu):
        new_menu = []
        num_price = 0
        num_src = 0
        num_name = 0
        num_img = 0
        for item in menu:
            new_price = ''
            new_src = ''
            new_name = ''
            new_img = ''
            for key in item.keys():
                if (key == 'img'):
                    new_img = item[key].split('@')
                    if (len(new_img) > 0):
                        new_img = new_img[0]
                    else:
                        new_img = item[key]
                if (key == 'name'):
                    new_name = re.sub(r'\s+', ' ', item[key]).strip()
                if (key == 'src'):
                    new_src = item[key].replace('shopeefood', 'foody')
                if (key == 'price'):
                    new_price = item[key].replace('đ', '').replace('.', '')
            if (new_price != '' or new_name != '' or new_src != '' or new_img != ''):
                new_item = {
                    'img': new_img,
                    'src': new_src,
                    'name': new_name,
                    'price': new_price
                }
                num_price += 1 if new_price != '' else 0
                num_name += 1 if new_name != '' else 0
                num_src += 1 if new_src != '' else 0
                num_img += 1 if new_img != '' else 0
                new_menu.append(new_item)
        static = {
            'img': num_img,
            'src': num_src,
            'name': num_name,
            'price': num_price
        }
        return static, new_menu

    @staticmethod
    def extractGallery(gallery):
        new_gallery = []
        num_gallery = 0
        num_name = 0
        for item in gallery:
            src = ''
            result = ''
            for key in item.keys():
                # IMG
                if (key == 'img'):
                    src = item[key].split('@')
                    if (len(src) > 0):
                        src = src[0]
                    else:
                        src = item[key]
                # NAME
                if (key == 'name'):
                    pattern = r'<div class="edit-album-title">(.*?)</div>'
                    result = re.findall(pattern, item[key])
                    if (len(result) > 0):
                        result = re.sub(r'\s+', ' ', result[0]).strip()
                    else:
                        result = ''

            if (src != ''):
                new_item = {
                    'img': src,
                    'name': result
                }
                num_gallery += 1
                if (result != ''):
                    num_name += 1
                new_gallery.append(new_item)

        static = {
            'img': num_gallery,
            'name': num_name
        }
        return static, new_gallery
