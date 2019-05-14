import urllib
import urllib.request as request
import re
import time
import os

# The notifier function
def notify(title, subtitle, message, url):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    o = '-open {!r}'.format(url)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s ,o])))

CURRENCY_NAME = '日元'
CURRENCY_BASE = input('请输入基准现汇买入价:')
PATH = "/Users/ts-ruiqiang.liu/Documents/SRC/python/bash/"
URL = "http://www.boc.cn/sourcedb/whpj/";
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"

headers = { 'User-Agent' : USER_AGENT}
req = request.Request(URL,None,headers);

def getCurrency():
    res = request.urlopen(req)
    content = res.read().decode("utf-8")
    th_list = re.findall('(?<=<th>).+?(?=</th>)',content)
    td_list = re.findall('(?<=<td>).+?(?=</td>)',content)
    if CURRENCY_NAME in td_list:
        curr_index = td_list.index(CURRENCY_NAME)
        if curr_index >= 0:
            curr_now = td_list[curr_index + 1]
            curr_date = td_list[curr_index + 6]
            curr_time = td_list[curr_index + 7]

            text = CURRENCY_NAME + ',' + curr_date +' '+ curr_time + ',' + curr_now
            print(th_list[1] +': '+ text)

            if float(curr_now) >= float(CURRENCY_BASE):
                notify(title= th_list[1] +': '+ curr_now + ' 基准:'+ CURRENCY_BASE,
                    subtitle='Developed by liu.',
                     message= text,
                         url= URL)

            path = PATH + CURRENCY_NAME +'-' +curr_date +'.txt'
            if not os.path.exists(path):
                f = open(path, "w")
                f.close()

            with open(path, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(text + '\n' + content)

interval = 180
while True:
    getCurrency()
    time.sleep(interval)
