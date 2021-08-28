import math

import requests as requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class ShowAll:
    def __init__(self, __url_get_all_films, __buttons, __films_in_one_pagination):
        self.__url_get_all_films = __url_get_all_films
        self.__buttons = __buttons
        self.__films_in_one_pagination = __films_in_one_pagination
        self.__message_film_id = []
        self.__message_pagination_id = 0

    def show_all(self, update, context, offset=1):
        # print(self.__url_get_all_films)
        # print(self.__films_in_one_pagination)

        self.clear_mess(update, context)

        films_in_one_pagination = self.__films_in_one_pagination
        try:
            response = requests.get(
                url=self.__url_get_all_films,
            ).json()
        except Exception as exe:
            return

        if len(response) > films_in_one_pagination:
            buttons = self.__buttons.pagination_films(math.ceil(len(response) / films_in_one_pagination))
        else:
            buttons = self.__buttons.start_button()

        index = 0
        skip = films_in_one_pagination * (int(offset) - 1)
        keyboard = []
        for item in response:
            if skip > 0:
                skip -= 1
                index += 1
                continue
            films_in_one_pagination -= 1
            keyboard.append([InlineKeyboardButton(item['title'], callback_data=f"film/{item['_id']}")])

            index += 1
            if films_in_one_pagination == 0:
                break

        # print(f"keyboard = {keyboard}")
        if len(keyboard) > 0:
            message = context.bot.send_message(
                update.effective_chat.id,
                text="Фильмы",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            self.__message_film_id.append(message.message_id)

            message = context.bot.send_message(
                update.effective_chat.id,
                text='Страницы',
                reply_markup=buttons
            )
            self.__message_pagination_id = message.message_id

    def show_pagination_page(self, update, context):
        page = update.callback_query.data.split('/')
        self.show_all(update, context, page[1])

    def clear_mess(self, update, context):
        if len(self.__message_film_id) > 0:
            for index in range(len(self.__message_film_id)):
                context.bot.deleteMessage(
                    update.effective_chat.id,
                    self.__message_film_id.pop(0),
                )
        if self.__message_pagination_id != 0:
            context.bot.deleteMessage(
                update.effective_chat.id,
                self.__message_pagination_id,
            )
