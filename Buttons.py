from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


class Buttons:

    def start_button(self):
        __reply_keyboard = [
            ['Узреть список почти шедевров', ],
        ]
        return ReplyKeyboardMarkup(__reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

    def pagination_films(self, count_pages):
        page = []
        for index in range(count_pages):
            page.append(InlineKeyboardButton(f"{index+1}", callback_data=f"page/{index+1}"),)
        __reply_keyboard = [
            page,
        ]
        return InlineKeyboardMarkup(__reply_keyboard)

    def pagination_remind(self, count_pages):
        page = []
        for index in range(count_pages):
            page.append(InlineKeyboardButton(f"{index+1}", callback_data=f"remind/{index+1}"),)
        __reply_keyboard = [
            page,
        ]
        return InlineKeyboardMarkup(__reply_keyboard)

    def film_detail(self, id, title):
        # print(f"title = {title}")
        keyboard = [[
            InlineKeyboardButton(title, callback_data=f"film/{id}"),
        ], ]
        return InlineKeyboardMarkup(keyboard)