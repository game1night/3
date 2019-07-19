#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/10 8:27

@author: tatatingting
"""

import time
import os


class follow_back:

    def __init__(self, dr, num_scroll, num_followers=700):
        self.dr = dr
        self.num_scroll = num_scroll
        self.user_list = []
        self.num_followers = num_followers
        self.path = os.path.dirname(os.path.realpath(__file__))

    def run(self):
        start_time = time.time()
        n = 2
        c = 0
        c1 = 0

        time.sleep(n)
        self.dr.execute_script("window.stop()")

        # --- 导航到指定页面 ---
        self.dr.find_element_by_class_name('user').click()
        time.sleep(n)
        self.dr.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/ul/li[2]/div/a').click()
        time.sleep(n)
        # --- 开始扫射 ---
        for scroll in range(self.num_scroll):
            # print(scroll)
            # 寻找关注目标
            wait_follow = self.dr.find_elements_by_link_text('关注')
            if len(wait_follow) > 0:
                m = len(wait_follow)
                try:
                    for j in range(m):
                        # 关注之
                        wait_follow[j].click()
                        time.sleep(n)
                        print('--- follow! {}'.format(j))
                except:
                    pass

            # 滚动多次平铺出目标（性能有待提高）
            names = self.dr.find_elements_by_class_name('avatar')
            c = len(names)
            print(c)

            if (c // 20 == 1) or (c // 50 == 1) or (c // 50 == 5) or (c // 50 == 7) or (c // 50 == 9) or (c // 50 == 14):
                try:
                    # 收集信息
                    for i in range(c):
                        names_link = names[i].get_attribute('href')
                        if names_link in self.user_list:
                            continue
                        else:
                            self.user_list.append(names_link)

                    # 读取历史信息
                    user_list_old = []
                    with open(os.path.join(self.path, 'data', 'user_list.txt'), 'r', encoding='utf-8-sig') as f:
                        for line in f.readlines():
                            user_list_old.append(line.strip())

                    # 对比历史信息
                    user_list_new = []
                    for user in self.user_list:
                        if user in user_list_old:
                            continue
                        else:
                            user_list_new.append(user)

                    # 存储新增信息
                    if len(user_list_new) > 0:
                        with open('./snippets/spider/jianshu/' + 'data/user_list.txt', 'a', encoding='utf-8-sig') as f:
                            n_i = 0
                            for i in user_list_new:
                                f.write('\n')
                                f.write(str(i))
                                n_i += 1
                                print('new', n_i)
                except:
                    pass

            if c != c1:
                # 滚动出更多潜在目标
                self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # print('0')
            else:
                # 扫描目标
                # 移动元素进入视线(另可以通过定位滚动条actionchain的方式实现）
                time.sleep(n)
                try:
                    self.dr.execute_script("arguments[0].scrollIntoView();",
                                       self.dr.find_elements_by_class_name('avatar')[c+1])

                except:
                    break

            c1 = c

        print('回粉 done!')
        # --- 返航到首页 ---
        self.dr.find_element_by_class_name('logo').click()
        end_time = time.time()
        print('time: {}'.format(end_time - start_time))

        return self.dr
