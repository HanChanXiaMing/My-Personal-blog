#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#把常用的SELECT、INSERT、UPDATE和DELETE操作用函数封装起来

from asyncio

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
    
# 创建Select
@asyncio.coroutine
def select(sql, args, size=None):   # size可以决定取几条
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        # SQL语句的占位符是?，而MySQL的占位符是%s
        # 用参数替换而非字符串拼接可以防止sql注入
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            # 传入参数 通过fetchmany()获取最多指定数量的记录
            rs = yield from cur.fetchmany(size)
        else:
            # 传入参数 通过fetchall()获取所有记录
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs

# INSERT,UPDATE,DELETE语句,可以定义一个通用函数
@asyncio.coroutine
def execute(sql, args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount # 通过rowcount返回结果数
            yield from cur.close()
        except BaseException as e:
            raise
        return affected
