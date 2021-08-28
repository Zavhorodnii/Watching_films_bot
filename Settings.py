
class Settings:

    def __init__(self, __buttons):
        self.__buttons = __buttons

    def settings_pagination(self, update, context):
        pagination = update.message.text

        context.bot.send_message(
            update.effective_chat.id,
            text=f"Ты справился с этим заданием! \n\n"
                 "За сколько дней до выхода фильма присылать уведомление?",
        )

        return int(pagination)

    def settings_day_notification(self, update, context):
        day_notification = update.message.text

        context.bot.send_message(
            update.effective_chat.id,
            text=f"Отлично! \n\n"
                 "А теперь давай введем время в которое необходимо проверять наличие скорых фильмов\n\n"
                 "Введи вряме в формате ЧЧ:ММ",
        )

        return int(day_notification)

    def settings_time(self, update, context):
        time = update.message.text

        context.bot.send_message(
            update.effective_chat.id,
            text="Вот и все!"
        )
        context.bot.send_message(
            update.effective_chat.id,
            text="Значит ты надеешься выйти в киношку? \n\n"
                 "Ну если аниме уже не устраивает.... \n\n"
                 "Жми кнопку расположенную ниже и узри список почти шедевров!",
            reply_markup=self.__buttons.start_button()
        )

        return time