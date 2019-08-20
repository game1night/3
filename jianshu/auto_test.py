#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/9 12:17

@author: tatatingting
"""

# 导入类
import time
import random
import class_login_js
import class_hot_push
import class_search_push
import class_like_follow
import class_follow_back
import class_follow_dianzan
import class_send_message


# --------确认页面---------
def show_windows(dr='dr'):
    n = 2
    windows = dr.window_handles
    time.sleep(n)
    # print(windows)


# --------关注点赞的--------
def fun0(dr, num=3):
    show_windows(dr)
    return class_follow_dianzan.follow_dianzan(dr=dr, counts=num).run()


# --------回粉回粉--------
def fun1(dr, num):
    show_windows(dr)
    return class_follow_back.follow_back(dr=dr, num_scroll=num).run()


# ---------给关注的人点赞--------------
def fun2(dr):
    show_windows(dr)
    return class_like_follow.like_follow(dr=dr,
                                         counts=2, dianzan=1,
                                         follow=0, num_followers=750,
                                         comment=0, comment_dianzan=0,
                                         push=0, num_zhuanti=0
                                         ).run()


# --------搜索收录---------
def fun3(dr, list, push=1, counts=10):
    show_windows(dr)
    print(list)
    return class_search_push.search_push(dr=dr,
                                         counts=counts, dianzan=1,
                                         follow=0,
                                         comment=0, comment_dianzan=0,
                                         push=push, key=list[0], num_zhuanti=list[1]
                                         ).run()


# --------点赞热门---------
def fun4(dr, num=10):
    show_windows(dr)
    return class_hot_push.hot_push(dr=dr,
                                   counts=num, dianzan=1,
                                   follow=0,
                                   comment=0, comment_dianzan=0,
                                   push=0, num_zhuanti=0
                                   ).run()


# --------群发简信----------
def fun5(dr, quick, num, content=''):
    show_windows(dr)
    return class_send_message.send_message(dr=dr,
                                           num_scroll=num,
                                           quick=quick,
                                           content=content
                                           ).run()

if __name__ == '__main__':
    start_time = time.time()
    dr = class_login_js.login_js(headless=False, auto_input=True, account='', password='').run()
    # ==================================================================================================================
#TODO
    while 1:
        try:
            # dr = fun5(dr, quick=1, num=900, content='')     # 留粉-私信
            dr = fun0(dr, num=100)  # 回粉-回点赞
            dr = fun2(dr)  # 留粉-点赞
            dr = fun4(dr, num=10)  # 吸粉-首页推荐-点赞
        except:
            dr.get('https://www.jianshu.com/')
            print('ohhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh!!!')

    # ==================================================================================================================
    # ------- 结束导航 ----------
    dr.quit()
    print('okokok')
    # ------- 运行时间 ---------
    end_time = time.time()
    print('time: {}'.format(end_time - start_time))
