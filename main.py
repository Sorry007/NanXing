from datetime import date, datetime
import math
import time
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 设置男朋友的账号
boy_friend_id = os.environ["BOY_FRIEND_ID"]
# 设置女朋友的账号
#girl_friend_id = os.environ["GIRL_FRIEND_ID"]
# 设置模板id
template_id = os.environ["TEMPLATE_ID"]

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
  now = datetime.datetime.now()
  # 格式化到日（varchar）
  return now.strftime("%Y-%m-%d")

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {
  "dateTime":{"value":get_today()+" "+get_weekdays(),"color":get_random_color()},
  "weather":{"value":wea,"color":get_random_color()},
  "temperature":{"value":temperature,"color":get_random_color()},
  "love_days":{"value":get_count(),"color":get_random_color()},
  "birthday_left":{"value":get_birthday(),"color":get_random_color()},
  "words":{"value":get_words(),"color":get_random_color()}}

res_boy = wm.send_template(boy_friend_id, template_id, data)
#res_girl = wm.send_template(girl_friend_id, template_id, data)

