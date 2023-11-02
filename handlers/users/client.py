import requests
from aiogram.types import Message, ReplyKeyboardRemove
from loader import dp
from states.register import Client, Profile, Travel
from aiogram.dispatcher import FSMContext
from keyboards.default.register import attribution, start_btn, profile_client, back, loc, find, phone, towns, \
    count_person
from data.config import BASE_URL


@dp.message_handler(text=["🧑‍💻Bot admin"])
async def a(mes: Message):
    await mes.answer("👨‍💼 Admin: Isroilov Rustam\n🇺🇿 Telegram: @abdumalikovichuz")


@dp.message_handler(text=['👨‍💼Yo’lovchi'])
async def client(mes: Message):
    await mes.answer("✍️Ism Familiya:", reply_markup=back)
    await Client.name.set()


@dp.message_handler(state=Client.name)
async def name(mes: Message, state: FSMContext):
    if mes.text == "⬅️Ortga":
        await mes.answer(f"Siz kimsiz 👮Taksist yoki 👨‍💼Yo’lovchi❓", reply_markup=start_btn)
        await state.finish()
    else:
        await state.update_data(
            {'name': mes.text, 'username': f"@{mes.from_user.username}", 'telegram_id': mes.from_user.id}
        )
        await mes.answer("☎️ Telefon Raqamingiz:\nMisol: (941234567)", reply_markup=phone)
        await Client.next()


@dp.message_handler(state=Client.phone, content_types=['contact', 'text'])
async def name(mes: Message, state: FSMContext):
    if mes.contact:
        await state.update_data(
            {'phone': mes.contact.phone_number}
        )
    else:
        await state.update_data(
            {'phone': f"998{mes.text}"}
        )
    data = await state.get_data()
    txt = "📋 Ma'lumotlar:\n"
    txt += f"👨‍💼 Yo’lovchi: <b>{data['name']}</b>\n"
    txt += f"☎️ Telefon Raqamingiz: <b>{data['phone']}</b>\n"
    txt += f"🇺🇿 Telegram:  <b>{data['username']}</b>\n"
    await mes.answer(txt)
    await mes.answer("Ma'lumotlaringizni to'g'rimi ❓", reply_markup=attribution)
    await Client.next()


@dp.message_handler(state=Client.is_true)
async def yes(mes: Message, state: FSMContext):
    if mes.text == "✅ Ha":
        data = await state.get_data()
        r = requests.post(url=f"{BASE_URL}/user/client/?id={mes.from_user.id}", data=data)
        if r.status_code == 200:
            await mes.answer("🎉 Tabriklaymiz Ro’yxatdan o’tdingiz ‼️", reply_markup=profile_client)
        else:
            await mes.answer("Xato")
    elif mes.text == "❌ Yo'q":
        await mes.answer(f"Siz kimsiz 👮Taksist yoki 👨‍💼Yo’lovchi❓", reply_markup=start_btn)
    await state.finish()


@dp.message_handler(text=['👤 Profil'])
async def a(mes: Message):
    r = requests.get(url=f"{BASE_URL}/user/client/?id={mes.from_user.id}")
    data = r.json()
    if data:
        txt = "📋 Ma'lumotlar:\n"
        txt += f"👨‍💼 Yo’lovchi: <b>{data['name']}</b>\n"
        txt += f"☎️ Telefon Raqamingiz: <b>{data['phone']}</b>\n"
        txt += f"🇺🇿 Telegram: <b>{data['username']}</b>\n"
        await mes.answer(txt, reply_markup=profile_client)
    else:
        await mes.answer("Xato")


@dp.message_handler(text="📝 Profilni o'zgartirish")
async def c(ms: Message):
    await ms.answer("Profilni o'zgartiramizmi❓", reply_markup=attribution)
    await Profile.update.set()


@dp.message_handler(state=Profile.update)
async def a(mes: Message, state: FSMContext):
    if mes.text == "❌ Yo'q":
        await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_client)
        await state.finish()
    elif mes.text == "✅ Ha":
        await mes.answer("✍️Ism Familiya:", reply_markup=ReplyKeyboardRemove())
        await Client.name.set()


@dp.message_handler(text="📍Qayerga boramiz")
async def a(mes: Message):
    r = requests.get(url=f"{BASE_URL}/where/")
    data = r.json()
    if data:
        await mes.answer("Qayerdan ketamiz ❓\n", reply_markup=towns(data))
        await Travel.where.set()
    else:
        await mes.answer("Viloyatlar qo'shilmagan! ")


@dp.message_handler(state=Travel.where)
async def a(mes: Message, state: FSMContext):
    if mes.text == "⬅️Ortga":
        await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_client)
        await state.finish()
    else:
        await state.update_data({'where': mes.text})
        r = requests.get(url=f"{BASE_URL}/where/?where={mes.text}")
        data = r.json()
        await mes.answer(f"{mes.text} dan Qayerga ❓", reply_markup=towns(data))
        await Travel.next()


@dp.message_handler(state=Travel.to_where)
async def a(mes: Message, state: FSMContext):
    if mes.text == "⬅️Ortga":
        r = requests.get(url=f"{BASE_URL}/where/")
        data = r.json()
        if data:
            await mes.answer("Qayerdan ❓\n", reply_markup=towns(data))
            await Travel.where.set()
    else:
        await state.update_data({'to_where': mes.text})
        await mes.answer("👥 Yulovchilar sonini kiriting:", reply_markup=count_person)
        await Travel.next()


@dp.message_handler(state=Travel.person)
async def a(mes: Message, state: FSMContext):
    await state.update_data({'count_person': mes.text})
    await mes.answer("⌨️ Qo’shimcha ma’lumot (Misol uchun nechida yo’lga chiqishingizni kiritishingiz mumkin):",
                     reply_markup=ReplyKeyboardRemove())
    await Travel.next()


@dp.message_handler(state=Travel.note)
async def a(mes: Message, state: FSMContext):
    await state.update_data({'note': mes.text})
    await mes.answer("📍 Yo’lga chiqish lokatsiyasini yuboring:\n", reply_markup=loc)
    await Travel.next()


@dp.message_handler(state=Travel.location, content_types='location')
async def a(mes: Message, state: FSMContext):
    await state.update_data(
        {'lon': mes.location['longitude'], 'lat': mes.location['latitude']}
    )
    data = await state.get_data()
    r = requests.get(url=f"{BASE_URL}/user/client/?id={mes.from_user.id}")
    dt = r.json()
    txt = f"👨‍💼 Yo’lovchi: <b>{dt['name']}</b>\n"
    txt += f"☎️ Telefon: <b>{dt['phone']}</b>\n"
    txt += f"🗺️ Yunalish: <b>{data['where']} -> {data['to_where']}</b>\n"
    txt += f"👥 Yo'lovchilar soni: <b>{data['count_person']}</b>\n"
    txt += f"🇺🇿 Telegram: <b>{dt['username']}</b>\n"
    txt += f"⌨️ Qo'shimcha: <b>{data['note']}</b>\n"
    txt += f"📍 Yo’lga chiqish lokatsiyasi: 👇️\n"
    await mes.answer(txt)
    await mes.reply_location(latitude=data['lat'], longitude=data['lon'])
    await mes.answer("Ma'lumotlarni tasdiqlaysizmi❓", reply_markup=attribution)
    await Travel.next()


@dp.message_handler(state=Travel.is_true)
async def a(mes: Message, state: FSMContext):
    if mes.text == "✅ Ha":
        data = await state.get_data()
        r = requests.post(url=f"{BASE_URL}/?telegram_id={mes.from_user.id}", data=data)
        if r.status_code == 201:
            dt = r.json()
            await state.update_data({'id': dt['id']})
            await mes.answer(
                f"📤 Ma'lumotlaringiz <b>{dt['count']}</b> taksisga yuborildi❗️\n⏰ Tez orada aloqaga chiqishadi\n🤝️ Taksi bilan kelishilgandan so'ng\n<b>🔴 Topildi</b> tugmasini bosing",
                reply_markup=find)
            await Travel.next()
    elif mes.text == "❌ Yo'q":
        await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=profile_client)
        await state.finish()


@dp.message_handler(state=Travel.completed)
async def a(mes: Message, state: FSMContext):
    if mes.text == "🔴 Topildi":
        dt = await state.get_data()
        r = requests.patch(url=f"{BASE_URL}/?id={dt['id']}")
        if r.status_code == 200:
            await mes.answer("✊ Qo'llab quvvatlash uchun bizga obuna bo'ling\n📢 @isroilov_rustamjon",
                             reply_markup=profile_client)
        else:
            await mes.answer("Xato")
    await state.finish()
