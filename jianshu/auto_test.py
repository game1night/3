#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/7/9 12:17

@author: tatatingting
"""

# 导入类
import time
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
    print(windows)


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
                                         push=1, num_zhuanti=0
                                         ).run()


# --------搜索收录---------
def fun3(dr, list):
    show_windows(dr)
    print(list)
    return class_search_push.search_push(dr=dr,
                                         counts=10, dianzan=1,
                                         follow=0,
                                         comment=0, comment_dianzan=1,
                                         push=1, key=list[0], num_zhuanti=list[1]
                                         ).run()


# --------点赞热门---------
def fun4(dr, num=10):
    show_windows(dr)
    return class_hot_push.hot_push(dr=dr,
                                   counts=num, dianzan=1,
                                   follow=0,
                                   comment=0, comment_dianzan=1,
                                   push=1, num_zhuanti=0
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

    # --------登陆成功--------
    dr = class_login_js.login_js(headless=False, auto_input=False,
                                 account='',
                                 password='',
                                 ).run()
    show_windows(dr)
    s_time = time.time()
    # ==================================================================================================================

    dr = fun0(dr, num=100)  # 回粉-回点赞
    dr = fun2(dr)  # 留粉-点赞
    dr = fun3(dr, ['素描心得', 1])  # 吸粉-搜索-收录入专题
    dr = fun3(dr, ['游戏化', 2])
    dr = fun3(dr, ['同桌', 4])
    dr = fun4(dr, num=10)  # 吸粉-首页推荐-点赞

    for i in range(3):
        dr = fun0(dr, num=10)  # 回粉-回点赞
        dr = fun2(dr)  # 留粉-点赞
        dr = fun4(dr, num=20)  # 吸粉-首页推荐-点赞



    # dr = fun5(dr, quick=1, num=700, content='友友你好')     # 留粉-私信

    # ==================================================================================================================
    e_time = time.time()
    print('time: {}'.format(e_time - s_time))

    # ------- 结束导航 ----------
    dr.quit()
    print('okokok')
    # ------- 运行时间 ---------
    end_time = time.time()
    print('time: {}'.format(end_time - start_time))
