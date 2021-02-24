import random
import asyncio
import aiovk
import time
import db
class Bot:
    def __init__(self):
        self.capitals_quize = [('1', 'Чехии', 'Прага'), ('2', 'Италии', 'Рим'), ('3', 'Греции', 'Афины'),
                               ('4', 'Испании', 'Мадрид'),
                               ('5', 'Канады', 'Оттава'), ('6', 'Ливии', 'Триполи'), ('7', 'Кении', 'Найроби'),
                               ('8', 'Боливии', 'Сукре'), ('9', 'Йемена', 'Сана'), ('10', 'Гайаны', 'Джорджтаун')]
        # {"peer_id" : "last_q"}
        self.history = {}
        # {"peer_id": {"user_id" : "result"}}
        self.results = {}
        self.TOKEN = 'eab10371bb86ac259709c026c81c7b774c1fc9ae13c484c55e377598551cc92e63840a6518a14eb955d28'
        self.session = aiovk.TokenSession(access_token=self.TOKEN)
        self.api = aiovk.API(self.session)
        self.lp = aiovk.longpoll.BotsLongPoll(self.session, group_id=202376739)
        self.delay = 10
        self.database = db.DB()
        asyncio.get_event_loop().run_until_complete(self.connect())

    async def ask_question(self):
        peer_id = self.event['object']['message']['peer_id'];
        i = await self.database.select_in_history(peer_id)
        await self.write_message(message="-------------------------------------")
        await self.write_message(message="Вопрос №" + self.capitals_quize[i][0])
        await self.write_message(message="Назовите столицу " + self.capitals_quize[i][1])
        print(await self.database.select_in_history(peer_id))
        await asyncio.sleep(self.delay)
        print(await self.database.select_in_history(peer_id))
        if i == await self.database.select_in_history(peer_id):
            await self.write_message(message="Время вышло...")
            await self.write_message(message="Правильный ответ : " + self.capitals_quize[i][2])
            await self.database.update_in_history(peer_id,i+1)
            await self.ask_question()

    async def start_game(self):
        peer_id = self.event['object']['message']['peer_id'];
        await self.database.insert_in_history(peer_id)
        #self.history[self.event['object']['message']['peer_id']] = 0;
        #self.results[peer_id] = {}
        await self.database.delete_in_results(peer_id)
        await self.write_message(message="Ну погнали");
        await self.ask_question()

    async def stop_game(self):
        peer_id = self.event['object']['message']['peer_id'];
        #del self.history[self.event['object']['message']['peer_id']]
        await self.database.delete_in_history(peer_id)
        await self.write_message("Игра закончена. Результаты:");
        await self.top()

    async def top(self):
        peer_id = self.event['object']['message']['peer_id'];
        await self.write_message("ТОП")
        await self.write_message("-------------------------------------")
        results = await self.database.select_in_results(peer_id)
        for row in results:
            user = await self.api('users.get', user_ids=row[0])
            name = str(user[0]['first_name']) + ' ' + str(user[0]['last_name'])
            await self.write_message(name + " : " + str(row[1]))
        await self.write_message("-------------------------------------")

    async def get_answer(self):
        peer_id = self.event['object']['message']['peer_id']
        i = await self.database.select_in_history(peer_id)
        chg1 = self.event['object']['message']['text'].lower()
        if chg1 == self.capitals_quize[i][2].lower():
            await self.write_message(message="Верно, на полке два пирожка,возьми средний")
            await self.database.update_in_history(peer_id,i+1)
            #self.history[peer_id] = i + 1
            i += 1
            sender = self.event['object']['message']['from_id']
            if await self.database.peer_id_in_results(peer_id,sender):
                await self.database.update_in_results(peer_id,sender,1)
            else:
                await self.database.insert_in_results(peer_id,sender)
            if i == 10:
                await self.stop_game()
            else:
                await self.ask_question()
        else:
            await self.write_message(message="Неверно, попробуй ещё")

    async def connect(self):
        async with aiovk.TokenSession(access_token=self.TOKEN) as session:
            async for self.event in self.lp.iter():
                print(self.event)
                if self.event['type'] == "message_new":
                    # Слушаем longpoll, если пришло сообщение то:
                    chg = self.event['object']['message']['text'].lower()
                    peer_id = self.event['object']['message']['peer_id'];
                    #print(await self.database.peer_id_in_history(peer_id))
                    if chg == 'закончить игру':
                        await self.stop_game()
                    elif chg == 'топ':
                        await self.top()

                    elif await self.database.peer_id_in_history(peer_id):
                        #print(await self.database.peer_id_in_history(peer_id))
                        asyncio.create_task(self.get_answer())
                        # await self.get_answer()
                    elif chg == 'начать игру':
                        asyncio.create_task(self.start_game())

    async def write_message(self, message):
        await self.api('messages.send', peer_id=self.event['object']['message']['peer_id'], message=message,
                       random_id=random.getrandbits(64))
