import requests
from telegram import ParseMode


class ShowOne:
    def __init__(self, __url_get_one_film):
        self.__url_get_one_film = __url_get_one_film

    def show_one_film(self, update, context):
        film_id = update.callback_query.data.split('/')[1]

        try:
            response = requests.get(
                url=self.__url_get_one_film + film_id,
            ).json()
        except Exception as exe:
            context.bot.send_message(
                update.effective_chat.id,
                text="Фильма уже нету",
                parse_mode=ParseMode.HTML
            )
            return

        html_text = ''
        if len(response['title']) > 0:
            html_text = f"<strong>{response['title']}</strong>\n\n"
        if len(response['datetime']) > 0:
            html_text += f"Дата выхода:  {response['datetime']} \n\n"
        if len(response['poster']) > 0:
            html_text += f"{response['poster']} \n\n"
        if len(response['description']) > 0:
            html_text += f"{response['description']} \n\n"

        message = context.bot.send_message(
            update.effective_chat.id,
            text=html_text,
            parse_mode=ParseMode.HTML
        )
        if len(response['url']) > 0:
            html_text = f"{response['url']} \n"
            message = context.bot.send_message(
                update.effective_chat.id,
                text=html_text,
                parse_mode=ParseMode.HTML
            )