import  cy_api
import random

help="目前功能如下(第一个括号后面是使用关键字)：\n增加对话（/add a->b）\n删除对话(/del a)\n今日人品（/jrrp）（待完善）\n"
adddict={}

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
                cy_api.send_msg({'msg_type':'private','number':qq,'msg':'我在'})
        elif rev["message_type"] == "group": #群聊
            group = rev['group_id']
            cy_api.add_function(adddict,rev)
            cy_api.del_function(rev)
            cy_api.group_get_send(rev,0,None,"/help",help)
            cy_api.group_get_send(rev,0,None,"/下班","小赤雨下班咯~")
            if "[CQ:at,qq=3591412706]" in rev["raw_message"]:
                if rev['raw_message'].split(' ')[1:3]=='你好':
                    cy_api.send_msg({'msg_type':'group','number':group,'msg':'[CQ:poke,qq={}]'.format(qq)})
                    cy_api.send_msg({'msg_type': 'group', 'number': group, 'msg': '大家好'})
            if rev['raw_message'] == '/jrrp':
                s=str(random.randint(1,100))
                qq = str(rev['sender']['user_id'])
                cy_api.send_msg({'msg_type': 'group', 'number': group, 'msg': "[CQ:at,qq="+qq+"]"+"你今日的人品是"+s+"（越低越好）"})

        else:
            continue
    else:  # rev["post_type"]=="meta_event":
        continue