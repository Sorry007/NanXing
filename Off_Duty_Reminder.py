from datetime import date, datetime
from distutils.log import INFO
import time
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import os
import random
import requests
import http.client
import json

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
  return time.strftime('%Y{}%m{}%d{}',time.localtime()).format("年","月","日")

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_weather():
    conn = http.client.HTTPConnection("eolink.o.apispace.com")
    payload = ""
    headers = {
        "X-APISpace-Token":"f59cbztv2k9jfcgn84ilxv6kymglm5s7",
        "Authorization-Type":"apikey"
    }
    conn.request("GET","/456456/weather/v001/now?areacode=101020600", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    #体感温度
    temperature = result['result']['realtime']['feels_like']
    #湿度
    humidity = result['result']['realtime']['rh']
    #天气
    info = result['result']['realtime']['text']
    #风向
    direct = result['result']['realtime']['wind_dir']
    #风力
    power = result['result']['realtime']['wind_class']
    if "晴" in info:
      if temperature >= 35:
        message_ = "今日温度过高，注意做好防晒~"
      else:
        message_ = "今日温度适宜，记得多晒太阳，长高高~"

    if "云" in info:
      message_ = "今日温度适宜，记得多晒太阳，长高高~" 

    if "雨" in info:
      message_ = "今天可能会下雨🌧，记得带伞~" 

    if "雪" in info:
      message_ = "今天可能会下雪🌨，记得做好防护~" 

    if "阴" in info:
      message_ = "今天可能见不到太阳啦~" 

    if "雾" in info:
      message_ = "今天可见度会降低，小心别迷路~"
      
    return temperature,humidity,info,direct,power,message_



# 获取下班提醒
def get_message():
  message_ = "马上就要下班啦，记得打卡，带好自己的东西~"
  return message_

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
message = get_message()
wm_temperature, wm_humidity, wm_info, wm_direct, wm_power, wm_message= get_weather()
data = {
  "dateTime":{"value":get_today()+" "+get_weekdays(),"color":get_random_color()},
  "message":{"value":""+ message ,"color":get_random_color()},
  "weather":{"value":""+wm_info,"color":get_random_color()},
  "temperature":{"value":""+wm_temperature,"color":get_random_color()},
  "humidity":{"value":""+wm_humidity,"color":get_random_color()},
  "direct":{"value":""+wm_direct,"color":get_random_color()},
  "power":{"value":""+wm_power,"color":get_random_color()},
  "wm_message":{"value":""+wm_message,"color":get_random_color()}
  }
  
res_boy = wm.send_template(boy_friend_id, template_id, data)
# res_girl = wm.send_template(girl_friend_id, template_id, data)

