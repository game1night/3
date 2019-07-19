# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 19:12:51 2019

@author: tatatingting
"""

import os
from selenium import webdriver
import time


class login_js:

    def __init__(self, url='https://www.jianshu.com/sign_in',
                 account='your@mail',
                 password='password',
                 headless=False,
                 auto_input=True
                 ):
        driver_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        print(driver_path)
        self.drive = os.path.join(driver_path, 'chromedriver.exe')
        print(self.drive)
        self.url = url
        self.account = account
        self.password = password
        self.headless = headless
        self.auto_input = auto_input

    def run(self):

        # 配置司机
        if self.headless:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            dr = webdriver.Chrome(self.drive, chrome_options=options)
        else:
            dr = webdriver.Chrome(self.drive)
        # 加载网页
        dr.get('https://www.jianshu.com/sign_in')
        time.sleep(1)
        # 开始登陆
        if self.auto_input:
            # 1. 找用户名输入框
            account = dr.find_element_by_name('session[email_or_mobile_number]')
            account.clear()
            account.send_keys(self.account)
            # 2. 找密码输入框
            password = dr.find_element_by_name('session[password]')
            password.clear()
            password.send_keys(self.password)
            # 3. 点击登陆
            dr.find_element_by_class_name('sign-in-button').click()
            # 4. 验证码环节
            try:
                # 人工标注
                time.sleep(10)
                # 点击确认
                dr.find_element_by_class_name('geetest_commit').click()
            except:
                pass
        else:
            for i in range(30):
                print(30 - i)
                time.sleep(1)

        time.sleep(2)
        print('--- login ok')
        return dr
