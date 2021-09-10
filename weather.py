# 天气网余姚地区爬虫案例
import requests
from lxml import etree


class WeatherSpider:

    def __init__(self):
        #self.url = "http://www.weather.com.cn/weather/101280101.shtml"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    def init_url(self,URL):
        self.url = URL

    def get_url_content(self):
        return requests.get(self.url, headers=self.headers).content.decode()

    def get_weather_data(self, html):
        tmp_html = etree.HTML(html)
        tomorrow_doc = tmp_html.xpath("//div[contains(@class,'con') and contains(@class,'today')]//div[@class='c7d']/ul/li[2]")[0]
        weather_data = {}
        weather_data["date"] = tomorrow_doc.xpath("./h1/text()")[0]
        weather_data["weather"] = tomorrow_doc.xpath("./p[@class='wea']/@title")[0]
        weather_data["temperature_max"] = tomorrow_doc.xpath("./p[@class='tem']/span/text()")[0]
        weather_data["temperature_min"] = tomorrow_doc.xpath("./p[@class='tem']/i/text()")[0]
        weather_data["air_speed"] = tomorrow_doc.xpath("./p[@class='win']/i/text()")[0]
        return weather_data

    # def run(self):
    #     # 获取url请求内容
    #     content_html = self.get_url_content()
    #     # 根据url内容获取天气数据
    #     data = self.get_weather_data(content_html)
    #     # 打印爬取的天气数据
    #     print(data)

    def result(self):
        # 获取url请求内容
        content_html = self.get_url_content()
        # 根据url内容获取天气数据
        data = self.get_weather_data(content_html)
        # 打印爬取的天气数据
        return data
