#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/9 14:43

@author: tatatingting
"""

import time
import random
import dict_comment


class article:

    def __init__(self, num_zhuanti, dr, dianzan, push, follow, comment_dianzan, comment, flag_counts):
        # ------ 个性化操作 -------
        # 配置司机
        self.dr = dr
        # 确定收录专题是第几个
        self.num_zhuanti = num_zhuanti
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
        # 确定翻页次数/决定收录几篇文章/确定操作几篇文章一个循环
        self.flag_counts = flag_counts

    def run(self):

        n = 3

        # def num():
        #     return random.randint(2, 10)
        #
        # n1 = num()

        comments = dict_comment.dict_comment().run()
        n_comments = len(comments.keys())

        # -------收录文章------------
        # 确定当前窗口数量
        windows = self.dr.window_handles
        # print(windows)
        # 确定当前页面的title数量
        titles = self.dr.find_elements_by_class_name("title")
        if self.flag_counts > 4:
            m = len(titles)
        else:
            m = self.flag_counts
        # 依次打开特定的页面
        for i in range(m):
            print('title:', i, '/', m)
            # 确认新页面的打开方式是新开选项卡
            if titles[i].get_attribute('target') == '_blank':
                try:
                    # =============执行启动===============
                    # 点击这个标题
                    self.dr.execute_script("var a = document.getElementsByClassName('title');a[" + str(i) + "].click();")
                    time.sleep(n)
                    # 打印目前的页面状况
                    windows = self.dr.window_handles
                    # print(windows)
                    # 切换到新页面，确定第几个（重要！！！)
                    self.dr.switch_to.window(windows[len(windows) - 1])
                    time.sleep(n)
                    # =============执行关注功能=============
                    if self.follow:
                        try:
                            self.dr.find_element_by_link_text('关注').click()
                            time.sleep(n)
                            print('--- follow!')
                        except:
                            pass
                    # =============执行点赞功能=============
                    if self.dianzan:
                        # try:
                        #     # self.dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        #     self.dr.find_element_by_link_text('喜欢').click()
                        #     time.sleep(n)
                        #     print('--- good!')
                        # except:
                        #     print('没有找到点赞的地方。。。')
                        def try_click():
                            try:
                                self.dr.find_element_by_link_text('喜欢').click()
                                time.sleep(n)
                                print('--- good!')
                                return True
                            except:
                                return False

                        n_while = 0
                        n_while_max = 10
                        result = try_click()

                        while n_while < n_while_max and result == False:
                            n_while += 1
                            self.dr.refresh()
                            time.sleep(n)
                            result = try_click()

                        if n_while == n_while_max:
                            print('没有找到“点赞”的按钮！')



                    # =============执行评论功能===============
                    if self.comment > 0:
                        text_choose = random.randint(0, n_comments)
                        text_content = comments.get(text_choose)
                        if self.comment == 2:
                            text_content = '已主动收录，如需沟通主页有联系方式~'
                        try:
                            input_comment = self.dr.find_element_by_xpath('//*[@id="comment-list"]/div[1]/form/textarea')
                            input_comment.click()
                            time.sleep(n)
                            input_comment.clear()
                            input_comment.send_keys(text_content)
                            time.sleep(n * n)
                            self.dr.find_element_by_link_text('发送').click()
                            time.sleep(n)
                            print('--- comment!')
                        except:
                            pass

                    # =============执行点赞评论功能===========
                    if self.comment_dianzan:
                        try:
                            # 点赞之
                            num_comment_dianzan = self.dr.find_elements_by_class_name('like-button')
                            for num_c_d in range(len(num_comment_dianzan)):
                                num_comment_dianzan[num_c_d].click()
                                time.sleep(n)
                                print('--- dz comment')
                        except:
                            pass

                    # =============执行收录操作=============
                    if self.push:
                        try:
                            # 打开收录的弹窗
                            self.dr.execute_script(
                                "var a = document.getElementsByClassName('js-submit-button');a[0].click();")
                            time.sleep(n)
                            # 指定收录的专题，确定第几个（重要！！！)
                            self.dr.execute_script("var a = document.getElementsByClassName('action-btn');a[" + str(
                                self.num_zhuanti) + "].click();")
                            time.sleep(n)
                            print('--- push!')
                        except:
                            pass
                    # ==============执行返航================
                    # 关闭该页面
                    self.dr.close()
                    # 切换回母页，确定第几个（重要！！！)
                    self.dr.switch_to.window(windows[len(windows) - 1 - 1])
                    # 打印信息
                    print('--- ok', i, '/', m)
                except:
                    print('_blank，但是没有成功打开页面。')
        return self.dr
