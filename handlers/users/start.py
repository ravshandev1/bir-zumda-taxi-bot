from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.register import start_btn, profile_client, profile_taxi
from loader import dp
import requests
from data.config import BASE_URL
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    requests.post(url=f"{BASE_URL}/users/", data={'telegram_id': message.from_user.id})
    await state.finish()
    r = requests.get(url=f"{BASE_URL}/user/{message.from_user.id}/")
    if r.status_code == 201:
        await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_client)
    elif r.status_code == 202:
        await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_taxi)
    elif r.status_code == 404:
        await message.answer(f"🙋 Assalomu alaykum ‼️\nSiz kimsiz 👮Taksist yoki 👨‍💼Yo’lovchi❓", reply_markup=start_btn)
