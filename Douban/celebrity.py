import os
import time
import random
import requests
from bs4 import BeautifulSoup
from scipy import rand

celebrity_id = '1265872'
save_dir = 'picture'
url_celebrity_photos = 'https://movie.douban.com/celebrity/{0}/photos/'.format(celebrity_id)

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
}

res = requests.get(url_celebrity_photos, headers=headers).text
content = BeautifulSoup(res, 'html.parser')
data = content.find_all('div', attrs={'class': 'cover'})

# 照片总数
pic_count = int(content.find('span', attrs={'class': 'count'}).text[2:-2])
page_num = 1
pic_num = 1
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# 遍历照片列表页
for i in range(0, pic_count, 30):
    print('\nCrawling page {0} photos...\n'.format(page_num))
    page_num += 1
    # https://movie.douban.com/celebrity/1265872/photos/?type=C&start=30&sortby=like&size=a&subtype=a
    url_photos_list = url_celebrity_photos + '?type=C&start={0}&sortby=like&size=a&subtype=a'.format(i)
    res = requests.get(url_photos_list, headers=headers).text
    content = BeautifulSoup(res, 'html.parser')
    data = content.find_all('div', attrs={'class': 'cover'})
    # 获取本页照片的url列表（每页30个，但此url不是高清的原图)
    # https://img1.doubanio.com/view/photo/m/public/p1876623207.jpg
    picture_list = []
    for d in data:
        list_item = d.find('img')['src']
        picture_list.append(list_item)
    # 下载本照片列表页图片的原图
    for pic_url_origin in picture_list:
        pic_name = pic_url_origin[46:]
        pic_id = pic_name[1:11]
        # 跳过已下载的图片
        if os.path.exists(save_dir + '/' + pic_name):
            pic_num += 1
            continue
        # referer 照片详情页
        headers['referer'] = url_celebrity_photos + pic_id + '/'
        # 原图url 
        # https://img1.doubanio.com/view/photo/raw/public/p1876623207.jpg
        pic_url_hd = pic_url_origin[:37] + 'raw' +  pic_url_origin[38:]
        print('Donwloading {0}/{1}: {2}'.format(pic_num , pic_count, pic_url_hd))
        pic = requests.get(pic_url_hd, headers=headers)
        with open('picture/'+ pic_name , 'wb') as f:
            f.write(pic.content)
        # 休眠时间，防止被封。 random()返回[0,1)之间的float 
        time.sleep(1 + random.random()*3)
        pic_num += 1