#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/3/13 14:40

@author: tatatingting
"""

import os
from selenium import webdriver
import time
import pandas as pd
import datetime as dt
import numpy as np


def cd(n, flag=False):
    for i in range(n):
        time.sleep(1)
        if flag:
            print(i)


def run(path, url, info, mode, like_count, date, str_list, master_list, user_list, flag):
    if flag[2]:
        # 设置驱动
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # 创建汽车
        driver = webdriver.Chrome(os.path.join(path, 'chromedriver'), options=options)
        # 启动汽车，前往各个站点
        # 首页半自动登陆，需手动输入验证码并点击提交or扫码登陆（推荐）
        sign_in(driver, url[1], info, mode)
        # 给关注的小伙伴动态点赞
        like_it(driver, like_count, str_list, url[6], flag)
        # 初始作品列表
        masters_url = {}
        get_masters_video(masters_url, driver, url[4], date)
        get_masters_article(masters_url, driver, url[5], date)
        get_masters_audio(masters_url, driver, url[7], date)
        if flag[3]:
            # 留意那些给我点赞的家伙和提取历史赞的数据
            follow_back(driver, master_list, user_list)

    # 清理一下数据
    get_tidy_data(['b_user_list.txt', 'b_master_list.txt', 'b_masters_url.csv'])

    return None


def sign_in(driver, url, info, mode):
    # 前往登陆页面
    driver.get(url)
    # 登陆页
    if mode == 1:
        # 登陆方式（1）手动短信验证码登录
        name = driver.find_element_by_xpath('//*[@id="login-username"]')
        name.click()
        name.clear()
        name.send_keys(info.get('name'))
        pwd = driver.find_element_by_xpath('//*[@id="login-passwd"]')
        pwd.click()
        pwd.clear()
        pwd.send_keys(info.get('password'))
        driver.find_element_by_xpath('//*[@id="geetest-wrap"]/div/div[5]/a[1]').click()
        cd(5)
        # 验证码
        # dr.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/div/div[3]/a').click()
        cd(20, flag=True)
    elif mode == 2:
        # 登录方式（2）扫码登陆
        cd(20, flag=True)
    # 首页-已登陆
    print('登陆成功，开心每一天o(^▽^)o')
    return 0


def like_it(driver, like_count, str_list, url, flag):
    # 预算一下话术库长度
    str_list_len = len(str_list)
    # 前往动态页面
    driver.get(url)
    cd(10)
    # 只看投稿视频
    try:
        # 有人直播的情况下
        driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/a').click()
        cd(10)
    except:
        # 没有人直播的情况下
        driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/a').click()
        cd(10)
    # 开始点赞列表
    try:
        # 防止出现新动态提示，从第二个开始，稳妥
        count = 2
        count_done = 0
        count_ready = 0
        while count <= like_count:
            like_str = '//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[{}]/div[1]/div[4]/div[3]/span/i'.format(str(count))
            like_item = driver.find_element_by_xpath(like_str)
            like_item_status = like_item.get_attribute('class')
            cd(1)
            if like_item_status == 'custom-like-icon zan':
                like_item.click()
                count_done += 1
                count_ready = 0
                print('第{}个赞/{}'.format(str(count_done), str(count)))
                cd(1)
                if flag[4]:
                    # 尝试互动模块
                    # 点击前往投稿视频页面
                    tougao_item_click = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[{}]/div[1]/div[3]/div[2]/div/div[2]/a/div/div[2]/div[1]'.format(str(count)))
                    tougao_item_click.click()
                    # 切换导航
                    driver.switch_to.window(driver.window_handles[1])
                    cd(3)
                    cd(np.random.randint(15))
                    try:
                        if np.random.randint(10) >= 8 and flag[0]:
                            cd(np.random.randint(15))
                            # 弹幕
                            danmu_input_item = driver.find_element_by_xpath('//*[@id="bilibiliPlayer"]/div[1]/div[2]/div/div[2]/div[3]/div[1]/input')
                            # danmu_input_item = driver.find_element_by_class_name('bilibili-player-video-danmaku-input')
                            danmu_input_item.click()
                            danmu_input_item.clear()
                            danmu_input_item.send_keys(str_list[np.random.randint(str_list_len)])
                            driver.find_element_by_xpath('//*[@id="bilibiliPlayer"]/div[1]/div[2]/div/div[2]/div[3]/div[2]').click()
                            cd(5)
                        elif np.random.randint(10) >= 5 and flag[1]:
                            cd(np.random.randint(30))
                            # 评论
                            driver.execute_script("window.scrollBy(0, 1000)")
                            cd(3)
                            input_box_item = driver.find_element_by_class_name('ipt-txt')
                            input_box_item.click()
                            input_box_item.clear()
                            input_box_item.send_keys(str_list[np.random.randint(str_list_len)])
                            cd(3)
                            submit_box_item = driver.find_element_by_class_name('comment-submit')
                            submit_box_item.click()
                            cd(3)
                        else:
                            cd(1)
                    except:
                        print('only play')
                    # 导航返回
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    cd(1)
            else:
                count_ready += 1
                print('已赞过')
                driver.execute_script("arguments[0].scrollIntoView();", like_item)
            if count_ready >= 50:
                print('连续{}个已赞过，先结束吧！'.format(str(count_ready)))
                break
            count += 1
    except:
        print('跳出点赞')

    return None


def get_masters_video(masters_url, driver, url, date):
    # 转到主页-video/article
    driver.get(url)
    cd(5)
    # 查找作品
    i = 0
    while i >= 0:
        try:
            i += 1
            m_item = driver.find_element_by_xpath('//*[@id="submit-video-list"]/ul[1]/li[{}]/div/div[1]/a'.format(str(i)))
            # 定位到视野中
            driver.execute_script("arguments[0].scrollIntoView();", m_item)
            m_url = m_item.get_attribute('href')
            m_title = m_item.get_attribute('title')
            # 播放量
            play_item = driver.find_element_by_xpath('//*[@id="submit-video-list"]/ul[2]/li[{}]/div/span[1]'.format(str(i)))
            m_play = play_item.get_attribute('textContent')
            mm(m_url, m_title, m_play, date)
            masters_url.update({m_url: m_title})
        except:
            break
    j = 0
    while j == 0:
        try:
            nextpage = driver.find_element_by_link_text('下一页')
            # 定位到视野中
            driver.execute_script("arguments[0].scrollIntoView();", nextpage)
            nextpage.click()
            cd(5)
            i = 0
            while i >= 0:
                try:
                    i += 1
                    m_item = driver.find_element_by_xpath(
                        '//*[@id="submit-video-list"]/ul[1]/li[{}]/div/div[1]/a'.format(str(i)))
                    # 定位到视野中
                    driver.execute_script("arguments[0].scrollIntoView();", m_item)
                    m_url = m_item.get_attribute('href')
                    m_title = m_item.get_attribute('title')
                    # 播放量
                    play_item = driver.find_element_by_xpath(
                        '//*[@id="submit-video-list"]/ul[2]/li[{}]/div/span[1]'.format(str(i)))
                    m_play = play_item.get_attribute('textContent')
                    mm(m_url, m_title, m_play, date)
                except:
                    break
        except:
            break
    print('作品收集完毕~')

    return None


def get_masters_article(masters_url, driver, url, date):
    # 转到主页-video/article
    driver.get(url)
    cd(5)
    # 查找作品
    i = 0
    while i >= 0:
        try:
            i += 1
            m_item = driver.find_element_by_xpath('//*[@id="page-article"]/div/div[2]/div[2]/div/ul/li[{}]/div[1]/h2/a'.format(str(i)))
            # 定位到视野中
            driver.execute_script("arguments[0].scrollIntoView();", m_item)
            m_url = m_item.get_attribute('href')
            m_title = m_item.get_attribute('title')
            # 播放量
            play_item = driver.find_element_by_xpath('//*[@id="page-article"]/div/div[2]/div[2]/div/ul/li[{}]/div[1]/div/span[2]'.format(str(i)))
            m_play = play_item.get_attribute('textContent')
            mm(m_url, m_title, m_play, date)
            masters_url.update({m_url: m_title})
        except:
            break
    j = 0
    while j == 0:
        try:
            nextpage = driver.find_element_by_link_text('下一页')
            # 定位到视野中
            driver.execute_script("arguments[0].scrollIntoView();", nextpage)
            nextpage.click()
            cd(5)
            i = 0
            while i >= 0:
                try:
                    i += 1
                    m_item = driver.find_element_by_xpath(
                        '//*[@id="page-article"]/div/div[2]/div[2]/div/ul/li[{}]/div[1]/h2/a'.format(str(i)))
                    # 定位到视野中
                    driver.execute_script("arguments[0].scrollIntoView();", m_item)
                    m_url = m_item.get_attribute('href')
                    m_title = m_item.get_attribute('title')
                    # 播放量
                    play_item = driver.find_element_by_xpath(
                        '//*[@id="page-article"]/div/div[2]/div[2]/div/ul/li[{}]/div[1]/div/span[2]'.format(str(i)))
                    m_play = play_item.get_attribute('textContent')
                    mm(m_url, m_title, m_play, date)
                    masters_url.update({m_url: m_title})
                except:
                    break
        except:
            break
    print('作品收集完毕~')

    return masters_url


def get_masters_audio(masters_url, driver, url, date):
    # 转到主页-video/article
    driver.get(url)
    cd(5)
    # 查找作品
    i = 0
    while i >= 0:
        try:
            i += 1
            m_item = driver.find_element_by_xpath('//*[@id="page-audio"]/div/div[2]/div[2]/div/ul[1]/li[{}]/a[2]'.format(str(i)))
            # 定位到视野中
            driver.execute_script("arguments[0].scrollIntoView();", m_item)
            m_url = m_item.get_attribute('href')
            m_title = m_item.get_attribute('title')
            # 播放量
            play_item = driver.find_element_by_xpath('//*[@id="page-audio"]/div/div[2]/div[2]/div/ul[1]/li[{}]/div/span[1]'.format(str(i)))
            m_play = play_item.get_attribute('textContent')
            mm(m_url, m_title, m_play, date)
            masters_url.update({m_url: m_title})
        except:
            break
    j = 0
    while j == 0:
        try:
            nextpage = driver.find_element_by_link_text('下一页')
            # 定位到视野中
            driver.execute_script("arguments[0].scrollIntoView();", nextpage)
            nextpage.click()
            cd(5)
            i = 0
            while i >= 0:
                try:
                    i += 1
                    m_item = driver.find_element_by_xpath(
                        '//*[@id="page-article"]/div/div[2]/div[2]/div/ul/li[{}]/div[1]/h2/a'.format(str(i)))
                    # 定位到视野中
                    driver.execute_script("arguments[0].scrollIntoView();", m_item)
                    m_url = m_item.get_attribute('href')
                    m_title = m_item.get_attribute('title')
                    # 播放量
                    play_item = driver.find_element_by_xpath(
                        '//*[@id="page-article"]/div/div[2]/div[2]/div/ul/li[{}]/div[1]/div/span[2]'.format(str(i)))
                    m_play = play_item.get_attribute('textContent')
                    mm(m_url, m_title, m_play, date)
                    masters_url.update({m_url: m_title})
                except:
                    break
        except:
            break
    print('作品收集完毕~')

    return masters_url


def mm(m_url, m_title, m_play, date):
    m_url = str(m_url).strip()
    m_title = str(m_title).strip()
    m_play = str(m_play).strip()
    # 存下来
    with open('{}_masters_url.csv'.format('b'), 'a', encoding='utf-8-sig') as f:
        f.write('\n{},{},{},'.format(m_url, m_title, m_play))

    return None


def follow_back(driver, master_list, user_list):
    master_list_len = len(master_list)
    for master_list_url in master_list:
        master_list_len -= 1
        # 前往作品消息
        driver.get(master_list_url)
        driver.refresh()
        cd(5)
        # 提取点赞行为数据
        j = 0
        while j >= 0:
            try:
                j += 1
                # 太快了缓一下
                if j % 10 == 0:
                    cd(1)
                # 点赞用户页卡
                l_user_str = '//*[@id="link-message-container"]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[{}]/div/div[2]/div[1]/span[1]/a'.format(str(j))
                l_user = driver.find_element_by_xpath(l_user_str)
                # 定位到视野中
                driver.execute_script("arguments[0].scrollIntoView();", l_user)
                # 获取点赞用户的信息url
                liked_user_url = l_user.get_attribute('href')
                # 更新用户数据库
                if liked_user_url not in user_list:
                    uu(liked_user_url)
                    user_list.append(liked_user_url)
                    print('      +1')
            except:
                print(master_list_len)
                break

    return None


def uu(user_link):
    with open('b_user_list.txt', 'a', encoding='utf-8-sig') as f:
        f.write('\n' + user_link)
    return 0


def get_tidy_data(filename_list):
    for filename in filename_list:
        if 'csv' not in filename:
            # 读取数据
            with open(filename, 'r', encoding='utf-8-sig') as f:
                user_list = f.read().splitlines()
            # 整理数据
            user_list_df = pd.DataFrame(user_list)
            user_list_df.drop_duplicates(inplace=True)
            user_list_df.sort_values(0, ascending=True, inplace=True)
            # 存储数据
            with open(filename, 'w', encoding='utf-8-sig') as f:
                for line in list(user_list_df.iloc[:, 0]):
                    f.write('{}\n'.format(line))
        elif 'csv' in filename:
            masters_url_df = pd.read_csv(filename, header=None)
            # 改成keep=last，这样能看出最新的情况
            masters_url_df.drop_duplicates(keep='last', subset=[0, 1], inplace=True)
            masters_url_df.sort_values(0, ascending=True, inplace=True)
            masters_url_df.to_csv(filename, index=False, header=None, encoding='utf-8-sig')

    return None


if __name__ == '__main__':
    # 获取今天的日期
    today = time.strftime('%Y-%m-%d')
    long_ago = dt.date.today() - dt.timedelta(10)
    # 记时开始
    s_time = time.time()
    # 驱动地址
    paths = os.path.dirname(os.path.dirname(__file__))
    # 目标网址
    urls = [
        'https://www.bilibili.com',
        'https://passport.bilibili.com/login',
        'https://message.bilibili.com/#/love',
        'https://space.bilibili.com/???',  # 个人主页id
        'https://space.bilibili.com/???/video',
        'https://space.bilibili.com/???/article',
        'https://t.bilibili.com/',
        'https://space.bilibili.com/???/audio',
    ]
    # 关键信息
    infos = {
        'name': '',
        'password': '',
    }

    # 拟稿评论
    str_list_new = [
        '',
        '',
        '',
    ]

    # 初始作品列表
    with open('b_master_list.txt', 'r', encoding='utf-8-sig') as f:
        b_master_list = f.read().splitlines()

    # 初始用户列表
    with open('b_user_list.txt', 'r', encoding='utf-8-sig') as f:
        b_user_list = f.read().splitlines()

    # 运行主程序
    run(paths, urls, infos, mode=2, like_count=1000, date=today,
        str_list=str_list_new,
        master_list=b_master_list,
        user_list=b_user_list,
        # [弹幕，评论，操作, 历史回溯, 点开详情播放], 0, 1
        flag=[0, 0, 1, 0, 1],
        )

    # 记时结束
    e_time = time.time()
    print('总耗时{}'.format(e_time - s_time))
