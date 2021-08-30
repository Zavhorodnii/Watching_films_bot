# import pymysql as pymysql
import psycopg2

class DataBase:
    def __init__(self):
        # self.__my_db_connector = pymysql.connect(
        #      host='localhost',
        #      user='root',
        #      password='root',
        #      database='watching_films_bot',
        #      charset='utf8mb4',
        # )
        # self.__my_db_connector = None
        self.__check_or_create_database = "CREATE DATABASE IF NOT EXISTS watching_films_bot"
        self.__create_db_table_settings = "CREATE TABLE IF NOT EXISTS settings(" \
                                          "chat_id VARCHAR(100), " \
                                          "films_in_one_pagination INT DEFAULT '5', " \
                                          "day_notification INT DEFAULT '7', " \
                                          "check_time VARCHAR(10) DEFAULT '12:00', " \
                                          "last_messages TEXT, " \
                                          "last_pagination VARCHAR(10) DEFAULT '0', " \
                                          "last_remind_messages TEXT, " \
                                          "last_remind_pagination VARCHAR(10) DEFAULT '0')"

        self.__select_settings = "select * from settings where chat_id = %s;"
        self.__select_all_settings = "select * from settings"
        self.__add_settings = "INSERT INTO settings (chat_id, films_in_one_pagination, day_notification, check_time) " \
                              "VALUES (%s, %s, %s, %s)"
        self.__update_settings = "UPDATE settings SET films_in_one_pagination = %s, day_notification = %s, " \
                                 "check_time = %s WHERE chat_id = %s"
        self.__update__messages = "UPDATE settings SET last_messages = %s, last_pagination = %s WHERE chat_id = %s"
        self.__update__remind = "UPDATE settings SET last_remind_messages = %s, last_remind_pagination = %s WHERE chat_id = %s"

    def create_connection(self):
        return psycopg2.connect(
            host='ec2-54-73-58-75.eu-west-1.compute.amazonaws.com',
            user='uqhhxycoxaihxq',
            password='91d4691c14c330a8c414d28147747114df451ce5fa802cd6263dd185a9650e7f',
            database='d1sm8k1mutg65v',
            # charset='utf8mb4',
            # cursorclass=pymysql.cursors.DictCursor
        )

    def check_or_create_db(self):
        mydb = self.create_connection()
        try:
            with mydb:
                __cur = mydb.cursor()
                __cur.execute(self.__check_or_create_database)
                __cur.close()
        except Exception as exe:
            pass

        # self.__my_db_connector = mydb
        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __cur = __my_db_connector.cursor()
            __cur.execute(self.__create_db_table_settings)
            __cur.close()

    def add_chat(self, chat_id, films_in_one_pagination, day_notification, check_time):
        # print("create chat")
        in_table = self.select_chat_settings(chat_id)
        if len(in_table) > 0:
            # print("in_table")
            self.update_settings(films_in_one_pagination, day_notification, check_time, chat_id)
            return
        # print("create")
        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__add_settings, (str(chat_id),
                                                str(films_in_one_pagination),
                                                str(day_notification),
                                                str(check_time)))
            __my_db_connector.commit()

    def select_chat_settings(self, chat_id):
        # print(f"chat_id = {chat_id}")
        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__select_settings, (str(chat_id),))
            all = __con.fetchall()
            __con.close()
        return all

    def select_all_chat_settings(self):
        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__select_all_settings)
            all = __con.fetchall()
            __con.close()
        return all

    def update_settings(self, films_in_one_pagination, day_notification, check_time, chat_id):
        in_table = self.select_chat_settings(chat_id)
        if len(in_table) == 0:
            return

        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__update_settings, (str(films_in_one_pagination),
                                                    str(day_notification),
                                                    str(check_time),
                                                    str(chat_id)))
            __my_db_connector.commit()

    def add_messages(self, last_messages, last_pagination, chat_id):
        in_table = self.select_chat_settings(chat_id)
        if len(in_table) == 0:
            return

        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__update__messages, (';'.join(map(str, last_messages)),
                                                str(last_pagination),
                                                str(chat_id)))
            __my_db_connector.commit()

    def add_remind(self, last_remind_messages, last_remind_pagination, chat_id):
        in_table = self.select_chat_settings(chat_id)
        if len(in_table) == 0:
            return

        __my_db_connector = self.create_connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__update__remind, (';'.join(map(str, last_remind_messages)),
                                                str(last_remind_pagination),
                                                str(chat_id)))
            __my_db_connector.commit()