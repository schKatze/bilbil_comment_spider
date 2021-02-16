import requests
import xlsxwriter
import jieba
import re
import wordcloud  # 导入词云库
import numpy as np
import matplotlib.pyplot as plt
import PIL
import json

comments = []
header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0",
          "Cookie": ""}
stop_word = []
fd = open("停用词表.txt", "r", encoding='utf-8')
for line in fd.readlines():
    stop_word += str(line).strip('\n').split(',')
fd.close()

pattern = re.compile(r'[\u4e00-\u9fa5]')
jieba.load_userdict('自定义词库.txt')


# pn=页码
def request_data():
    for p in range(5):
        url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid=48487753&sort=2'.format(p + 1)
        html = requests.get(url, headers=header)
        comments_data = json.loads(html.text)['data']['replies']
        for i in comments_data:
            comments.append(i['content']['message'])
    # print(comments)

    workbook = xlsxwriter.Workbook(r'D:\mypython\spider_1\评论爬取.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A2', comments)
    workbook.close()
    return comments


def fenci2(list1):
    seg_list = ''
    for i in range(len(list1)):
        words_list = jieba.cut(list1[i], cut_all=False)
        for i in words_list:
            if pattern.match(i) and i not in stop_word:
                seg_list += i
                seg_list += ' '
    return seg_list


if __name__ == '__main__':
    request_data()
    corpus_list = fenci2(comments)
    image1 = PIL.Image.open(r'鬼灭.jpg')
    MASK = np.array(image1)
    WC = wordcloud.WordCloud(font_path='C:\\Windows\\Fonts\\STFANGSO.TTF', max_words=1000, mask=MASK, height=800,
                             width=800, background_color='white', repeat=False, mode='RGBA')  # 设置词云图对象属性
    con = WC.generate(corpus_list)
    plt.imshow(con)
    plt.axis("off")
    WC.to_file('词云图2.png')
