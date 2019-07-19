#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/8 17:03

@author: tatatingting
"""

from selenium import webdriver
import time

# ================================================================================
# # 声明一个司机，司机是个Chrome类的对象
# driver = webdriver.Chrome()
#
# # 让司机加载一个网页
# driver.get("http://demo.ranzhi.org")
#
# # 给司机3秒钟去打开
# sleep(3)
#
# # 开始登录
# # 1. 让司机找用户名的输入框
# we_account = driver.find_element_by_css_selector('#account')
# we_account.clear()
# we_account.send_keys("demo")
#
# # 2. 让司机找密码的输入框
# we_password = driver.find_element_by_css_selector('#password')
# we_password.clear()
# we_password.send_keys("demo")
#
# # 3. 让司机找 登录按钮 并 单击
# driver.find_element_by_css_selector('#submit').click()
# sleep(3)
# ================================================================================


options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome("./chromedriver", chrome_options=options)

browser.get("https://www.jianshu.com/")

for i in range(3):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# print(browser)
for j in range(3):
    try:
        button = browser.execute_script("var a = document.getElementsByClassName('load-more'); a[0].click();")
        time.sleep(2)
    except:
        pass
#
titles = browser.find_elements_by_class_name("title")
with open("./data/article_0.txt", "w", encoding="utf-8") as f:
    for t in titles:
        try:
            f.write(t.text + " " + t.get_attribute("href"))
            f.write("\n")
        except TypeError:
            pass

browser.close()
