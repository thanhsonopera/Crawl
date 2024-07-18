# Crawl

## Install env

```
conda create --name nameenv python=3.11
```

```
conda activate nameenv
```

```
conda install --file requirements.txt
```

```
conda list
```

## Run Scrapy

```
scrapy
```

```
scrapy startproject foody (Đã tạo rồi không cần chạy lại)
```

```
cd foody
```

```
scrapy genspider pathspider https://www.foody.vn/
```

```
scrapy shell
```

```
fetch('https://www.foody.vn/')
```

## Run Selenium

```
cd Selenium
```

```
python crw.py

```

- category_crw.py to convert folder Place
- place_crw.py to convert place.json
- restaurant_cvt to match all link folder Place - place_tree.json
- folder data_review_in_shop : format data
