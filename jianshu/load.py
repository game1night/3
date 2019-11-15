#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/10/30 16:32

@author: tatatingting
"""

import os
from selenium import webdriver
import time


def cd(n):
    for i in range(n):
        time.sleep(1)
        # print(i)


def run(path, url, info, user_list, page_count, fresh_count):
    # 设置驱动
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # 创建汽车
    dr = webdriver.Chrome(os.path.join(path, 'chromedriver'), options=options)
    # 启动汽车，前往各个站点
    # 首页半自动登陆，需手动输入验证码并点击提交
    signin(dr, url, info)
    # 关注那些给予喜欢和赞的朋友
    like_count = follow(dr, url, user_list, page_count)
    # 给关注的朋友点赞
    like(dr, url, like_count)
    # 给首页的文章点赞
    find(dr, url, fresh_count)
    return 0


def signin(dr, url, info):
    # 前往首页
    dr.get(url[0])
    # 首页-未登录
    dr.find_element_by_xpath('//*[@id="sign_in"]').click()
    cd(2)
    # 登陆页
    name = dr.find_element_by_xpath('//*[@id="session_email_or_mobile_number"]')
    name.click()
    name.clear()
    name.send_keys(info.get('name'))
    pwd = dr.find_element_by_xpath('//*[@id="session_password"]')
    pwd.click()
    pwd.clear()
    pwd.send_keys(info.get('password'))
    dr.find_element_by_xpath('//*[@id="sign-in-form-submit-btn"]').click()
    cd(15)
    # 验证码
    # dr.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/div/div[3]/a').click()
    # cd(5)
    # 首页-已登陆
    return 0


def follow(dr, url, user_list, page_count):
    b_len = len(user_list)
    print('当前已关注{}位'.format(b_len))
    # 前往收到的喜欢和赞
    dr.get(url[1])
    cd(3)
    # 翻页逐行判断
    for page in range(page_count):
        # 当页索引
        print('当前第{}页'.format(page + 1))
        for i in range(10):
            try:
                user = dr.find_element_by_xpath('/html/body/div/div/div[2]/div/ul/li[' + str(i + 1) + ']/div/a[1]')
                user_link = user.get_attribute('href')
                # print(i, '-', user_link)
                if user_link not in user_list:
                    # 进入用户主页
                    user.click()
                    cd(3)
                    try:
                        dr.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/button').click()
                        cd(2)
                        # print('-关注成功')
                        uu(user_link)
                        # print('-记录册更新成功')
                        user_list.append(user_link)
                        print('-添加成功', i)
                    except:
                        print('-follow error')
                    # 退出当前主页
                    dr.back()
                    cd(3)
                    # 翻页至当前进度
                    for i in range(page):
                        dr.find_element_by_link_text('下一页').click()
                        cd(3)
                # else:
                #     print('-已关注该用户')
            except:
                print('follow not find')
        # 下一页
        dr.find_element_by_link_text('下一页').click()
        cd(3)
    a_len = len(user_list)
    print('更新后共关注{}位，新增{}位'.format(a_len, a_len - b_len))
    return a_len


def uu(user_link):
    with open('user_list.txt', 'a', encoding='utf-8-sig') as f:
        f.write('\n' + user_link)
    return 0


def like(dr, url, a_len):
    dr.get(url[2])
    cd(3)
    # 筛选只看作者
    dr.find_element_by_xpath('/html/body/div/div/div[1]/a[1]').click()
    dr.find_element_by_xpath('/html/body/div/div/div[1]/ul[1]/li[2]/a').click()
    cd(3)
    # 捕捉有更新的对象
    # dr.execute_script("var q=document.getElementsByClassName('js-subscription-list')[0].scrollTop = 10000")
    like_count = 0
    for i in range(a_len):
        try:
            # 查找视野内目标
            dr.find_element_by_xpath('/html/body/div/div/div[1]/ul[2]/li[' + str(2 + i) + ']/a/span').click()
            cd(5)
            # 点击文章
            dr.find_element_by_xpath('/html/body/div/div/div[2]/div/div/ul[2]/div[1]/li/div/a').click()
            # 操作文章
            like_article(dr)
            like_count += 1
        except:
            # 排头兵滚动条法
            dr.find_element_by_xpath('/html/body/div/div/div[1]/ul[2]/li[' + str(2 + i) + ']').click()
            cd(1)
        print(i, '/', like_count, '/', a_len)
    return 0


def like_article(dr):
    # 切换导航
    cd(1)
    dr.switch_to_window(dr.window_handles[1])
    cd(4)
    # 评阅文章
    try:
        dr.find_element_by_xpath('//*[@id="__next"]/footer/div[1]/div[1]/div[2]/div[2]').click()
        cd(1)
    except:
        print('no button')
    # 返航
    dr.close()
    dr.switch_to_window(dr.window_handles[0])
    return 0


def find(dr, url, fresh_count):
    dr.get(url[3])
    cd(3)
    for fresh in range(fresh_count):
        print('这是第{}次刷新'.format(fresh))
        # dr.execute_script("var q=document.documentElement.scrollTop=10000")
        # cd(3)
        # 获取文单
        article_list = dr.find_elements_by_class_name('ic-list-comments')
        print(len(article_list))
        for i in range(len(article_list)):
            # 点击文章
            article_list[i].click()
            # 操作文章
            like_article(dr)
        # 刷新页面
        dr.refresh()
    return 0


if __name__ == '__main__':
    # 记时开始
    s_time = time.time()
    # 驱动地址
    path = os.path.dirname(os.path.dirname(__file__))
    # 目标网址
    url = [
        'https://www.jianshu.com',
        'https://www.jianshu.com/notifications#/likes',
        'https://www.jianshu.com/subscriptions#/timeline',
        'https://www.jianshu.com/',
        '',
    ]
    # 关键信息
    info = {
        'name': '',
        'password': ''
    }
    # 初始用户列表
    with open('user_list.txt', 'r', encoding='utf-8-sig') as f:
        user_list = f.read().splitlines()
    # 运行主程序
    run(path, url, info, user_list, page_count=20, fresh_count=10)
    # 记时结束
    e_time = time.time()
    print('总耗时{}'.format(e_time - s_time))
