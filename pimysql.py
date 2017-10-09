# -*- coding:utf-8 -*-
import pymysql


def select():
    conn = pymysql.connect(host='127.0.0.1',
                           user='nova', passwd='password',
                           db='wechat',
                           port=3306,
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("select version()")
    row = cur.fetchone()
    print "server version:", row[0]
    cur.close()
    conn.close()


def insert(fromUser, CreateTime, msgType, QR_ID):
    conn = pymysql.connect(host='w3c.poissonodds.win',
                           user='nova', passwd='password',
                           db='wechat',
                           port=3306,
                           charset='utf8')
    cur = conn.cursor()
    ins = 'insert into wechat_fans (openid, CreateTime, MsgType, qr_scene_id) values ("%s", "%s", "%s", "%d");' % (fromUser, CreateTime, msgType, QR_ID)
    status = cur.execute(ins)
    if status == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

