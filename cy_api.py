import socket
import string
import json

import requests
import json
import random
import weather

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 8000))
ListenSocket.listen(100)

HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html
'''

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None

#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json

def get_group(id):
    response = requests.post('http://127.0.0.1:5700/get_group_member_list?group_id='+str(id)).json()
    for i in response['data']:
        if(i['card']!=''):
            print(i['card']+str(i['user_id']))
        else:
            print(i['nickname']+str(i['user_id']))

def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))

    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + str(msg) + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0

def judge(rev,mes,start,end):
    if rev['raw_message'][start:end]==mes:
        return True
    else:
        return False

def group_get_send(rev,start,end,mes,send):
    group = rev['group_id']
    if judge(rev,mes,start,end):
        send_msg({'msg_type': 'group', 'number': group, 'msg': send})

def add_dict(dict,rev,mes,start,end):
    group = rev['group_id']
    if judge(rev,mes,start,end):
        temp=rev['raw_message'][5:]
        res=temp.partition("->")
        dict[res[0]]=res[2]
        jsObj = json.dumps(dict)
        fileObject = open(r'save_dict.json', 'w')
        fileObject.write(jsObj)
        fileObject.close()
        send_msg({'msg_type': 'group', 'number': group, 'msg': "已添加"+res[0]+"->"+res[2]})

def del_dict(rev,mes,start,end):
    group = rev['group_id']
    if judge(rev,mes,start,end):
        key=rev['raw_message'][5:]
        with open("save_dict.json")as json_file:
            json_data = json.load(json_file)
        if key in json_data:
            del json_data[key]
            jsObj = json.dumps(json_data)
            fileObject = open(r'save_dict.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            send_msg({'msg_type': 'group', 'number': group, 'msg': "已删除"+key})
        else:
            send_msg({'msg_type': 'group', 'number': group, 'msg': "不存在“" + key+"”的关键词"})


def send_dict(rev):
    group = rev['group_id']
    with open("save_dict.json")as json_file:
        json_data = json.load(json_file)
    for key in json_data:
        if key == rev['raw_message']:
            send_msg({'msg_type': 'group', 'number': group, 'msg': json_data[key]})
            break

def add_function(adddict,rev):
    add_dict(adddict, rev, "/add ", 0, 5)
    send_dict(rev)

def del_function(rev):
    del_dict(rev, "/del ", 0, 5)

def jrrp_judge(qq,time):
    with open("save_jrrp.json")as json_file:
        try:
            json_data = json.load(json_file)
        except Exception as ex:
            print(ex)
    if qq in json_data:
        if json_data[qq] == time.day:
            return False
        else:
            return True
    else:
            return True

def jrrp_function(rev,time):
    s = str(random.randint(0,100))
    qq = str(rev['sender']['user_id'])
    group = rev['group_id']
    if rev['raw_message'] == '/jrrp':
        if jrrp_judge(qq,time):
            print("jrrp")
            send_msg({'msg_type': 'group', 'number': group, 'msg': "[CQ:at,qq="+qq+"]"+"你今日的人品是"+s+"（越低越好）"})
            dict = {}
            dict[qq] = time.day
            dict[qq+'jrrp'] = s
            jsObj = json.dumps(dict)
            fileObject = open(r'save_jrrp.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
        else:
            with open("save_jrrp.json")as json_file:
                json_data = json.load(json_file)
                for key in json_data:
                    if key == qq+'jrrp':
                        send_msg({'msg_type': 'group', 'number': group,
                                  'msg': "[CQ:at,qq=" + qq + "]" + "你今日的人品是" + json_data[key] + "（越低越好）"})

def weather_init(rev,name,url):
    group = rev['group_id']
    spider = weather.WeatherSpider()
    spider.init_url(url)
    data = spider.result()
    date = data['date']
    wea = data['weather']
    temp_max = data['temperature_max']
    temp_in = data['temperature_min']
    air = data['air_speed']
    send_msg({'msg_type': 'group', 'number': group,
              'msg': name + date + "的天气情况：" + "天气：" + wea + " 温度: " + temp_in + "~" + temp_max + " 风速：" + air})

def weather_report(rev):
    if rev['raw_message'][0:3] == '/天气':
        spider = weather.WeatherSpider()
        if rev['raw_message'][4:] == '广州':
            weather_init(rev,"广州","http://www.weather.com.cn/weather/101280101.shtml")
        if rev['raw_message'][4:] == '北京':
            weather_init(rev, "北京", "http://www.weather.com.cn/weather/101010100.shtml")
        if rev['raw_message'][4:] == '南京':
            weather_init(rev, "南京", "http://www.weather.com.cn/weather/101190101.shtml")








