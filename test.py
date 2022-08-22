from contextlib import nullcontext
import urllib
import urllib.request as request
import urllib.error as error
import json
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
                      message_ = "今日温度过高，注意做好防晒呀🌞"
                    else:
                      message_ = "今日温度适宜，记得多晒太阳，长高高~😊"
                  else:
                    message_ = "今日温度适宜，记得多晒太阳，长高高~😊"

                  if "云" in info:
                    message_ = "今日温度适宜，记得多晒太阳，长高高~😊" 

                  if "雨" in info:
                    message_ = "今天可能会下雨🌧，记得带伞🌂" 

                  if "雪" in info:
                    message_ = "今天可能会下雪🌨，记得做好防护呀~☔" 

                  if "阴" in info:
                    message_ = "今天可能见不到太阳啦，但也不能没有阳光呀🌞" 

                  if "雾" in info:
                    message_ = "今天可见度会降低，小心别迷路呀~😜"
                  print("温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
                      temperature, humidity, info, direct, power, aqi))
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
wm_temperature,wm_humidity,wm_info,wm_direct,wm_power,wm_aqi,wm_message= get_weather()
print(wm_temperature)