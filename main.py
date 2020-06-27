import vk_api  # Библиотека VK
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType  # Библиотека VK LongPool
import random
from datetime import datetime, timedelta
import time
import re
import json
import wikipedia
wikipedia.set_lang("RU")
now = datetime.now()

# Настройки
token = "2104cf20acdf3fa79f6801cd0db84a1d5cc613d3df7940d1da07689bae4376bfaf96cd30cf0fb39802548"  # Личный access_token сообщества (Желателен полный доступ)
group_id = "180982284"  # ID сообщества ы
longpool_sleep = "0.5"  # Задержка проверки сообщений, зависит от нагрузки на сервер (Рекомендуется значение от 0.1 до 10)
YOURFILENAME = "vkbot.json"
# VK LongPool
vk_session = vk_api.VkApi(token=token)  # Обработка access_token
longpoll = VkBotLongPoll(vk_session, group_id)  # Данные для работы в сообществе
vk = vk_session.get_api()  # Работа с VK API

# Сообщения

for event in longpoll.listen():
    try:

        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text.lower() == "start" or event.obj.text.lower() == "старт":
            global m
            with open(YOURFILENAME, "r") as j:
                m = json.load(j)
                j.close()
            if len(m) == 0:
                m = {}

                members = vk.messages.getConversationMembers(peer_id=event.obj.peer_id, fields='member_id')['items']
                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                message = ''
                for member_id in members_ids:
                    message += f' {member_id}'
                    m[str(member_id)] = {"ban": 0, "mute": 0, "admin": 0, "warn": 0}
                    print({member_id})
                    # vk.messages.send(peer_id = event.obj.peer_id, random_id = 0, message = f'{member_id}')

            vk.messages.send(peer_id = event.obj.peer_id, random_id = 0, message = f'Бот запущен в данной беседе!' )

        # Проверка участника на мут при отправке сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            User_ID = event.object.from_id
            if m[str(User_ID)]["mute"] == 1:
                vk.messages.removeChatUser(chat_id=event.chat_id, user_id=User_ID)

        #if event.type == VkBotEventType.MESSAGE_NEW:
            #response = event.obj.text.lower()
            #if response.split(' ')[0] == "spam":
                #vk.messages.send(peer_id=event.obj.peer_id, random_id=0,message=f'[id{218967539}|s] ')
                #while True:
                    #vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'[id{218967539}|💚 ] ')



        #Варн
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "warn":
                aidi = re.findall('(\d+)', response.split(' ')[1])
                results = ''.join(aidi)
                User_ID = event.object.from_id
                if m[str(User_ID)]["admin"] == 1:
                    m[str(results[0:9])]["warn"] += 1
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0,
                                     message=f'[id{results[0:9]}|Пользователю] выдано предупреждение [' + str(
                                         m[str(results[0:9])]["warn"]) + "/3]")
                    if m[str(results[0:9])]["warn"] == 3:
                        vk.messages.removeChatUser(chat_id=event.chat_id, user_id= results[0:9])
                else:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'Вы не администратор.')

        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "unwarn":
                aidi = re.findall('(\d+)', response.split(' ')[1])
                results = ''.join(aidi)
                User_ID = event.object.from_id
                if m[str(User_ID)]["admin"] == 1:
                    m[str(results[0:9])]["warn"] -= 1
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0,message=f'[id{results[0:9]}|Пользователю] снято предупреждение [' + str(m[str(results[0:9])]["warn"]) + "/3]")
                else:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'Вы не администратор.')






        # Википедия
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "вики":
                viki = response.split(' ')[1]
                vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message= "Вот, что я нашла:\n" + str(wikipedia.summary(viki)))

        #Выдать админку
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "setadmin":
                aidi = re.findall('(\d+)', response.split(' ')[1])
                results = ''.join(aidi)
                for element in vk.messages.getConversationMembers(peer_id=event.obj.peer_id, fields='items')['items']:
                    admin = element.get('is_admin', False)
                    owner = element.get('is_owner', False)
                    id = element.get('member_id')
                    member = event.object.from_id
                    if id == member:
                        if admin == True or owner == True:
                            m[str(results[0:9])]["admin"] += 1
                            vk.messages.send(peer_id = event.obj.peer_id, random_id = 0, message = f'[id{results[0:9]}|Пользователь] назначен администратором!')
                        else:
                            vk.messages.send(peer_id = event.obj.peer_id, random_id = 0, message = f'У вас нет прав!')
        #Кик участника
        if event.type == VkBotEventType.MESSAGE_NEW:
            member = event.object.from_id
            response = event.obj.text.lower()
            if response.split(' ')[0] == "kick":
                aidi = re.findall('(\d+)', response.split(' ')[1])
                results = ''.join(aidi)
                if m[str(member)]["admin"] == 1:
                    vk.messages.removeChatUser(chat_id=event.chat_id, user_id=results[0:9])
                else:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'Вы не администратор.')


        # if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text.lower() == "stop" or event.obj.text.lower() == "время":
        # with open(YOURFILENAME, "w") as j:
        # j.write( json.dumps(m) )
        # j.close()

        #Мут
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "mute":
                aidi = re.findall('(\d+)', response.split(' ')[1])
                results = ''.join(aidi)
                if m[str(member)]["admin"] == 1:
                    m[str(results[0:9])]["mute"] += 1
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0,message=f'[id{results[0:9]}|Пользователь] получил мут. При отправке сообщения он будет исключен.')
                else:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'Вы не администратор.')
        #Анмут
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "unmute":
                aidi = re.findall('(\d+)', response.split(' ')[1])
                results = ''.join(aidi)
                if m[str(member)]["admin"] == 1:
                    m[str(results[0:9])]["mute"] -= 1
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0,message=f'У [id{results[0:9]}|Пользователя] снят мут.')
                else:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'Вы не администратор.')

        # Время
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "time":
                hour = now.strftime("%H")
                minutes = now.strftime("%M")
                seconds = now.strftime("%S")
                vk.messages.send(peer_id=event.obj.peer_id, random_id=0,
                                 message='Текущее время: ' + str(hour) + ":" + str(minutes) + ":" + str(seconds))

        # Упомянуть всех участников беседы
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.obj.text.lower()
            if response.split(' ')[0] == "сбор":
                User_ID = event.object.from_id
                members = vk.messages.getConversationMembers(peer_id=event.obj.peer_id, fields='member_id')['items']
                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                message = ''
                for member_id in members_ids:
                    message += f'[id{member_id}|☎]'
                if m[str(member)]["admin"] == 1:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0,message=f'Вы были вызваны [id{User_ID}|начальником]!\n' + message + '\n Причина вызова: ' + response.split(' ')[1])
                else:
                    vk.messages.send(peer_id=event.obj.peer_id, random_id=0, message=f'Вы не администратор.')

    except Exception as E:
        print(Exception)
        time.sleep(1)
