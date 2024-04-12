from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.keyboadrs_collection import start_keyboard, yn_keyboard, sendtext_keyboard, publish_keyboard
from aiogram.fsm.context import FSMContext
from loader import bot
from .admin_funcs import send_admin
from templates.admins import ADMINS
from filters.chat_types import ChatTypeFilter
from states.my_states import GetDataState
import json
import os

router = Router()


@router.message(ChatTypeFilter(chat_type=["private"]), Command('start'))
async def start_command(message: types.Message):
    """
        Handle the /start command in private chat.

        Args:
            message (types.Message): The incoming message.

        Returns:
            None
    """
    print('started')
    user_id = message.from_user.id
    print(user_id)
    if user_id != ADMINS:
        key = await start_keyboard()
        await message.answer('Приветствую тебя в своем пространстве 👋.\nЗдесь ты можешь оставить свой вопрос:\n⬇️⬇️⬇️',
                             reply_markup=key)


@router.message(ChatTypeFilter(chat_type=["private"]), (F.text == 'Начать'))
async def send_confirm(message: types.Message, state: FSMContext):
    key = await yn_keyboard()
    await message.answer('Были ли попытки как-то решить данный вопрос самостоятельно или с другим специалистом?',
                         reply_markup=key)
    await state.set_state(GetDataState.answer_input)


@router.message(GetDataState.answer_input, lambda message: message.text in ['Да', 'Нет'])
async def yn_catch(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(id=user_id)
    await state.update_data(answer=message.text)
    user_data = await state.get_data()
    print(user_data)
    await message.answer('Пожалуйста, ввведите сообщение:')
    await state.set_state(GetDataState.text_input)


@router.message(GetDataState.text_input, F.text)
async def text_catch(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    user_data = await state.get_data()
    text_value = user_data['text']
    key = await sendtext_keyboard()
    await message.answer('<b>Пожалуйста, проверьте сообщение:</b>', parse_mode='HTML')
    await message.answer(text_value, reply_markup=key)
    await state.set_state(GetDataState.confirmation_input)


@router.message(GetDataState.confirmation_input, lambda message: message.text in ['Отправить', 'Отменить'])
async def confirmation_catch(message: types.Message, state: FSMContext):
    if message.text == "Отправить":
        user_data = await state.get_data()
        user_id = user_data['id']
        # Проверяем, существует ли файл и содержит ли он уже данные с таким же ID
        id_exists = False
        if os.path.exists('data.txt'):
            with open('data.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        existing_data = json.loads(line)
                        if str(existing_data.get("id")) == str(user_id):
                            id_exists = True
                            break
                    except json.JSONDecodeError:
                        continue  # В случае ошибки чтения пропускаем строку

        # Записываем данные, только если запись с таким ID не найдена
        if not id_exists:
            with open('data.txt', 'a', encoding='utf-8') as f:
                json_data = json.dumps(user_data, ensure_ascii=False)
                f.write(json_data + "\n")
            await send_admin(user_data)
            await message.answer('Спасибо, сообщение отправлено на модерацию!')
            await state.clear()
        else:
            await message.answer('Запись с таким ID уже существует. Ожидайте обработки сообщения админом.')
            await state.clear()
    else:
        await message.answer('Отправка сообщения отменена')
        await state.clear()


@router.message(ChatTypeFilter(chat_type=["private"]), F.text)
async def unknown(message: types.Message):
    """
    Handle unknown commands.

    Responds to unknown commands with a message.

    Args:
        message (types.Message): The incoming message object.

    Returns:
        None
    """
    await message.answer(text="Я не знаю такой команды.")
