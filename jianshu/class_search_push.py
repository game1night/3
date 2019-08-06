#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/9 12:42

@author: tatatingting
"""


from selenium import webdriver
import time
import random
import class_article

class search_push:

    def __init__(self, dr='dr', key='素描', num_zhuanti=1, counts=10, dianzan=True, push=True, follow=True,
                 comment_dianzan=True, comment=False):

        self.dr = dr

        # ------ 个性化操作 -------
        self.key = key
        # 确定收录专题是第几个
        self.num_zhuanti = num_zhuanti
        # 确定翻页次数
        self.counts = counts
        # 确定是否点赞
        self.dianzan = dianzan
        # 确定是否收录
        self.push = push
        # 确定是否关注
        self.follow = follow
        # 给评论点赞
        self.comment_dianzan = comment_dianzan
        # 增加一条评论
        self.comment = comment

    def run(self):
        start_time = time.time()

        n = 2
        # -------搜索结果----------
        # 找到输入框，输入关键词
        inbox = self.dr.find_element_by_class_name('search-input')
        inbox.clear()
        inbox.send_keys(self.key)
        # 点击搜索按钮，得到新页面
        self.dr.find_element_by_class_name('search-btn').click()
        time.sleep(n)
        print('--- 成功搜索')

        # -------筛选排序-----------
        # 切换到某页面
        windows = self.dr.window_handles
        # print(windows)
        self.dr.switch_to.window(windows[1])
        time.sleep(n*n)
        # 按照最近时间排序
        # 点击一次时间排序
        self.dr.execute_script("var a = document.getElementsByClassName('v-select-wrap');a[0].click();")
        time.sleep(n)
        # 选择“最近一天”
        self.dr.execute_script("var a = document.getElementsByClassName('v-select-options-item');a[2].click();")
        time.sleep(n)
        # print('--- 成功筛选')
        # ----------翻页+收录--------------------
        # 遇到过搜索为0的情况
        try:
            for c in range(10):
                # 滚屏到底下
                self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                # --- 打印信息
                # print('--- fanye', c)
                # ------------------收录文章------------------------
                self.dr = class_article.article(num_zhuanti=self.num_zhuanti,
                                                dr=self.dr,
                                                dianzan=self.dianzan,
                                                push=self.push,
                                                follow=self.follow,
                                                comment_dianzan=self.comment_dianzan,
                                                comment=self.comment,
                                                flag_counts=self.counts).run()

                # -------------------下一页-----------
                try:
                    self.dr.find_element_by_link_text('下一页').click()
                    time.sleep(n)
                except:
                    pass
        except:
            print('no result at all!')

        print('--- search push ok')
        # --- 返航到首页 ---
        # self.dr.find_element_by_class_name('logo').click()
        # 关闭该页面
        self.dr.close()
        time.sleep(n)
        # 切换到某页面
        windows = self.dr.window_handles
        print(windows)
        self.dr.switch_to.window(windows[0])

        end_time = time.time()
        print('time: {}'.format(end_time - start_time))
        return self.dr
