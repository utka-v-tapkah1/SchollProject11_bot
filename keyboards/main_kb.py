from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU_BUTTON


def create_menu_kb():
    button_breakfast = InlineKeyboardButton(text=LEXICON_RU_BUTTON['breakfast'],
                                            callback_data='breakfast')
    button_obed = InlineKeyboardButton(text=LEXICON_RU_BUTTON['obed'],
                                       callback_data='obed')
    button_site = InlineKeyboardButton(text=LEXICON_RU_BUTTON['official_site'],
                                       callback_data='official_site')

    markup = InlineKeyboardBuilder()
    markup.row(button_breakfast, button_obed)
    markup.row(button_site)

    return markup.as_markup()


def create_back_to_menu_kb():
    button_back_to_menu = InlineKeyboardButton(text=LEXICON_RU_BUTTON['menu'],
                                               callback_data='/start')
    markup = InlineKeyboardBuilder()
    markup.row(button_back_to_menu)

    return markup.as_markup()
