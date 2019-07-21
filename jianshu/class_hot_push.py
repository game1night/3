# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 18:25:28 2019

@author: tatatingting
"""

# 个性化操作
from selenium import webdriver
import time
import random
import class_article


class hot_push:

    def __init__(self,
                 dr,
                 num_zhuanti=0,
                 counts=10,
                 dianzan=True,
                 push=True,
                 follow=True,
                 comment_dianzan=True,
                 comment=False):
        # 确定司机
        self.dr = dr
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

        for i in range(self.counts):
            # 打印信息
            print('--- fresh', i)
            # 刷新页面
            self.dr.refresh()
            time.sleep(n)
            # ------------------下翻几页---------------------
            # 翻出阅读更多的按钮
            for count_fanye in range(1):
                self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(n)
            # # 点击阅读更多
            # for j in range(3):
            #     try:
            #         self.dr.execute_script("var a = document.getElementsByClassName('load-more'); a[0].click();")
            #         print('--- scroll ok')
            #         time.sleep(n)
            #     except:
            #         pass
            # ------------------收录文章------------------------
            self.dr = class_article.article(num_zhuanti=self.num_zhuanti,
                                            dr=self.dr,
                                            dianzan=self.dianzan,
                                            push=self.push,
                                            follow=self.follow,
                                            comment_dianzan=self.comment_dianzan,
                                            comment=self.comment,
                                            flag_counts=self.counts).run()

        print('--- hot push ok')
        # --- 返航到首页 ---
        self.dr.find_element_by_class_name('logo').click()
        end_time = time.time()
        print('time: {}'.format(end_time - start_time))

        return self.dr
