# -*- coding: utf-8 -*-
"""
--------------------------------------
Project Name: 爬虫
File Name: Douyin.py
Author: Onway
Create Date: 2021/11/20
--------------------------------------
"""
import sys
from selenium.webdriver.common.keys import Keys
import requests   # 数据请求 第三方模块 pip install requests
import re  # 正则表达式模块
import os  # 文件操作模块
import time # 时间模块
from selenium import webdriver  # pip install selenium
fileName="D:\\douyinVideo"    #设置保存目录
def change_title(title):    #去除标题中的特殊词
    patten=re.compile(r"[\/\\\:\*\?\"\<\>\|\n]")
    newTitle=re.sub(patten,"_",title)
    return newTitle
driver=webdriver.Chrome()
def getnamepage(name):     #得到搜索用户结果网页
   driver.get('https://www.douyin.com/')
   search_box=driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/header/div[2]/div/div[1]/div/div[2]/div/form/input[1]')
   search_box.send_keys(name)
   search_box.send_keys(Keys.ENTER)
   time.sleep(1)
name=input("请输入你想爬取的用户")   #输入想爬取的用户
getnamepage(name)
driver.switch_to.window(driver.window_handles[1])
text=input("请手动通过滑块验证，否则程序无法正常运行，通过后输入yes")   #能力有限，滑块验证需要手动过 通过之后输入yes，进行下一步，输入其他程序终止
if text=="yes":
    pass
else:
    sys.exit()
time.sleep(3)
#因为抖音反爬 每次搜索后可能会随机出现两种网页模式，所以用try except 进行实验，得到正确的网页
try:
    ele1=driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[1]/div/div/span[3]').click()   #点击用户 获得用户搜索结果
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[3]/div[3]/ul/li[1]/a').click()       #点击搜索结果中第一个用户 打开用户主页
except:
    pass
try:
    ele1=driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[1]/div/div/span[2]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[3]/div[3]/ul/li[1]/a').click()
except:
    pass
driver.switch_to.window(driver.window_handles[2])
def drop_down(num):      #滚轮向下滑动到底部，滑动num次
    for x in range(num):
        time.sleep(1)
        j=x/9
        js='document.documentElement.scrollTop=document.documentElement.scrollHeight'
        driver.execute_script(js)
num=driver.find_element_by_css_selector('#root > div > div:nth-child(2) > div > div.Z-bTIPaS > div.knrjsN15 > div._8izJhzVW > div.tfdQqKjV.fxRoXi9C > span')
list_num=int(num.text)//10+1   #获取该用户的视频数量，每页个视频，计算需要爬取的页数，并滚动num次，加载出所有视频
drop_down(list_num)
list=driver.find_elements_by_css_selector("#root > div > div:nth-child(2) > div > div.Z-bTIPaS > div.knrjsN15 > div:nth-child(2) > ul li")
list_url=[li.find_element_by_css_selector("a").get_attribute("href") for li in list]   #获取用户所有的视频链接

header={
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        "cookie":"ttcid=932510bad4a34afc9c10e8e98e0070b815; ttwid=1|UI81cuisftwh5xMxnyf70Nn4uP7wvAS-54kYxWm7ncc|1637394497|762127dc8e7477e4e502b38e51874ab9efde614c34c9a02e9fd5275e6edd25f0; MONITOR_WEB_ID=4bb57299-459f-4aaa-98d8-e4aa5ec89052; passport_csrf_token_default=2173b5a6829719e084acffaf8c0ec5a1; passport_csrf_token=2173b5a6829719e084acffaf8c0ec5a1; __ac_nonce=061a73b90004a47e8bd4f; __ac_signature=_02B4Z6wo00f01Rb7ZzAAAIDB0NGZcsNvdzkW32OAACQc8MbQsVjSSKKOnDTs9YSNkWaCSaAsY08Vc1bwH6PyfBlmZUijU0c1mb355p.BeWY8PNRg1bFROIH-93ZLNVK77mjcL13phCfbmUp-0b; _tea_utm_cache_6383=undefined; douyin.com; home_can_add_dy_2_desktop=0; AB_LOGIN_GUIDE_TIMESTAMP=1638349715489; _tea_utm_cache_1300=undefined; s_v_web_id=verify_kwnb4cx1_4a8PJcBE_w45Q_4wHo_9JjR_HVjCfNDmwewT; odin_tt=753e2761ecf57e95419bd8e15d604bbfe7bd974b7c9e4670f85e0310ebeb44dd4f5b6edb086624182af1408ed1a6b6fcc71867ed452230bd8d697161edfa1034; msToken=iT88Rr_sor3QznLfQ6KrVU2LSwNqJuHngQauak6-vkxj5K9Vc07cQeIOxJOGU7d6Op90IAavT06ohtjyk8TrdIIlUNZqNSzg2NOrGZRQwkEsgTaotE_vEzkOJ78=; msToken=vBXMZbHBJAoHVGs040CuiN9OjePHbbL792h1lTWN_MqiK5wy_6BlnFJ_h7yqGf8zb_LgMZBu9XRiX5ueXlBLcu9ICJm4LZeqPb1kWpJNyh2j2yZjII_Avyw=; tt_scid=2hsrZRrPV5LOvkFoHH5nd9OkfoYqcHZSLSN5MM5tOZmBrp.DZmM7ZDVvvUcBAOEe7371"

}
for url in list_url:
    response0=requests.get(url=url,headers=header)
    # print(response0.text)
    title=re.findall('<title data-react-helmet="true"> (.*)</title>',response0.text)[0]    #获得视频标题
    new_title=change_title(title)
    viedo=re.findall("src(.*?)vr%3D%2",response0.text)[1]     #获得视频下载地址
    # print(viedo)
    video_url = requests.utils.unquote(viedo).replace('":"', 'http:')   #解码视频的下载地址
    viedo_content=requests.get(url=video_url,headers=header).content    #以二进制打开
    if not os.path.exists(path=fileName + "\\" + name):    #如果不存在该用户文件夹，创建新文件夹
        os.mkdir(fileName + "\\" +name)
    with open(fileName + "\\" + name +'\\'+ new_title + ".mp4", mode='wb') as f:
        f.write(viedo_content)                  #写入mp4文件
        video_Name=name+new_title+".mp4"+"已下载"
        print(video_Name)
        f.close()  #保存
driver.quit()  #退出浏览器

# header = {
#     "accept": "application/json, text/plain, */*",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "x-tt-logid": "202112011714590102120352092411FA08",
#     "x-tt-trace-host": "01d7d241de1496903e1a77bffdf7f3b7987a2a82345aa55740f8f73c41117fe9f31c81e2bda14b73396cee8c926b3d28bb9895f0f992e05e76f42bba0c9d55b920a001b6bac43332911a2643bc0bad29f0f78e1f44090f2acb83812d6fe4401bf5",
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
#     "cookie":"ttcid=932510bad4a34afc9c10e8e98e0070b815; ttwid=1|UI81cuisftwh5xMxnyf70Nn4uP7wvAS-54kYxWm7ncc|1637394497|762127dc8e7477e4e502b38e51874ab9efde614c34c9a02e9fd5275e6edd25f0; MONITOR_WEB_ID=4bb57299-459f-4aaa-98d8-e4aa5ec89052; passport_csrf_token_default=2173b5a6829719e084acffaf8c0ec5a1; passport_csrf_token=2173b5a6829719e084acffaf8c0ec5a1; __ac_nonce=061a73b90004a47e8bd4f; __ac_signature=_02B4Z6wo00f01Rb7ZzAAAIDB0NGZcsNvdzkW32OAACQc8MbQsVjSSKKOnDTs9YSNkWaCSaAsY08Vc1bwH6PyfBlmZUijU0c1mb355p.BeWY8PNRg1bFROIH-93ZLNVK77mjcL13phCfbmUp-0b; _tea_utm_cache_6383=undefined; douyin.com; home_can_add_dy_2_desktop=0; AB_LOGIN_GUIDE_TIMESTAMP=1638349715489; _tea_utm_cache_1300=undefined; s_v_web_id=verify_kwnb4cx1_4a8PJcBE_w45Q_4wHo_9JjR_HVjCfNDmwewT; odin_tt=753e2761ecf57e95419bd8e15d604bbfe7bd974b7c9e4670f85e0310ebeb44dd4f5b6edb086624182af1408ed1a6b6fcc71867ed452230bd8d697161edfa1034; msToken=iT88Rr_sor3QznLfQ6KrVU2LSwNqJuHngQauak6-vkxj5K9Vc07cQeIOxJOGU7d6Op90IAavT06ohtjyk8TrdIIlUNZqNSzg2NOrGZRQwkEsgTaotE_vEzkOJ78=; msToken=vBXMZbHBJAoHVGs040CuiN9OjePHbbL792h1lTWN_MqiK5wy_6BlnFJ_h7yqGf8zb_LgMZBu9XRiX5ueXlBLcu9ICJm4LZeqPb1kWpJNyh2j2yZjII_Avyw=; tt_scid=2hsrZRrPV5LOvkFoHH5nd9OkfoYqcHZSLSN5MM5tOZmBrp.DZmM7ZDVvvUcBAOEe7371"
# }
# data = {
#     "sec_uid": "MS4wLjABAAAAlwXCzzm7SmBfdZAsqQ_wVVUbpTvUSX1WC_x8HAjMa3gLb88-MwKL7s4OqlYntX4r",
#     "count": "21",
#     "max_cursor": "0",
#     "aid": "1128",
#     "_signature": "1rexVRAciIE-bZMoZ46qv9a3sU",
#     "dytk": "96ad80961288263ad9d1cff2895d0636"
# }
# url="https://www.douyin.com/user/MS4wLjABAAAAlwXCzzm7SmBfdZAsqQ_wVVUbpTvUSX1WC_x8HAjMa3gLb88-MwKL7s4OqlYntX4r?enter_from=general_search&enter_method=general_search&extra_params=%7B%22search_params%22%3A%7B%22search_type%22%3A%22general%22%2C%22search_id%22%3A%22202112011710410102120420514910C64F%22%2C%22search_keyword%22%3A%22%E7%BD%97%E6%B0%B8%E6%B5%A9%22%2C%22search_result_id%22%3A%224195355415549012%22%7D%7D"
# response = requests.get(url, headers=header)
# data0 = response.text.encode().decode('utf-8')
# print(data0)
# pattern = re.compile('"(https://aweme.snssdk.com/aweme/v1/play/.*?)"')
# result = pattern.findall(data0)
# print(result)
# result = [i.split("&ratio")[0] for i in result]
# result2 = [i.replace("/play/", "/playwm/") for i in result]
#
# for i in result:
#     print(i)
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
# }
# if not os.path.exists("无水印"):
#     os.mkdir("无水印")
# if not os.path.exists("水印"):
#     os.mkdir("水印")
#
# count = 0
# # for res1 in result:
# #     count += 1
# #     videoBin = requests.get(res1, timeout=5, headers=headers)
# #     with open(f'无水印/{count}.mp4', 'wb') as fb:
# #         fb.write(videoBin.content)
#
# for res2 in result2:
#     count += 1
#     videoBin = requests.get(res2, timeout=5, headers=headers)
#     with open(f'水印/{count}.mp4', 'wb') as fb:
#         fb.write(videoBin.content)