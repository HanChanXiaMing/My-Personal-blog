#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from orm import Model, StringField, IntegerField
#把常用的SELECT、INSERT、UPDATE和DELETE操作用函数封装起来

# 连接池由全局变量__pool存储
@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),  # 自动提交
        maxsize=kw.get('maxsize', 10),  # 池中最多有10个链接对象
        minsize=kw.get('minsize', 1),
        loop=loop
    )
