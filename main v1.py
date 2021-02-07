
import vk_api, json
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='eab10371bb86ac259709c026c81c7b774c1fc9ae13c484c55e377598551cc92e63840a6518a14eb955d28')

longpoll = VkLongPoll(vk_session)




def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:

                msg = event.text.lower()
                id = event.chat_id

                if msg == 'привет':
                    sender(id, 'Hi ')
                if msg == 'пока':
                    sender(id, 'Ну пока ')
                if msg == 'Спокойной ночи':
                    sender(id, 'Споки ноки')
                if msg == 'Ты красавчик':
                    sender(id, 'Нет, ты красавчик')
                if msg == 'cпасибо':
                    sender(id, 'Обращайся')
             #   else :
             #       sender(id, 'Я тебя не понимаю')