# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:43:38 2018

@author: Python
"""

import requests
import re
import pymysql,pymongo
import warnings

class Maoyan:
    def __init__(self):
        self.headers = {"User_Agent":'Mozilla5.0/'}
        self.baseurl = 'http://maoyan.com/board/4?offset='
        self.page = 0
        #创建数据库对象
        self.db = pymysql.connect('localhost','root','123456',charset = 'utf8')
        #创建游标对象
        self.cursor = self.db.cursor()
        # self.conn = pymongo.MongoClient('localhost',27017)
        # self.db = self.conn.movie
        # self.myset = self.db.filem
    #1.请求获取内容
    def getPage(self,url):
        req = requests.get(url,headers = self.headers)
        req.encoding = 'utf-8'
        html = req.text
        print(html)
        print('第%d页数据获取成功'%self.page)
        self.parsePage(html)
    #2.用正则匹配所需要的内容
    def parsePage(self,html):
        p = re.compile('<div class="movie-item-info">.*?title="(.*?).*?class="star"></p>(.*?)class="releasetime">(.*?)</p></div>',re.S)
        content_list = p.findall(html)
    	# print(content_list)
        print('第%d页数据匹配成功'%self.page)
        self.DownLoadMysql(content_list)
    #3.将匹配到的数据存入到MySQL数据库
    def DownLoadMysql(self,content_list):
        warnings.filterwarnings('error')
        try:
            self.cursor.execute('create database if not exists Maoyantop100;')
        except Warning:
            pass
        self.cursor.execute('use Maoyantop100')
        try:
            self.cursor.execute('create table maoyanMovie(id int primary key auto_increment,\
            	movieName varchar(30),\
            	movieActions varchar(100),\
            	movieReleaseTime varchar(50))')
        except Warning:
            pass
        for content_str in content_list:
            self.cursor.execute('insert into maoyanMovie\
            	(movieName,movieActions,moveReleaseTime)values("%s","%s","%s");'\
            	%(content_str[0].strip(),content_str[1].strip(),content_str[2].strip()))
            self.db.commit()
        print(content_list)
        print('第%d页数据插入成功'%self.page)
            # d = {
            # 'name':content_str[0],
            # 'star':content_str[1],
            # 'time':content_str[2],
            # }
            # self.myset.insert(d)
    #4.主函数
    def Main(self):
    	#http://maoyan.com/board/4?offset=10
        while True:
        	url = self.baseurl + str(self.page)
        	self.getPage(url)
        	c = input('是否要继续爬取下一页（y/n:?）')
            if c.strip().lower()=='y':
                self.page += 10
            else:
                self.cursor.close()
                self.db.close()
                print("数据爬取完成，谢谢使用！")
        		break
if __name__ == '__main__':
    maoyan = Maoyan()
    maoyan.Main()
