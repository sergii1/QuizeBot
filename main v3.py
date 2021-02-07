import random

import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def write_message(sender,message):
    authorize.method('messages.send', {'chat_id': sender, 'message': message,'random_id': random.getrandbits(64)})

authorize = vk_api.VkApi(token='eab10371bb86ac259709c026c81c7b774c1fc9ae13c484c55e377598551cc92e63840a6518a14eb955d28')

longpoll = VkBotLongPoll(authorize, group_id=202376739)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text')!='':
    #Слушаем longpoll, если пришло сообщение то:
        chg=event.message.get('text')
        sender=event.chat_id
        if chg == 'привет' or chg == 'Второй вариант фразы': #Если написали заданную фразу
           write_message(sender,'ну привет')
