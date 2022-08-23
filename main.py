from ast import If
from datetime import date, datetime
from distutils.log import INFO
import math
import time
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import urllib
import urllib.request as request
import urllib.error as error
import json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 设置男朋友的账号
boy_friend_id = os.environ["BOY_FRIEND_ID"]
# 设置女朋友的账号
girl_friend_id = os.environ["GIRL_FRIEND_ID"]
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
  return time.strftime('%Y{}%m{}%d{}',time.localtime()).format("年","月","日")

def get_weather():
  api_url = 'http://apis.juhe.cn/simpleWeather/query'
  params_dict = {
      "city": city,  # 查询天气的城市名称，如：北京、苏州、上海
      "key": "5bf0c43ad287a8d60e506cbd8f9577cd",  # 您申请的接口API接口请求Key
  }
  params = urllib.parse.urlencode(params_dict)
  temperature = "1"
  humidity= "2"
  info= "3"
  direct= "4"
  power= "5"
  aqi= "6"
  message_ = "记得爱自己"
  try:
      req = request.Request(api_url, params.encode())
      response = request.urlopen(req)
      content = response.read()
      if content:
          try:
              result = json.loads(content)
              error_code = result['error_code']
              if (error_code == 0):
                  #温度
                  temperature = result['result']['realtime']['temperature']
                  #湿度
                  humidity = result['result']['realtime']['humidity']
                  #天气
                  info = result['result']['realtime']['info']
                  #风向
                  direct = result['result']['realtime']['direct']
                  #风力
                  power = result['result']['realtime']['power']
                  #空气质量
                  aqi = result['result']['realtime']['aqi']
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
                  return temperature,humidity,info,direct,power,aqi,message_
              else:
                  return temperature,humidity,info,direct,power,aqi,message_
          except Exception as e:
              return temperature,humidity,info,direct,power,aqi,message_
      else:
          # 可能网络异常等问题，无法获取返回内容，请求异常
         return temperature,humidity,info,direct,power,aqi,message_
  except error.HTTPError as err:
      return temperature,humidity,info,direct,power,aqi,message_
  except error.URLError as err:
      # 其他异常
      return temperature,humidity,info,direct,power,aqi,message_

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
# wea, temperature = get_weather()
wm_temperature, wm_humidity, wm_info, wm_direct, wm_power, wm_aqi, wm_message= get_weather()
data = {
  "dateTime":{"value":get_today()+" "+get_weekdays(),"color":get_random_color()},
  "weather":{"value":""+wm_info,"color":get_random_color()},
  "temperature":{"value":""+wm_temperature,"color":get_random_color()},
  "humidity":{"value":""+wm_humidity,"color":get_random_color()},
  "aqi":{"value":""+wm_aqi,"color":get_random_color()},
  "direct":{"value":""+wm_direct,"color":get_random_color()},
  "power":{"value":""+wm_power,"color":get_random_color()},
  "love_days":{"value":get_count(),"color":get_random_color()},
  "birthday_left":{"value":get_birthday(),"color":get_random_color()},
  "words":{"value":get_words(),"color":get_random_color()},
  "message":{"value":""+wm_message,"color":get_random_color()}
  }
  
res_boy = wm.send_template(boy_friend_id, template_id, data)
res_girl = wm.send_template(girl_friend_id, template_id, data)

