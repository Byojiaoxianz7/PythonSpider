# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


s_keyword = input('搜索书名： ')
s_url = 'https://sou.xanbhx.com/search?siteid=qula&q={}'.format(s_keyword)
s_res = requests.get(url=s_url)


bsObj = BeautifulSoup(s_res.text, 'lxml')
target_url = bsObj.select('.s2 a')[0]['href']


res = requests.get(url=target_url)
bsObj = BeautifulSoup(res.text, 'lxml')

all_chapter_url = []
all_chapter_title = []
for item in bsObj.select('#list dd a'):
    url = str(target_url) + str(item['href'])
    all_chapter_url.append(url)
    all_chapter_title.append(item.text)

for i in range(len(all_chapter_url)):
    res = requests.get(url=all_chapter_url[i])
    bsObj = BeautifulSoup(res.text, 'lxml')
    for content in bsObj.select('#content'):
        with open(s_keyword+'.txt', 'a') as f:
            print("Downloading %s" % all_chapter_title[i])
            f.write(all_chapter_title[i] + '\n\n' + content.text.replace('\n', '').replace('\xa0', '').replace('\u3000', '').replace('chaptererror();', '') + '\n\n')
