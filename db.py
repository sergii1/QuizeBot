import psycopg2
import asyncio

class DB:
    def __init__(self):
        self.connection = psycopg2.connect(database="test", user="postgres", password="1", host="localhost", port=5432)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS history(
             peer_id INT PRIMARY KEY,
             last_question INT);
        """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS results(
            peer_id INT,
		    user_id INT,
		    result INT,
		    PRIMARY KEY(peer_id,user_id)   
		    );
		""")
        self.connection.commit()

    async def insert_in_history(self,peer_id):
        self.cursor.execute("INSERT INTO history VALUES(" + str(peer_id) + ", 0);")
        self.connection.commit()

    async def update_in_history(self,peer_id,last_question):
        self.cursor.execute("UPDATE history set last_question=" + str(last_question) + " where peer_id=" + str(peer_id) + ";")
        self.connection.commit()

    async def delete_in_history(self,peer_id):
        self.cursor.execute("DELETE from history where peer_id=" + str(peer_id) + ";")
        self.connection.commit()

    async def select_in_history(self,peer_id):
        self.cursor.execute("SELECT last_question from history where peer_id=" + str(peer_id) + ";")
        self.connection.commit()
        for row in self.cursor:
            return(row[0])


    async def peer_id_in_history(self,peer_id):
        cur = self.cursor.execute("SELECT * from history where peer_id=" + str(peer_id) + ";")
        self.connection.commit()
        for row in self.cursor:
            return True
        return False

    async def insert_in_results(self,peer_id,user_id):
        self.cursor.execute("INSERT INTO results VALUES(" + str(peer_id) + "," + str(user_id) + ", 1);")
        self.connection.commit()

    async def delete_in_results(self,peer_id):
        self.cursor.execute("DELETE from results where peer_id=" + str(peer_id) + ";")
        self.connection.commit()

    async def peer_id_in_results(self,peer_id,user_id):
        cur = self.cursor.execute("SELECT * from results where peer_id=" + str(peer_id) + " and user_id=" + str(user_id) + ";")
        self.connection.commit()
        for row in self.cursor:
            return True
        return False

    async def select_in_results(self,peer_id):
        self.cursor.execute("SELECT user_id,result from results where peer_id=" + str(peer_id) + ";")
        self.connection.commit()
        return self.cursor

    async def update_in_results(self,peer_id,user_id,score):
        self.cursor.execute("SELECT result from results where peer_id=" + str(peer_id) + " and user_id=" + str(user_id) + ";")
        for row in self.cursor:
            ex_score=row[0]
        self.cursor.execute("UPDATE results set result=" + str(ex_score+score) + " where peer_id=" + str(peer_id) + " and user_id=" + str(user_id) + ";")
        self.connection.commit()










