import os
import json
from glob import glob

paths = glob('Place/*')
print(len(paths))
tree = {}

for se_path in paths:
    if (os.path.exists(se_path + '/all_category.json')):
        with open(se_path + '/all_category.json', 'r') as f:
            data_loaded = json.load(f)

        big_place = se_path.split('\\')[-1]
        tree[big_place] = {
            'second_place': [],
            'third_place': [],
            'number_place_second': len(data_loaded),
            'number_place_third': 0,
        }
        for key in data_loaded:
            tree[big_place]['second_place'].append({
                'src_place': key,
                'type': 1
            })
            for value in data_loaded[key]:
                tree[big_place]['third_place'].append({
                    'src_place': value,
                    'type': 2
                })
                tree[big_place]['number_place_third'] += 1

        # print(tree[big_place])
        # break
    else:
        # Các địa danh chỉ có 1 category thường là địa danh nước ngoài
        big_place = se_path.split('\\')[-1]  # In place.json
        tree[big_place] = {
            'second_place': [{'src_place': 'https://www.foody.vn/' + big_place,
                             'type': 1}],
            'third_place': [],
            'number_place_second': 1,
            'number_place_third': 0,
        }

path = 'place_tree.json'
with open(path, 'w') as f:
    json.dump(tree, f)
