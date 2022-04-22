from pprint import pprint
import requests
from bs4 import BeautifulSoup

URL = "https://top.baidu.com/board?tab=realtime"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

itemList = soup.select("div.category-wrap_iQLoo.horizontal_1eKyQ")

for item in itemList:
    infoDict = {
        "标题": item.select("div.c-single-text-ellipsis")[0].text.strip(),
        "链接地址": item.select("a.title_dIF3B")[0].attrs['href'],
        "简介": item.select("div.hot-desc_1m_jR.small_Uvkd3")[0].text.strip(),
        "热搜指数": item.select("div.hot-index_1Bl1a")[0].text.strip(),
    }
    pprint(infoDict)