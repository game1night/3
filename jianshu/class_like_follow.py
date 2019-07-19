#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/9 16:52

@author: tatatingting
"""

import class_article
import time


class like_follow:

    def __init__(self,
                 num_followers,
                 dr,
                 num_zhuanti=0,
                 counts=0,
                 dianzan=1,
                 push=1,
                 follow=0,
                 comment_dianzan=1,
                 comment=0
                 ):
        self.dr = dr
        # 确定有几个粉丝
        self.num_followers = num_followers
        # 确定收录专题是第几个
        self.num_zhuanti = num_zhuanti
        # 确定翻页次数/决定收录几篇文章/确定操作几篇文章一个循环
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

        # ---- 个性化 ---------
        n = 2
        num = 0

        # 找到关注列表
        self.dr.find_element_by_class_name('ic-navigation-follow').click()
        time.sleep(n)
        self.dr.find_element_by_link_text('全部关注').click()
        time.sleep(n)
        self.dr.find_element_by_link_text('只看作者').click()
        time.sleep(n)

        # 开始扫平
        for i in range(self.num_followers+1):
            # print(i)
            try:
                # 滚轮进入视线
                if i % 15 == 0:
                    # 滚轮到特定用户页面(另可以通过定位滚动条actionchain的方式实现）
                    self.dr.execute_script("arguments[0].scrollIntoView();", self.dr.find_elements_by_class_name('name')[i])
                    time.sleep(n)
                # 查阅有更新的作者
                new_names = self.dr.find_elements_by_class_name('count')
                if len(new_names) > 0:
                    # 点开特定用户页面
                    self.dr.execute_script("var a = document.getElementsByClassName('count');a[0].click();")
                    time.sleep(n)
                    # ------------------操作文章------------------------
                    self.dr = class_article.article(num_zhuanti=self.num_zhuanti,
                                                    dr=self.dr,
                                                    dianzan=self.dianzan,
                                                    push=self.push,
                                                    follow=self.follow,
                                                    comment_dianzan=self.comment_dianzan,
                                                    comment=self.comment,
                                                    flag_counts=self.counts).run()
                    num += 1
                    print(num)
            except:
                pass


        print('给粉丝点赞 done!')

        # --- 返航到首页 ---
        self.dr.find_element_by_class_name('logo').click()


        end_time = time.time()
        print('time: {}'.format(end_time - start_time))
        return self.dr
