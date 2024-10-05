# coding=utf-8
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time,pandas,os,re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

"""
aqistudy:
failed :
unable to get real tables of the data
may use javascript to hide the real table
"""
class aqistudy():
   def __init__(self,city):
       self.url = "https://www.aqistudy.cn/"
       self.city = city
       self.WholeUrl = ""


   def get_weather_table(self):
      """
      伪装浏览器访问，反爬
      :pram url:get weather 所需的网址
      :return:返回空气质量表格
      """
      option = ChromeOptions()
      option.add_experimental_option('excludeSwitches', [ 'enable-automation' ])
      option.add_experimental_option('useAutomationExtension', False)
      browser = webdriver.Chrome(options=option)
      browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
         'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
      })

      browser.get(self.WholeUrl)
      # browser.set_window_size(500, 500)
      time.sleep(0.3)
      browser.refresh()
      time.sleep(1)
      # averange min time

      table = pandas.read_html(browser.page_source) [ 0 ]
      browser.quit()
      return table

   def __save_table(self,table,date):
      path = "data/city/"
      path = path.replace("city", self.city)
      if not os.path.exists(path):
         os.makedirs(path)
      base_name = "city_month.csv"
      save_name = base_name.replace("city", self.city, 3)
      save_name = save_name.replace("month", date)
      table.to_csv(path + save_name, "a", index=None)

   def __get_date(self):
      url = "https://www.aqistudy.cn/historydata/monthdata.php?city=" + self.city
      month_list = [ ]
      """
         伪装浏览器访问，反爬
         :pram url:get weather 所需的网址
         :return:返回空气质量表格
         """
      option = ChromeOptions()
      option.add_experimental_option('excludeSwitches', [ 'enable-automation' ])
      option.add_experimental_option('useAutomationExtension', False)
      browser = webdriver.Chrome(options=option)
      browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
         'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
      })

      browser.get(url)
      time.sleep(2)
      month_table = pandas.read_html(browser.page_source) [ 0 ]
      for i in range(0, month_table.shape [ 1 ]):
         if type(month_table.iloc [ 2, i ]) == str:
            for j in range(1, month_table.shape [ 0 ]):
               month_list.append(month_table.iloc [ j, i ])
         else:
            pass
      browser.quit()
      return month_list

   def get_all_save(self):
      month_list = self.__get_date()
      base_url = "https://www.aqistudy.cn/historydata/daydata.php?city=" + self.city + "&month="
      for i in month_list:
         self.WholeUrl = base_url + i
         table = self.__get_weather_table()
         self.__save_table(table,i)



class HoubaoWeather():
   def __init__(self,city):
      self.url = 'http://tianqihoubao.com'
      self.city = city
      self.headers = {"Host": "www.tianqihoubao.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate",
"Referer": "http://www.tianqihoubao.com/aqi/",
"Connection": "keep-alive",
"Cookie": "ASP.NET_SessionId=me5kxf552je0mquffg0i3t45",
"Upgrade-Insecure-Requests": "1",
"Priority": "u=0, i"}


   def __get_date(self):
       url = "http://www.tianqihoubao.com/aqi/city.html".replace("city", self.city)
       response = requests.get(url,headers = self.headers)
       response.encoding = 'utf-8'
       html = etree.HTML(response.text)
       date_list = html.xpath('/html/body/form/div[2]/div[7]/div[1]/div[3]/ul/li/a/@href')
       return date_list

   def get_table(self,date):
      count = 1
      return_list = []
      _list = []
      url = self.url + date

      option = ChromeOptions()
      option.add_experimental_option('excludeSwitches', [ 'enable-automation' ])
      option.add_experimental_option('useAutomationExtension', False)
      browser = webdriver.Chrome(options=option)
      browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
         'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
      })
      desired_capabilities = DesiredCapabilities.CHROME
      desired_capabilities [ "pageLoadStrategy" ] = "eager"
      browser.get(url)
      time.sleep(5)
      table = pandas.read_html(browser.page_source) [ 0 ]
      browser.quit()
      return table

   def __save_table(self,table,date):
      path = "data/city/"
      path = path.replace("city", self.city)
      pattern = r'\d+'
      match = re.findall(pattern, date)[0]
      if not os.path.exists(path):
         os.makedirs(path)
      base_name = "city_month.csv"
      save_name = base_name.replace("city", self.city, 3)
      save_name = save_name.replace("month", match)
      table.to_csv(path + save_name, "a", index=None)

   def get_all_save(self):
      month_list = self.__get_date()
      for date in range(len(month_list)-1):
         table = self.get_table(month_list[date+1])
         self.__save_table(table,date)




if __name__ != '__main__':
    pass
else:
   a = HoubaoWeather("xian")
   a.get_all_save()