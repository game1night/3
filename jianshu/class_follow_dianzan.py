#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/11 13:47

@author: tatatingting
"""

import time
import os

class follow_dianzan:

    def __init__(self, dr, counts):
        self.dr = dr
        self.counts = counts
        self.path = os.path.dirname(os.path.realpath(__file__))

        # 读取历史信息
        user_list_old = []
        with open(os.path.join(self.path, 'data', 'user_list.txt'), 'r', encoding='utf-8-sig') as f:
            for line in f.readlines():
                user_list_old.append(line.strip())
        self.user_list = user_list_old

    def run(self):
        start_time = time.time()
        n = 2
        user_list_new = []

        # --- 导航到指定页面 ---
        self.dr.find_element_by_class_name('ic-navigation-notification').click()
        time.sleep(n)
        # self.dr.find_element_by_link_text('喜欢和赞').click()
        self.dr.execute_script("var a = document.getElementsByClassName('ic-likes'); a[0].click();")
        time.sleep(n)

        # --- 消灭红点点 ---
        # if len(self.dr.find_element_by_class_name('badge')) > 0:
        #     pass
        # '/html/body/div/div/div[2]/div/ul/li[1]/div/a[1]'
        # '/html/body/div/div/div[2]/div/ul/li[2]/div/a[1]'
        # '/html/body/div/div/div[2]/div/ul/li[10]/div/a[1]'
        # 观察列表

        # 存储信息
        def update_user_list(user_list_new):
            try:
                # 存储新增信息
                if len(user_list_new) > 0:
                    with open(os.path.join(self.path, 'data', 'user_list.txt'), 'a', encoding='utf-8-sig') as f:
                        n_i = 0
                        for user_new in user_list_new:
                            f.write('\n')
                            f.write(str(user_new))
                            n_i += 1
                            print('new', n_i)
            except:
                pass

        for count in range(1, self.counts+1):
            # 翻页
            if count > 1:
                try:
                    self.dr.find_element_by_link_text('下一页').click()
                    time.sleep(n)
                except:
                    print('翻页失败。')
            else:
                time.sleep(n)
            # 查找
            for i in range(1, 11):
                try:
                    user_link = ''
                    path = '/html/body/div/div/div[2]/div/ul/li['+str(i)+']/div/a[1]'
                    user = self.dr.find_element_by_xpath(path)
                    user_link = user.get_attribute('href')
                    if user_link in self.user_list:
                        # print('pass', i, count, user_link)
                        continue
                    else:
                        user.click()
                        time.sleep(n)
                        # 匹配
                        print(len(self.user_list), i, count, user_link)
                        try:
                            # 关注之
                            self.dr.execute_script("var a = document.getElementsByClassName('off  user-follow-button');"
                                                   "a[0].click();")
                            time.sleep(1)
                            # print('--- follow!')
                            # 新增一项
                            self.user_list.append(user_link)
                            user_list_new = [user_link]
                            update_user_list(user_list_new)
                        except:
                            try:
                                self.dr.execute_script("var a = document.getElementsByClassName('on  user-follow-button');"
                                                       "a[0].click();")
                                print('点了却是已关注')
                            except:
                                print('没有成功！')
                            try:
                                time.sleep(n)
                                self.dr.execute_script("var a = document.getElementsByClassName('off  user-follow-button');"
                                                       "a[0].click();")
                                time.sleep(1)
                                # print('--- follow!')
                                # 新增一项
                                self.user_list.append(user_link)
                                user_list_new = [user_link]
                                update_user_list(user_list_new)
                            except:
                                print('关注失败。')

                        # 返航
                        self.dr.back()
                        time.sleep(n)
                        # 翻页
                        for fanye in range(count):
                            self.dr.find_element_by_link_text('下一页').click()
                            time.sleep(n)



                except:
                    pass

        print('关注那些给我点赞的 done! 正在返航。。。')


        # --- 返航到首页 ---
        self.dr.find_element_by_class_name('logo').click()
        end_time = time.time()
        print('time: {}'.format(end_time - start_time))

        return self.dr
