import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://www.bilibili.com/v/popular/rank/all"

response = requests.get(URL)

soup = BeautifulSoup(response.text, "lxml")

itemList = soup.select(".rank-container .rank-item")

for item in itemList:
    infoDict = {
        "标题": item.select(".title")[0].text,
        "链接地址": f'https:{item.select(".title")[0].attrs["href"]}',
        "UP名": item.select(".data-box.up-name")[0].text.strip(),
        "UP首页": f'https:{item.select(".detail a")[0].attrs["href"]}',
        "播放量": item.select(".detail-state span:nth-child(1)")[0].text.strip(),
        "评论数": item.select(".detail-state span:nth-child(2)")[0].text.strip(),

    }
    pprint(infoDict)
