import logging

import telegram

import Start
import ShowAll
import ShowOne
import Buttons
import SecretInfo
import Settings
import Threads
import DataBase


from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALL, ONE, SETTINGS_PAGINATION, SETTINGS_TIME, SETTINGS_DAY_BEFORE_NOTIFICATION = range(5)


class WatchingFilms:
    def __init__(self, films_in_one_pagination=2, day_notification=7, check_time='12:00', __this_class=None):
        # print('init all')
        self.__url_get_all_films = 'https://films-assembly.pp.ua/api/films'
        self.__url_get_one_film = 'https://films-assembly.pp.ua/api/film/'
        self.__films_in_one_pagination = films_in_one_pagination
        self.__buttons = Buttons.Buttons()
        self.__settings = Settings.Settings(self.__buttons)
        self.__start = Start.Start()
        self.__show_all = None
        self.__show_one = ShowOne.ShowOne(self.__url_get_one_film)
        self.__check_time = check_time
        self.__day_notification = day_notification
        self.__thread = None
        self.__this_class = __this_class
        self.dispatcher = None

    def update_restart(self):
        database = DataBase.DataBase()
        database.check_or_create_db()
        chat_settings = database.select_all_chat_settings()
        # print(f"dis = {self.dispatcher}")
        telegram_bot = telegram.ext.callbackcontext.CallbackContext(self.dispatcher)

        for chat in chat_settings:
            if chat[6] is not None:
                array_str = chat[6].split(';')
            else:
                array_str = []
            # print(f"len = {len_}")
            # if len_ > 0:
            #     print('split')

            self.__thread = Threads.Threads(self.__buttons,
                                            chat[2],
                                            chat[3],
                                            chat[0],
                                            telegram_bot,
                                            chat[1],
                                            self.__url_get_all_films,
                                            array_str,
                                            chat[7])
            self.__thread.start_thread()


    def start(self, update, context):
        self.__start.start(update, context)
        return SETTINGS_PAGINATION

    def restart_bot(self, update, context):
        data_base = DataBase.DataBase()
        chat_settings = data_base.select_chat_settings(update.effective_chat.id)
        self.__films_in_one_pagination = chat_settings[0][1]
        self.__day_notification = chat_settings[0][2]
        self.__check_time = chat_settings[0][3]

    def setting_pagination(self, update, context):
        self.__films_in_one_pagination = self.__settings.settings_pagination(update, context)
        self.__show_all = ShowAll.ShowAll(self.__url_get_all_films, self.__buttons, self.__films_in_one_pagination)
        return SETTINGS_DAY_BEFORE_NOTIFICATION

    def settings_day_notification(self, update, context):
        self.__day_notification = self.__settings.settings_day_notification(update, context)
        return SETTINGS_TIME

    def setting_time(self, update, context):
        self.__check_time = self.__settings.settings_time(update, context)
        self.__thread = Threads.Threads(self.__buttons,
                                        self.__day_notification,
                                        self.__check_time,
                                        update.effective_chat.id,
                                        context,
                                        self.__films_in_one_pagination,
                                        self.__url_get_all_films)
        self.__thread.start_thread()
        database = DataBase.DataBase()
        database.add_chat(update.effective_chat.id,
                          self.__films_in_one_pagination,
                          self.__day_notification,
                          self.__check_time)
        return ALL

    # def update(self, update: object) -> Optional[Union[bool, object]]:
    #     print(f"1 = {type(update)}")

    def reminder_pagination(self, update, context):
        try:
            self.__thread.show_pagination_page(update, context)
        except Exception as exe:
            self.restart_bot(update, context)
            database = DataBase.DataBase()
            chat_settings = database.select_chat_settings(update.effective_chat.id)
            if chat_settings[0][6] is not None:
                array_str = chat_settings[0][6].split(';')
            else:
                array_str = []
            self.__thread = Threads.Threads(self.__buttons,
                                            self.__day_notification,
                                            self.__check_time,
                                            chat_settings[0][0],
                                            context,
                                            self.__films_in_one_pagination,
                                            self.__url_get_all_films,
                                            array_str,
                                            chat_settings[0][7])
            self.__thread.start_thread()
            # self.__thread.show_pagination_page(update, context)

        return ALL

    def show_all(self, update, context):
        try:
            self.__show_all.show_all(update, context)
        except Exception as exe:
            try:
                self.restart_bot(update, context)
            except Exception as exe:
                return ;
            database = DataBase.DataBase()
            chat_settings = database.select_chat_settings(update.effective_chat.id)
            if chat_settings[0][4] is not None:
                array_str = chat_settings[0][4].split(';')
            else:
                array_str = []
            self.__show_all = ShowAll.ShowAll(self.__url_get_all_films, self.__buttons, self.__films_in_one_pagination,
                                              array_str,
                                              chat_settings[0][5])
            self.__show_all.show_all(update, context)
        return

    def show_pagination_page(self, update, context):
        try:
            self.__show_all.show_pagination_page(update, context)
        except Exception as exe:
            self.restart_bot(update, context)
            database = DataBase.DataBase()
            chat_settings = database.select_chat_settings(update.effective_chat.id)
            self.__show_all = ShowAll.ShowAll(self.__url_get_all_films, self.__buttons, self.__films_in_one_pagination,
                                              chat_settings[0][4].split(';'),
                                              chat_settings[0][5])
            self.__show_all.show_pagination_page(update, context)
        return ALL

    def show_one_film(self, update, context):
        self.__show_one.show_one_film(update, context)
        return ALL

    def main(self):
        updater = Updater(SecretInfo.TELEGRAM_HTTP_API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        self.dispatcher = dispatcher

        self.update_restart()

        control_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', self.start),
                MessageHandler(Filters.regex('Узреть список почти шедевров'), self.show_all),
                CallbackQueryHandler(self.show_one_film, pass_user_data=True, pattern="film/"),
                CallbackQueryHandler(self.show_pagination_page, pass_user_data=True, pattern="page/"),
                CallbackQueryHandler(self.reminder_pagination, pass_user_data=True, pattern="remind/"),
            ],
            states={
                SETTINGS_PAGINATION: [
                    MessageHandler(Filters.regex(r"^(?:[1-9]\d*(?:\.\d+)?|0\.0*[1-9]\d*)$"), self.setting_pagination, )
                ],
                SETTINGS_DAY_BEFORE_NOTIFICATION: [
                    MessageHandler(Filters.regex(r"^(?:[1-9]\d*(?:\.\d+)?|0\.0*[1-9]\d*)$"),
                                   self.settings_day_notification, )
                ],
                SETTINGS_TIME: [
                    MessageHandler(Filters.regex(r"^(0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9]$"), self.setting_time, )
                ],
                ALL: [
                    MessageHandler(Filters.regex('Узреть список почти шедевров'), self.show_all),
                    CallbackQueryHandler(self.show_one_film, pass_user_data=True, pattern="film/"),
                    CallbackQueryHandler(self.show_pagination_page, pass_user_data=True, pattern="page/"),
                    CallbackQueryHandler(self.reminder_pagination, pass_user_data=True, pattern="remind/"),
                ]
            },
            fallbacks=[],
        )

        dispatcher.add_handler(control_handler)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    watchingFilms = WatchingFilms()
    # print('main function')
    watchingFilms.main()
