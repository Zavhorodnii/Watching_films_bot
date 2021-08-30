import math
import DataBase
from threading import Thread
from datetime import datetime, timedelta
from time import sleep

import requests
from pytz import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Threads:

    def __init__(self, __buttons,
                 __day_before_notification,
                 __time,
                 __effective_chat_id,
                 __context,
                 __films_in_one_pagination,
                 __url_get_all_films,
                 __message_film_id=[],
                 __message_pagination_id=0):
        # print('init threads')
        self.__buttons = __buttons
        self.__day_before_notification = __day_before_notification
        self.__time = __time
        self.__effective_chat_id = __effective_chat_id
        self.__context = __context
        self.__films_in_one_pagination = __films_in_one_pagination
        self.__url_get_all_films = __url_get_all_films
        self.__thread = None

        self.__message_film_id = __message_film_id
        self.__message_pagination_id = __message_pagination_id
        self.__database = DataBase.DataBase()

    def start_thread(self):
        # print('thread start')
        thread = Thread(target=self.create_thread, args=())
        self.__thread = thread
        thread.start()

    def create_thread(self):
        while True:
            rem_time = datetime.strptime(str(datetime.now().date()) + ' ' + self.__time + ':00', "%Y-%m-%d %H:%M:%S")
            ukraine_time = timezone('Europe/Kiev')
            time_now = datetime.now(ukraine_time).replace(tzinfo=None)
            if rem_time.time() <= time_now.time():
                # print('send mes')
                self.thread_send_films()

                time = ((rem_time + timedelta(days=1)) - time_now)
                sleep_time = time.total_seconds()
            else:
                # print('not send')
                sleep_time = (rem_time - time_now).total_seconds()

            # print(f"sleep_time = {sleep_time}")
            sleep(sleep_time)

    def thread_send_films(self, offset=0):
        self.clear_mess()
        films_in_one_pagination = self.__films_in_one_pagination
        try:
            response = requests.get(
                url=self.__url_get_all_films,
            ).json()
            # print(response)
        except Exception as exe:
            return

        __film = []
        ukraine_time = timezone('Europe/Kiev')
        time_now = datetime.now(ukraine_time).replace(tzinfo=None)
        for item in response:
            # print(f"time = {(time_now + timedelta(days=self.__day_before_notification)).date()}")
            # date = datetime.strptime(item['datetime'], "%Y-%m-%d").date()
            # print(f"film = {date}")
            if (time_now + timedelta(days=self.__day_before_notification)).date() == datetime.strptime(item['datetime'], "%Y-%m-%d").date() :
                # print('+')
                __film.append(item)

        # print(response)
        buttons = self.__buttons.pagination_remind(math.ceil(len(__film) / films_in_one_pagination))
        index = 0
        keyboard = []
        skip = films_in_one_pagination * (int(offset) - 1)
        # print(f"films = {__film}")
        for item in __film:
            if skip > 0:
                skip -= 1
                index += 1
                continue
            films_in_one_pagination -= 1
            keyboard.append([InlineKeyboardButton(item['title'], callback_data=f"film/{item['_id']}")])

            index += 1
            if films_in_one_pagination == 0:
                break

        if len(__film) > 0:
            message = self.__context.bot.send_message(
                self.__effective_chat_id,
                text="Фильмы",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            self.__message_film_id.append(message.message_id)

            message = self.__context.bot.send_message(
                self.__effective_chat_id,
                text='Страницы напоминания',
                reply_markup=buttons
            )
            self.__message_pagination_id = message.message_id
            self.__database.add_remind(self.__message_film_id,
                                       self.__message_pagination_id,
                                       self.__effective_chat_id)

    def show_pagination_page(self, update, context):
        page = update.callback_query.data.split('/')
        # print(page)
        self.thread_send_films(page[1])

    def clear_mess(self):
        # try:
        if len(self.__message_film_id) > 0:
            for index in range(len(self.__message_film_id)):
                self.__context.bot.deleteMessage(
                    self.__effective_chat_id,
                    self.__message_film_id.pop(0),
                )
        if self.__message_pagination_id != 0:
            self.__context.bot.deleteMessage(
                self.__effective_chat_id,
                self.__message_pagination_id,
            )
        self.__message_pagination_id = 0

        # print(self.__message_pagination_id)
        # except Exception as exe:
        #     return