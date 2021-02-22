import random
import asyncio
import aiovk


capitals_quize = [('1', 'Чехии', 'Прага'), ('2', 'Италии', 'Рим'),('3', 'Греции', 'Афины'),('4', 'Испании', 'Мадрид'),('5', 'Канады', 'Оттава'),('6', 'Ливии', 'Триполи'),('7', 'Кении', 'Найроби'),('8', 'Боливии', 'Сукре'),('9', 'Йемена', 'Сана'),('10', 'Гайаны', 'Джорджтаун')]


async def start_game(api,event,lp):
    await write_message(api, event, "Ну погнали")
    for i in range(len(capitals_quize)):
        await write_message(api, event, "Вопрос №" + capitals_quize[i][0])
        await write_message(api, event, "Назовите столицу " + capitals_quize[i][1])
        async for event1 in lp.iter():
            chg1=event1['object']['message']['text'].lower()
            if chg1 == "закончить игру":
                return;
            
            if chg1 == capitals_quize[i][2].lower():
                await write_message(api, event1, "Верно, на полке два пирожка,возьми средний")
                break;
            else:
                await write_message(api, event1, "Неверно, попробуй ещё")
			
async def func():
    TOKEN = 'eab10371bb86ac259709c026c81c7b774c1fc9ae13c484c55e377598551cc92e63840a6518a14eb955d28'
    async with aiovk.TokenSession(access_token=TOKEN) as session:
        api = aiovk.API(session)
        lp = aiovk.longpoll.BotsLongPoll(session, group_id=202376739)
        async for event in lp.iter():
            
            if event['type'] == "message_new":
            #Слушаем longpoll, если пришло сообщение то:
                chg=event['object']['message']['text'].lower()
                sender=event['object']['message']['from_id']
                print(len(capitals_quize))
                if chg == 'начать игру':
                    await start_game(api,event,lp)
                    

async def write_message(api, event,message1):
    await api('messages.send', peer_id=event['object']['message']['peer_id'], message=message1, random_id = random.getrandbits(64))


loop = asyncio.get_event_loop()
loop.run_until_complete(func())

