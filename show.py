import pymysql
import re
import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup

# 院校列表
URL_DICT = {
    'ZGKXY': 'forum-83-1.html',
    'QINGHUA': 'forum-84-1.html',
    'BEIDA': 'forum-85-1.html',
    'BEIHANG': 'forum-86-1.html',
    'HAGONGDA': 'forum-79-1.html',
    'DBDX': 'forum-80-1.html',
    'BEIYOU': 'forum-87-1.html',
    'JLDX': 'forum-81-1.html',
    'BEILI': 'forum-90-1.html',
    'SDDX': 'forum-93-1.html',
    'TJDX': 'forum-91-1.html',
    'DLLGDX': 'forum-82-1.html',
    'NKDX': 'forum-92-1.html',
    'BGD_BKD_BJD': 'forum-89-1.html',
    'RENDA_BEISHI': 'forum-88-1.html',
    'HEBGCDX': 'forum-231-1.html',
    'ZGHYDX': 'forum-281-1.html',
    'HB_HD_OTHER': 'forum-277-1.html',
    'SHANGJIAO': 'forum-95-1.html',
    'FUDAN': 'forum-98-1.html',
    'TONGJI': 'forum-99-1.html',
    'ZHEDA': 'forum-94-1.html',
    'ZGKXJSDX': 'forum-97-1.html',
    'GFKJDX': 'forum-121-1.html',
    'HUAKE': 'forum-102-1.html',
    'WHDX': 'forum-103-1.html',
    'DNDX': 'forum-100-1.html',
    'NJDX': 'forum-96-1.html',
    'ZNDX': 'forum-104-1.html',
    'HNDX': 'forum-105-1.html',
    'ZSDX': 'forum-106-1.html',
    'HNLGDX': 'forum-107-1.html',
    'HDLGDX_HDSFDX': 'forum-138-1.html',
    'XMDX_FZDX_NCDX': 'forum-272-1.html',
    'NJLG_NJHK_NJYD': 'forum-288-1.html',
    'WHLG_HZSD_HNSD': 'forum-274-1.html',
    'ZD_AD_SD_SD_HD': 'forum-276-1.html',
    'HZ_HD_HN_OTHER': 'forum-275-1.html',
    'XAJTDX': 'forum-108-1.html',
    'DZKJDX': 'forum-113-1.html',
    'XADZKJDX': 'forum-110-1.html',
    'XBGYDX': 'forum-109-1.html',
    'SCDX': 'forum-112-1.html',
    'CQDX': 'forum-111-1.html',
    'XB_XN_OTHER': 'forum-273-1.html'
}

NAME_DICT = {
    'ZGKXY': '中科院',
    'QINGHUA': '清华大学',
    'BEIDA': '北京大学',
    'BEIHANG': '北航',
    'HAGONGDA': '哈工大',
    'DBDX': '东北大学',
    'BEIYOU': '北邮',
    'JLDX': '吉林大学',
    'BEILI': '北理',
    'SDDX': '山东大学',
    'TJDX': '天津大学',
    'DLLGDX': '大连理工大学',
    'NKDX': '南开大学',
    'BGD_BKD_BJD': '北工/北科/北交',
    'RENDA_BEISHI': '人大/北京师范',
    'HEBGCDX': '哈尔滨工程大学',
    'ZGHYDX': '中国海洋大学',
    'HB_HD_OTHER': '华北/东北其他',
    'SHANGJIAO': '上海交通大学',
    'FUDAN': '复旦大学',
    'TONGJI': '同济大学',
    'ZHEDA': '浙江大学',
    'ZGKXJSDX': '中国科学技术大学',
    'GFKJDX': '国防科技大学',
    'HUAKE': '华中科技大学',
    'WHDX': '武汉大学',
    'DNDX': '东南大学',
    'NJDX': '南京大学',
    'ZNDX': '中南大学',
    'HNDX': '湖南大学',
    'ZSDX': '中山大学',
    'HNLGDX': '华南理工大学',
    'HDLGDX_HDSFDX': '华东理工/华东师范',
    'XMDX_FZDX_NCDX': '厦大/福大/南昌大学',
    'NJLG_NJHK_NJYD': '南理/南航/南邮',
    'WHLG_HZSD_HNSD': '武汉理/华中师/华南师',
    'ZD_AD_SD_SD_HD': '郑大/安大/苏大/上大/杭电',
    'HZ_HD_HN_OTHER': '华中/华东/华南其他',
    'XAJTDX': '西安交通大学',
    'DZKJDX': '电子科技大学',
    'XADZKJDX': '西安电子科技大学',
    'XBGYDX': '西北工业大学',
    'SCDX': '四川大学',
    'CQDX': '重庆大学',
    'XB_XN_OTHER': '西北/西南其他高校'
}

# 结果字典
RESULT_DICT = {}

# 使用pymysql进行数据库连接
conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='cskaoyan', charset='utf8')
cur = conn.cursor()

# bs4
URL = "http://www.cskaoyan.com/forum.php"
URL_DATA = requests.get(URL).text
SOUP = BeautifulSoup(URL_DATA, 'html.parser')

for u in NAME_DICT:
    result_list = []
    # 查询最近一天的热度
    sql1 = "SELECT " + u + " FROM wangdao ORDER BY PK_id DESC LIMIT 1"
    cur.execute(sql1)
    count_yesterday = cur.fetchone()[0]
    # 查询历史热度总和
    sql2 = "SELECT sum(" + u + ") FROM wangdao"
    cur.execute(sql2)
    count_all = cur.fetchone()[0]
    result_list.append(count_all)
    result_list.append(count_yesterday)
    parent_tag = SOUP.find('a', href=URL_DICT[u]).parent
    count_tag = parent_tag.find(class_="xw0 xi1")
    if count_tag != None:
        count_today = re.findall(r'\d+', count_tag.text)[0]
        count_today = int(count_today)
    else:
        count_today = 0
    result_list.append(count_today)
    RESULT_DICT[u] = result_list

SORTED_RESULT = sorted(RESULT_DICT.items(), key = lambda k: k[1], reverse=True)
# print(SORTED_RESULT)

# 格式化输出
table = PrettyTable(['大学', '昨日热度', '今日热度', '历史热度'])
for n in SORTED_RESULT:
    table.add_row([NAME_DICT[n[0]], n[1][1], n[1][2], n[1][0]+n[1][2]])

print(table)
# 释放数据库连接
cur.close()
conn.close()