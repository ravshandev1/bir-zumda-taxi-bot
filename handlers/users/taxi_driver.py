import requests
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import dp
from states.register import Taxi, TaxiAtDe, TaxiAtUp, Yunalish
from aiogram.dispatcher import FSMContext
from keyboards.default.register import attribution, start_btn, profile_taxi, back, phone, towns
from data.config import BASE_URL
from keyboards.inline.list import yes_no, no_yes, routes


@dp.message_handler(text=["👮Taksis"])
async def a(mes: Message):
    await mes.answer("✍️Ism Familiya:", reply_markup=back)
    await Taxi.name.set()


@dp.message_handler(state=Taxi.name)
async def a(mes: Message, state: FSMContext):
    if mes.text == "⬅️Ortga":
        await mes.answer(f"Siz kimsiz 👮Taksist yoki 👨‍💼Yo’lovchi❓", reply_markup=start_btn)
        await state.finish()
    else:
        await state.update_data(
            {'name': mes.text, 'username': f"@{mes.from_user.username}", 'telegram_id': mes.from_user.id}
        )
        await mes.answer("☎️ Telefon Raqamingiz:\nMisol: (941234567)", reply_markup=phone)
        await Taxi.next()


@dp.message_handler(state=Taxi.phone, content_types=['contact', 'text'])
async def a(mes: Message, state: FSMContext):
    if mes.contact:
        await state.update_data(
            {'phone': mes.contact.phone_number}
        )
    else:
        await state.update_data(
            {'phone': f"998{mes.text}"}
        )
    data = await state.get_data()
    txt = "📋 Ma'lumotlar\n"
    txt += f"👮 Taxi: <b>{data['name']}</b>\n"
    txt += f"☎️ Telefon Raqamingiz: <b>{data['phone']}</b>\n"
    txt += f"🇺🇿 Telegram:  <b>{data['username']}</b>\n"
    await mes.answer(txt)
    await mes.answer("Ma'lumotlaringizni to'g'rimi?", reply_markup=attribution)
    await Taxi.next()


@dp.message_handler(state=Taxi.is_true)
async def yes(mes: Message, state: FSMContext):
    if mes.text == "✅ Ha":
        data = await state.get_data()
        r = requests.post(url=f"{BASE_URL}/user/taxi/?id={mes.from_user.id}", data=data)
        if r.status_code == 200:
            await mes.answer("🎉 Tabriklaymiz Ro’yxatdan o’tdingiz!")
            r = requests.get(url=f"{BASE_URL}/where/")
            data = r.json()
            if data:
                await mes.answer("🗺️ Yo’nalish qo'shing: 👇️", reply_markup=towns(data))
                await state.finish()
                await Yunalish.where.set()
            else:
                await mes.answer("Viloyatlar qo'shilmagan! ")
                await state.finish()
        else:
            await mes.answer("Xato")
            await state.finish()
    elif mes.text == "❌ Yo'q":
        await mes.answer(f"Siz kimsiz 👮Taksist yoki 👨‍💼Yo’lovchi❓", reply_markup=start_btn)
        await state.finish()


@dp.message_handler(text=["🗑️ Profileni o'chirish", "👤 Profilni o'zgartirish"])
async def a(mes: Message):
    if mes.text == "🗑️ Profileni o'chirish":
        await mes.answer("Rostan o'chirishni hohlaysizmi❓", reply_markup=attribution)
        await TaxiAtDe.st.set()
    else:
        await mes.answer("Profilni o'zgartiramizmi❓", reply_markup=attribution)
        await TaxiAtUp.st.set()


@dp.message_handler(state=TaxiAtDe.st)
async def a(mes: Message, state: FSMContext):
    if mes.text == "❌ Yo'q":
        await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_taxi)
    elif mes.text == "✅ Ha":
        requests.delete(url=f"{BASE_URL}/user/taxi/?id={mes.from_user.id}")
        await mes.answer(f"Siz kimsiz 👮Taksist yoki 👨‍💼Yo’lovchi❓", reply_markup=start_btn)
    await state.finish()


@dp.message_handler(state=TaxiAtUp.st)
async def a(mes: Message, state: FSMContext):
    if mes.text == "❌ Yo'q":
        await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_taxi)
        await state.finish()
    elif mes.text == "✅ Ha":
        await mes.answer("✍️Ism Familiya:", reply_markup=ReplyKeyboardRemove())
        await Taxi.name.set()


@dp.message_handler(text=["📋 Ma'lumotlarim"])
async def a(mes: Message):
    r = requests.get(url=f"{BASE_URL}/user/taxi/?id={mes.from_user.id}")
    data = r.json()
    r = requests.get(url=f"{BASE_URL}/destination/?telegram_id={mes.from_user.id}")
    des = r.json()
    dt = ""
    for (i, j) in zip(range(1, len(des) + 1), des):
        dt += f"  \t{i}. <b>{j['where']} -> {j['to_where']}</b>\n"
    txt = "📋 Ma'lumotlar\n"
    txt += f"👮 Taxi: <b>{data['name']}</b>\n"
    txt += f"📞 Aloqa: <b>{data['phone']}</b>\n"
    txt += f"🇺🇿 Telegram:  <b>{data['username']}</b>\n"
    txt += f"🗺️ Yo’nalish: 👇️\n{dt}"
    await mes.answer(txt)


@dp.message_handler(text="🛣️ Yo’nalish qo’shish")
async def a(mes: Message):
    r = requests.get(url=f"{BASE_URL}/where/")
    data = r.json()
    if data:
        await mes.answer("Qayerdan ❓", reply_markup=towns(data))
        await Yunalish.where.set()
    else:
        await mes.answer("🗺️Barcha yo'nalishlarni band qildingiz!")


@dp.message_handler(state=Yunalish.where)
async def a(mes: Message, state: FSMContext):
    if mes.text == "⬅️Ortga":
        await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_taxi)
        await state.finish()
    else:
        await state.update_data({'where': mes.text})
        r = requests.get(url=f"{BASE_URL}/where/?where={mes.text}")
        data = r.json()
        await mes.answer(f"{mes.text} dan Qayerga ❓", reply_markup=towns(data))
        await Yunalish.next()


@dp.message_handler(state=Yunalish.to_where)
async def a(mes: Message, state: FSMContext):
    if mes.text == "⬅️Ortga":
        r = requests.get(url=f"{BASE_URL}/where/")
        data = r.json()
        await mes.answer("Qayerdan ❓", reply_markup=towns(data))
        await Yunalish.where.set()
    else:
        data = await state.get_data()
        data['to_where'] = mes.text
        data['telegram_id'] = mes.from_user.id
        r = requests.post(url=f"{BASE_URL}/destination/", data=data)
        if r.status_code == 302:
            await mes.answer("Bunday yo'nalish sizda mavjud!", reply_markup=profile_taxi)
        elif r.status_code == 201:
            await mes.answer(f"🛣️ {data['where']} -> {mes.text} qo'shildi\nYana yo'nalish qo'shishni xoxlaysizmi ❓",
                             reply_markup=yes_no)
        await state.finish()


@dp.message_handler(text="🛣️ Yo’nalishni o’chirish")
async def a(mes: Message):
    r = requests.get(url=f"{BASE_URL}/destination/?telegram_id={mes.from_user.id}")
    des = r.json()
    if des:
        txt = ""
        for (i, j) in zip(range(1, len(des) + 1), des):
            txt += f"  \t{i}. <b>{j['where']} -> {j['to_where']}</b>\n"
        await mes.answer("Qaysi yo’nalishingizni o’chrasiz ❓\n" + txt, reply_markup=routes(des))
    else:
        await mes.answer("Yo'nalishlaringiz mavjud emas❗")


@dp.callback_query_handler(text_startswith='delete_id:')
async def a(call: CallbackQuery):
    await call.message.delete()
    w_id = call.data.split('delete_id:')[1]
    r = requests.delete(url=f"{BASE_URL}/destination/?id={w_id}")
    if r.status_code == 204:
        await call.message.answer("✅ Muvaffaqiyatli o’chirildi.\nYana yo’nalish o’chirasizmi ❓",
                                  reply_markup=no_yes)
    else:
        await call.message.answer("Xato")
    await call.answer(cache_time=1)


@dp.callback_query_handler(text=['yes', 'no'])
async def a(call: CallbackQuery):
    if call.data == 'yes':
        await call.message.delete()
        r = requests.get(url=f"{BASE_URL}/where/")
        data = r.json()
        await call.message.answer("Qayerdan ❓", reply_markup=towns(data))
        await Yunalish.where.set()
    else:
        await call.message.delete()
        await call.message.answer("Ma'lumotlar saqlandi ⬇️", reply_markup=profile_taxi)


@dp.callback_query_handler(text=['yuq', 'ha'])
async def a(call: CallbackQuery):
    if call.data == 'ha':
        await call.message.delete()
        r = requests.get(url=f"{BASE_URL}/destination/?telegram_id={call.from_user.id}")
        des = r.json()
        if des:
            txt = ""
            for (i, j) in zip(range(1, len(des) + 1), des):
                txt += f"  \t{i}. <b>{j['where']} -> {j['to_where']}</b>\n"
            await call.message.answer("Qaysi yo’nalishingizni o’chrasiz ❓\n" + txt, reply_markup=routes(des))
        else:
            await call.message.answer("Yo'nalishlaringiz mavjud emas❗")
    else:
        await call.message.delete()
        await call.message.answer("Ma'lumotlar saqlandi ⬇️", reply_markup=profile_taxi)
