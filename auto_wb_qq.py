# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 20:32:13 2021

@author: 13942
"""

import requests
import re
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from bs4 import BeautifulSoup

url = 'https://s.weibo.com/top/summary?cate=realtimehot' #微博网址
headers = {'Cookie': 'SUB=_2AkMWPQnsf8NxqwJRmP0WyGvgbo9wwwDEieKgYfg3JRMxHRl-yT9jqhZftRB6Pb0nA8sx_gPHxXeGyQrlFLm3_q-jOQqd; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhBE4aU.PdCc3y_IE54zrvb; _s_tentry=passport.weibo.com; Apache=4496432981604.41.1633781467608; SINAGLOBAL=4496432981604.41.1633781467608; ULV=1633781467615:1:1:1:4496432981604.41.1633781467608:',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
url1 = 'http://www.weather.com.cn/weather/101200101.shtml'
headers1 = {'Cookie': 'HMACCOUNT_BFESS=C8CE7F19C7214ADF; BDSFRCVID_BFESS=c1_OJeC62xB8vG3HSwizJ7xXumKMABnTH6ao6JRCbbvubv4VyRwfEG0Pfx8g0Ku-_2fqogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tRKj_IPMfIvbfP0k24Q0M-FQ5eT22-usKb6d2hcH0KLKJh_95xt5yhtWMq6ZtbvvbCji2ljPafb1MRjvjx6CLPDV5loa-j3pMGrf0q5TtUJtJKnTDMRhqqRXblQyKMniBIv9-pnGBpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjQLeH_83e; ab_sr=1.0.1_NDliNzE0NzAwZmIxYjQ4OWJlNjVhYmY4ZmJjYzdjMzJlYzU4MDc3NzQ3NzIyMzRlMzVlZGIzY2I5NjVkYTJkNmMxNDYwN2FkODgwZTMxYzU5ZmM5ZDk5MzYxMWI1M2JkY2Y1ZDljM2JjYThhZGZmNmZjMWYwY2M5OWUwNzMwODIwM2U0YzUwYTdjNWU1Y2NiZmYyODUzOTgwYWVkY2Q1Yg==; BAIDUID_BFESS=24BA7F0AEBF3C80BD7B5C39E7F21356C:FG=1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}

def getnr():
    ret = requests.get(url, headers=headers)
    test = ret.text
    u_href = '<a href="(.*?)" target="_blank">.*?</a>'
    u_title = '<a href=".*?" target="_blank">(.*?)</a>'
    u_amount = '<span>(.*?)</span>'
    u_category = '<td class="td-03">(.*?)</td>'
    # u_href = '<a href="(.*?)" target="_blank">.*?</a>'
    title = re.findall(u_title,test)
    amount = re.findall(u_amount,test)
    category = re.findall(u_category,test)
    href = re.findall(u_href,test)
    return title,amount,category,href

def getnr2():
    res = requests.get(url1, headers=headers1)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    tem1 = soup.find(class_='tem')
    weather1 = soup.find(class_='wea')
    fen = soup.find(class_='win')
    tem = tem1.text
    weather = weather1.text
    fen  = fen.text
    result = weather + '   ' + tem + '   ' + fen
    return result

def shujuwish(title,amount,category,href):
    title = title[1:51]
    
    href = href[1:51]
    for j in range(len(href)):
        href[j] = 'https://s.weibo.com/' + href[j]
   
    # amount = amount[1:50]
    while ' ' in amount:
        amount.remove(' ')  # 注意这里双引号之间有空格
        
    category = category[1:]
    for i in range(len(category)):
        if category[i] != '':
            category[i] = re.findall('<i class=".*?">(.*?)</i>',category[i])[0]
        if category[i] == '':
            category[i] = '空'
    if '荐' in category:
        category.remove('荐')
    if '商' in category:
        category.remove('商')
    if len(category)>50:
        category = category[:50]
        
    df = pd.DataFrame()
    df['关键词'] = title
    df['amount'] = amount
    df['category'] = category
    df['href'] = href
    # df = df.sort_values('amount')
    # df2 = df[df['category']=='爆']
    # df3 = df[df['category']=='沸']
    # df4 = df[df['category'] == '热']
    # df5 = df[df['category'] == '新']
    # df6 = df[df['category'] == '空']
    # df = pd.concat([df2,df3,df4,df5,df6],ignore_index = True)
    df.to_csv('微博热搜.csv',encoding = 'gbk')#输出为csv文本格式
    return df

def email(df,wea):
    # hll = True
    number = 'llh.forever@foxmail.com'
    smtp = 'wvitioaamusbgbad'
    to = '1394242742@qq.com'  # 可以是非QQ的邮箱

    mer = MIMEMultipart()
    # 设置邮件正文内容
    head = '''
    <p style="color:OrangeRed">微博热搜及天气</p>
    <p style="color:Lime">天气: "{}"</p>
    <p>最热门词条为</p>
    <p><a href="{}">{}</a></p>
    <p>排名前五的热搜</p>
    <p><a href="{}">{}</a></p>
    <p><a href="{}">{}</a></p>
    <p><a href="{}">{}</a></p>
    <p><a href="{}">{}</a></p>
    <p><a href="{}">{}</a></p>
    '''.format(wea,df.iloc[0,:]['href'],df.iloc[0,:]['关键词'],
               df.iloc[1,:]['href'],df.iloc[1,:]['关键词'],
               df.iloc[2,:]['href'],df.iloc[2,:]['关键词'],
               df.iloc[3,:]['href'],df.iloc[3,:]['关键词'],
               df.iloc[4,:]['href'],df.iloc[4,:]['关键词'],
               df.iloc[5,:]['href'],df.iloc[5,:]['关键词'])
    mer.attach(MIMEText(head, 'html', 'utf-8'))
    fujian = MIMEText(open('微博热搜.csv', 'rb').read(), 'base64', 'utf-8')
    fujian["Content-Type"] = 'application/octet-stream'  #附件内容
    fujian.add_header('Content-Disposition', 'file', filename=('utf-8', '', '微博热搜.csv'))  
    mer.attach(fujian)

    mer['Subject'] = '每日微博热搜及天气自动发送' #邮件主题
    mer['From'] = number   #发送人
    mer['To'] = to        #接收人

    # 5.发送邮件
    try:
        s = smtplib.SMTP_SSL('smtp.qq.com', 465)
        s.login(number, smtp)
        s.send_message(mer)  # 发送邮件
        s.quit()
        print('执行成功')
    except Exception as e:
        print(e)
        print('发送失败')
if __name__ == '__main__':
    title1, amount1, category1, href1 = getnr()  
    weath = getnr2()
    result = shujuwish(title1,amount1,category1,href1)
    email(result,weath)


