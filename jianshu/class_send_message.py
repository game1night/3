#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/11 18:28

@author: tatatingting
"""

import time

class send_message:

    def __init__(self, dr, num_scroll, quick=1, content=''):
        self.dr = dr
        self.num_scroll = num_scroll
        self.content = content
        self.quick = quick

    def run(self):
        start_time = time.time()
        n = 2

        # --- 导航到指定页面 ---
        self.dr.find_element_by_class_name('user').click()
        time.sleep(n)
        self.dr.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/ul/li[2]/div/a').click()
        time.sleep(n)
        # --- 开始扫平，进入循环列表 ---
        # 对视线内的用户进行操作
        for i in range(4, self.num_scroll, self.quick):
            print(i)
            # 滚屏几次
            if i > 10:
                # 刷新一次多出现9个
                for j in range(i // 9, 0, -1):
                    # print(j)
                    if j < 5:
                        self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(n)
                    elif j < 10:
                        self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    else:
                        self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)

            # 锁定目标
            path = '//*[@id="list-container"]/ul/li['+str(i)+']/a[1]/img'
            path1 = '//*[@id="list-container"]/ul/li['+str(i-2)+']/a[1]/img'
            # 目标进入视线
            self.dr.execute_script("arguments[0].scrollIntoView();",
                                   self.dr.find_element_by_xpath(path1))
            time.sleep(n)
            # 点击头像进入用户主页
            self.dr.find_element_by_xpath(path).click()
            time.sleep(n)
            # 寻找发送简信的按钮
            self.dr.find_element_by_link_text('发简信').click()
            # 输入框
            inbox = self.dr.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/form/textarea')
            inbox.clear()
            inbox.send_keys(self.content)
            time.sleep(1)
            # 点击发送
            self.dr.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/form/input').click()
            print('--- send!')
            time.sleep(1)
            # --- 返回循环列表 ---
            self.dr.back()
            self.dr.back()
            time.sleep(n)

        # 打印信息
        print('send_message done!')
        # --- 返航到首页 ---
        self.dr.find_element_by_class_name('logo').click()
        # --- 打印运行时间信息 ---
        end_time = time.time()
        print('time: {}'.format(end_time - start_time))
        return self.dr
