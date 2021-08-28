import Buttons

class Start:
    # def __init__(self, buttons):
    #     self.__buttons = buttons

    def start(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text="Ну здрасте\n\n"
                 "Так как это наше первое знакомство, давай проведем некоторые настройки",
            # reply_markup=self.__buttons.start_button()
        )
        context.bot.send_message(
            update.effective_chat.id,
            text="Начнем с пагинации\n\n"
                 "Введи число, которое будет является количеством фильмов на одной странице",
            # reply_markup=self.__buttons.start_button()
        )