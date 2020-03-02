# -*- conding: utf-8 -*-

"""
运行前需要下载第三方库 pixabay
pip install python-pixabay
"""

import os
import requests
from pixabay import Image

# 这是我的 API_KEY 仅供测试用
API_KEY = "12529361-78722cf76d163c8adc77d4e0c"

def get_image(keyword="食物", per_page=20):
    # 默认下载 20 张图
    image = Image(API_KEY)
    image.search()
    ims = image.search(q=keyword,
                 lang='zh',
                 image_type='photo',
                 safesearch='true',
                 order='latest',
                 page=1,
                 per_page=per_page)
    return ims
	

def download_image(image_url):
    # 下载图片到根目录的 Pic/ 文件夹
    if not os.path.exists('./Pic/'):
        os.mkdir(path='./Pic/')
    response = requests.get(image_url)
    filename = image_url.split('/')[-1]
    with open('./Pic/'+filename, 'wb+') as f:
        f.write(response.content)
		
	
if __name__ == '__main__':
    ims = get_image()
    for i, eve_url in enumerate(ims['hits']):
        download_image(eve_url['largeImageURL'])
        print("小黄图+1, 已有 {} 张".format(i+1))