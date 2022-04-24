import requests
from bs4 import BeautifulSoup
import config
from pprint import pprint

URL = "https://s.weibo.com/top/summary?cate=realtimehot"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Cookie': config.Cookie,
           }
response = requests.get(URL, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

itemList = soup.select("#pl_top_realtimehot tbody tr")

for item in itemList:
    relativeLinkAddress = item.select("td.td-02 a")[0].attrs['href']
    hotNumberElement = item.select("td.td-02 span")
    infoDict = {
        "标题": item.select("td.td-02 a")[0].text.strip(),
        "链接地址": f"https://s.weibo.com/{relativeLinkAddress}",
        "热搜指数": hotNumberElement[0].text.strip() if len(hotNumberElement) else "",
    }
    pprint(infoDict)