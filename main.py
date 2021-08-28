import logging

import Start
import ShowAll
import ShowOne
import Buttons
import SecretInfo
import Settings
import Threads

from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALL, ONE, SETTINGS_PAGINATION, SETTINGS_TIME, SETTINGS_DAY_BEFORE_NOTIFICATION = range(5)


class WatchingFilms:
    def __init__(self):
        self.__url_get_all_films = 'https://films-assembly.pp.ua/api/films'
        self.__url_get_one_film = 'https://films-assembly.pp.ua/api/film/'
        self.__films_in_one_pagination = 2
        self.__buttons = Buttons.Buttons()
        self.__settings = Settings.Settings(self.__buttons)
        self.__start = Start.Start()
        self.__show_all = None
        self.__show_one = ShowOne.ShowOne(self.__url_get_one_film)
        self.__check_time = '12:00'
        self.__day_notification = None
        self.__thread = None

    def start(self, update, context):
        self.__start.start(update, context)
        return SETTINGS_PAGINATION

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
                                        update,
                                        context,
                                        self.__films_in_one_pagination,
                                        self.__url_get_all_films)
        self.__thread.start_thread()
        return ALL

    def reminder_pagination(self, update, context):
        self.__thread.show_pagination_page(update, context)
        return ALL

    def show_all(self, update, context):
        self.__show_all.show_all(update, context)
        return

    def show_pagination_page(self, update, context):
        self.__show_all.show_pagination_page(update, context)
        return ALL

    def show_one_film(self, update, context):
        self.__show_one.show_one_film(update, context)
        return ALL

    def main(self):
        updater = Updater(SecretInfo.TELEGRAM_HTTP_API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        control_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start),],
            states={
                SETTINGS_PAGINATION: [
                    MessageHandler(Filters.regex(r"^(?:[1-9]\d*(?:\.\d+)?|0\.0*[1-9]\d*)$"), self.setting_pagination,)
                ],
                SETTINGS_DAY_BEFORE_NOTIFICATION:[
                    MessageHandler(Filters.regex(r"^(?:[1-9]\d*(?:\.\d+)?|0\.0*[1-9]\d*)$"), self.settings_day_notification, )
                ],
                SETTINGS_TIME:[
                    MessageHandler(Filters.regex(r"^(0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9]$"), self.setting_time,)
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
    watchingFilms.main()