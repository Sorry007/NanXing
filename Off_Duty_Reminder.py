from datetime import date, datetime
from distutils.log import INFO
import time
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import os
import random
import requests

today = datetime.now()

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 设置男朋友的账号
boy_friend_id = os.environ["BOY_FRIEND_ID"]
# 设置女朋友的账号
girl_friend_id = os.environ["GIRL_FRIEND_ID"]
# 设置模板id
template_id = os.environ["LOW_WORK_TEMPLATE_ID"]

# 获取当前周几
def get_weekdays():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    local_time = time.localtime(time.time())   # 获取当前时间的时间元组
    # time.struct_time(tm_year=2022, tm_mon=4, tm_mday=9, tm_hour=13, tm_min=48, tm_sec=23, tm_wday=5, tm_yday=99, tm_isdst=0)
    week_index = local_time.tm_wday  # 获取时间元组内的tm_wday值
    week = week_list[week_index]
    return week

# 获取当前日期
def get_today():
  return (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')   
  #return time.strftime('%Y{}%m{}%d{} %H{}%M{}',time.localtime()).format("年","月","日","时","分")

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

# 获取下班提醒
def get_message():
  message_ = "马上就要下班啦，记得打卡，带好自己的东西~"
  return message_

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
message = get_message()
data = {
  "dateTime":{"value":get_today()+" "+get_weekdays(),"color":get_random_color()},
  "message":{"value":""+ message ,"color":get_random_color()},
}

res_boy = wm.send_template(boy_friend_id, template_id, data)
res_girl = wm.send_template(girl_friend_id, template_id, data)

