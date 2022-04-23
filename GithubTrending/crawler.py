from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re

URL = "http://github.com/trending"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

itemList = soup.select("article.Box-row")
pattern = re.compile(r"\s+")

for item in itemList:
    projectName = re.sub(pattern, "", item.select(".h3.lh-condensed")[0].text.strip())
    projectURL = f"https://github.com/{projectName}"
    starNumber = re.sub(pattern, "", item.select("a.Link--muted")[0].text)
    descriptionElement = item.select("p")
    programmingLanguageElement = item.select("[itemprop='programmingLanguage']")
    infoDict = {
        "名称": projectName,
        "链接地址":  projectURL,
        "简介": descriptionElement[0].text.strip() if len(descriptionElement) else "",
        "编程语言": programmingLanguageElement[0].text if len(programmingLanguageElement) else "",
        "总Star数": starNumber,
    }
    pprint(infoDict)