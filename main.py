import datetime
import  cy_api
import random

help="目前功能如下(第一个括号后面是使用关键字)：\n增加对话（/add a->b）\n删除对话(/del a)\n今日人品（/jrrp）\n天气预报（/天气 城市名）(目前只收录了广州，北京，南京)\n定时提醒功能（在做了在做了）"
adddict={}

now = datetime.datetime.now()
path="E:/小赤雨本体/2.jpg"

while True:
    try:
        rev = cy_api.rev_msg()
        print(rev)
        if rev == None:
            continue
    except:
        continue
    if rev["post_type"] == "message":
        #print(rev) #需要功能自己DIY
        if rev["message_type"] == "private": #私聊
            if rev['raw_message']=='在吗':
                qq = rev['sender']['user_id']
                cy_api.send_msg({'msg_type':'private','number':qq,'msg':'[CQ:image,file=file:///{}]'.format(path)})
        elif rev["message_type"] == "group": #群聊
            group = rev['group_id']

            cy_api.add_function(adddict,rev) #添加对话功能

            cy_api.del_function(rev) #删除对话功能

            cy_api.group_get_send(rev,0,None,"/help",help) #帮助功能

            cy_api.group_get_send(rev,0,None,"/下班","小赤雨下班咯~")

            cy_api.jrrp_function(rev,now) #今日人品功能

            cy_api.weather_report(rev) #天气预报功能

            if "[CQ:at,qq=3591412706]" in rev["raw_message"]:
                if rev['raw_message'].split(' ')[1:3]=='你好':
                    cy_api.send_msg({'msg_type':'group','number':group,'msg':'[CQ:poke,qq={}]'.format(qq)})
                    cy_api.send_msg({'msg_type': 'group', 'number': group, 'msg': '大家好'})

        if now.hour == 0 and now.minute == 15:
            cy_api.send_msg({'msg_type': 'group', 'number':518293342, 'msg': '现在是'+str(now.hour)+'时'+str(now.minute)+"分"})
            cy_api.send_msg({'msg_type': 'private', 'number':1343238133, 'msg': '现在是'+str(now.hour)+'时'+str(now.minute)+"分"})
            print(now.hour,now.minute)

        else:
            continue
    else:  # rev["post_type"]=="meta_event":
        continue