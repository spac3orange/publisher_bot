from aiogram import Router, types, F
from keyboards.keyboadrs_collection import publish_keyboard
from aiogram.fsm.context import FSMContext
from states.my_states import GetDataState
from aiogram.exceptions import TelegramForbiddenError
from loader import bot
from templates.admins import ADMINS, CHANNEL
import json
import os


router = Router()


async def send_admin(user_data):
    key = await publish_keyboard(user_data['id'])
    message_text = f"id пользователя: {user_data['id']}\nответ пользователя: {user_data['answer']}\nтекст:\n\n {user_data['text']}"
    try:
        await bot.send_message(ADMINS[0], message_text, reply_markup=key)
    except TelegramForbiddenError:
        pass


async def find_and_remove_entry_by_id(file_path, entry_id):
    if not os.path.exists(file_path):
        print("Файл не найден.")
        return None

    lines_to_keep = []
    text_value = None
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                # Проверяем, совпадает ли id в текущей строке с искомым
                if str(data.get("id")) == str(entry_id):
                    text_value = data.get("text")
                else:
                    lines_to_keep.append(line)
            except json.JSONDecodeError:
                continue  # Пропускаем строки с ошибками

    # Перезаписываем файл без удалённой строки
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines_to_keep)

    return text_value


@router.callback_query(lambda c: c.data.startswith('send') or c.data.startswith('cancel'))
async def callback_handler(query: types.CallbackQuery):
    file_path = 'data.txt'
    data = query.data
    if data.startswith('send'):
        g_id = data[len('send'):]
        text_value = await find_and_remove_entry_by_id(file_path, g_id)
        if text_value is not None:
            await publish(text_value, g_id)
        else:
            await bot.send_message(ADMINS[0], 'Запись не найдена или файл не существует.')

    elif data.startswith('cancel'):
        g_id = data[len('cancel'):]
        text_value = await find_and_remove_entry_by_id(file_path, g_id)
        try:
            await bot.send_message(g_id, 'Ваше сообщение было отклонено модератором.\nИзмените сообщение и попробуйте еще раз!')
        except TelegramForbiddenError:
            pass
    await query.message.edit_reply_markup(reply_markup=None)


async def publish(text_value, g_id):
    try:
        await bot.send_message(CHANNEL[0], text_value)
    except TelegramForbiddenError:
        pass
    try:
        await bot.send_message(g_id, 'Спасибо! Ваше сообщение опубликовано в канале!')
    except TelegramForbiddenError:
        pass




