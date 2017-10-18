# -*- coding: utf-8 -*-
import hashlib
import web
import time
import os
from lxml import etree
from pimysql import insert


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "wniu"  # 这里改写在微信公众平台里输入的token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()  # 获得获取来的数据格式
        xml = etree.fromstring(str_xml)  # 进行XML解析

        toUser = xml.find("ToUserName").text  # 开发者微信号
        fromUser = xml.find("FromUserName").text  # 发送方帐号（一个OpenID）
        # CreateTime = xml.find("CreateTime").text
        CreateTime = time.strftime("%Y-%m-%d %X", time.localtime())
        msgType = xml.find("MsgType").text
        if msgType == 'event':  # 接收事件推送
            EventType = xml.find("Event").text  # 获取事件类型
            if EventType == 'subscribe':  # 用户未关注时，进行关注后的事件推送
                EventKey = xml.find("EventKey").text
                QR_ID = int(EventKey[8:])  # 去掉"qrscene_"的8位前缀
                insert(str(fromUser), str(CreateTime), str(msgType), QR_ID)
                # re_msg_sub = u"您好，欢迎关注皮尔磁Pilz官方微信公众号"
                # return self.render.reply_text(fromUser, toUser, int(time.time()), re_msg_sub)
                title1 = u"欢迎关注皮尔磁PILZ官方微信公众号"
                description1 = u"您可在对话框回复对应数字获取相关内容，直接点击本图文页面进入皮尔磁PILZ全球中文官网\n1.安全产品\n2.安全服务"
                picurl = 'https://www.pilz.com/imagecache/mam/pilz/images/import/01_Products_and_Solutions/I_industry40/fittosize__752_0_4bb4bf8e6d398c4debe5899c5746716b_f_industry_4_0_production_ostfildern_digital_network_dsc_8201_cold1_3c_2016_08_1000x562-desktop-1475157749.jpg'
                tw_url = 'https://www.pilz.com/zh-CN/'
                return self.render.reply_news(fromUser, toUser, int(time.time()), title1, description1, picurl, tw_url)
            elif EventType == 'SCAN':  # 用户已关注时的事件推送
                EventKey = int(xml.find("EventKey").text)  # 事件KEY值，是一个32位无符号整数，即创建二维码时的二维码scene_id
                insert(str(fromUser), str(CreateTime), str(msgType), EventKey)
                title1 = u"欢迎关注皮尔磁PILZ官方微信公众号"
                description1 = u"您可在对话框回复对应数字获取相关内容，直接点击本图文页面进入皮尔磁PILZ全球中文官网\n1.安全产品\n2.安全服务"
                picurl = 'https://www.pilz.com/imagecache/mam/pilz/images/import/01_Products_and_Solutions/I_industry40/fittosize__752_0_4bb4bf8e6d398c4debe5899c5746716b_f_industry_4_0_production_ostfildern_digital_network_dsc_8201_cold1_3c_2016_08_1000x562-desktop-1475157749.jpg'
                tw_url = 'https://www.pilz.com/zh-CN/'
                return self.render.reply_news(fromUser, toUser, int(time.time()), title1, description1, picurl, tw_url)
                # re_msg_scan = u"您好，皮尔磁Pilz官方微信公众号欢迎您回来"
                # return self.render.reply_text(fromUser, toUser, int(time.time()), re_msg_scan)

            else:
                re_msg_other_events = u"您好，皮尔磁Pilz官方微信公众号欢迎您回来"
                return self.render.reply_text(fromUser, toUser, int(time.time()), re_msg_other_events)
        elif msgType == 'text':
            content = xml.find("Content").text
            if content == "1":
                re_msg_1 = u"您好，皮尔磁相关产品请点击https://www.pilz.com/zh-CN/products-solutions"
                return self.render.reply_text(fromUser, toUser, int(time.time()), re_msg_1)
            elif content == "2":
                re_msg_2 = u"您好，皮尔磁相关服务请点击https://www.pilz.com/zh-CN/services"
                return self.render.reply_text(fromUser, toUser, int(time.time()), re_msg_2)
            else:
                re_other_txt = u"您好，无法识别该请求，相关资料请访问页面底部菜单查询。"
                return self.render.reply_text(fromUser, toUser, int(time.time()), re_other_txt)
        else:
            re_others = u"您好，无法识别该请求，相关资料请访问页面底部菜单查询。"
            return self.render.reply_text(fromUser, toUser, int(time.time()), re_others)