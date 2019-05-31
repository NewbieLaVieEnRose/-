# -* coding: utf-8 *-
# 爬取链家天津全部二手房的详细信息，并将爬取的数据存储到CSV文

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent

class LianjiaSpider(object):

    def __init__(self):
        self.headers = {"User-Agent": UserAgent().random}
        self.datas = list()

    # 提取最大页码
    def getMaxPage(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            source = response.text
            soup = BeautifulSoup(source, "html.parser")
            pageData = soup.find("div", class_="page-box house-lst-page-box")["page-data"]
            maxPage = eval(pageData)["totalPage"]
            return maxPage
        else:
            print("Fail status: {}".format(response.status_code))
            return None


    def parsePage(self, url):
        maxPage = self.getMaxPage(url)
        #  解析每个page，获取每个二手房的链接
        for pageNum in range(1, maxPage+1 ):
            url_temp = url+"pg{}/".format(pageNum)
            print("当前正在爬取: {}".format(url_temp))
            net_status = False
            while not net_status:
                try:
                    response = requests.get(url_temp, headers=self.headers, timeout=5)
                    net_status = True
                except Exception as e:
                    print(e)
                    net_status = False

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("div", class_="info clear")
            for i in links:
                link = i.find("a")["href"]    #每个<info clear>标签有很多<a>,而我们只需要第一个，所以用find
                detail = self.parseDetail(link)
                self.datas.append(detail)

        #  将所有爬取的二手房数据存储到csv文件中
        data = pd.DataFrame(self.datas)
        # columns字段：自定义列的顺序（DataFrame默认按列名的字典序排序）
        columns = ["小区", "户型", "面积", "价格", "单价", "朝向", "位置", "地铁"]
        data.to_csv(".\Lianjia_xiqing.csv", encoding='utf_8_sig', index=False, columns=columns)


    def parseDetail(self, url):
        response = requests.get(url, headers=self.headers)
        detail = {}
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            detail["价格"] = soup.find("span", class_ = "total").text
            detail["单价"] = soup.find("span", class_ = "unitPriceValue").text
            detail["小区"] = soup.find("div", class_ = "communityName").find("a", class_ = "info").text
            detail["位置"] = soup.find("div", class_="areaName").find("span", class_="info").text
            detail["地铁"] = soup.find("div", class_="areaName").find("a", class_="supplement").text
            base = soup.find("div", class_ = "base").find_all("li") # 基本信息
            detail["户型"] = base[0].text[4:]
            detail["面积"] = base[2].text[4:]
            detail["朝向"] = base[6].text[4:]
            return detail
        else:
            return None

if __name__ == "__main__":
    Lianjia = LianjiaSpider()
    Lianjia.parsePage("https://tj.lianjia.com/ershoufang/xiqing/")