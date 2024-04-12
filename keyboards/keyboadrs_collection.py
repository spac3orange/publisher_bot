from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def start_keyboard() -> ReplyKeyboardMarkup:
    """
        Create and return a reply keyboard with a confirmation button.

        Returns:
            ReplyKeyboardMarkup: A reply keyboard with a button for confirming an action.
    """
    kbi = ReplyKeyboardBuilder()
    kbi.button(text="Начать")
    kbi.adjust(1)
    return kbi.as_markup(resize_keyboard=True, one_time_keyboard=True)


async def yn_keyboard():
    kb_row1 = [
        types.KeyboardButton(text="Да")
    ]

    kb_row2 = [
        types.KeyboardButton(text="Нет")
    ]

    kb = [kb_row1, kb_row2]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


async def sendtext_keyboard():
    kb_row1 = [
        types.KeyboardButton(text="Отправить")
    ]

    kb_row2 = [
        types.KeyboardButton(text="Отменить")
    ]

    kb = [kb_row1, kb_row2]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


async def publish_keyboard(g_id):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Подтвердить', callback_data=f'send{g_id}')
    kb_builder.button(text='Отмена', callback_data=f'cancel{g_id}')

    kb_builder.adjust(1)
    return kb_builder.as_markup(resize_keyboard=True)
