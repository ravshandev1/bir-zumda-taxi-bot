from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def towns(res: list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for i in res:
        markup.insert(KeyboardButton(f"{i['name']}"))
    markup.insert(KeyboardButton("⬅️Ortga"))
    return markup


count_person = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("1 kishi"),
            KeyboardButton("2 kishi"),
        ],
        [
            KeyboardButton("3 kishi"),
            KeyboardButton("4 kishi"),
        ]
    ],
    resize_keyboard=True
)

start_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("👮Taksis"),
            KeyboardButton("👨‍💼Yo’lovchi"),
        ],
        [
            KeyboardButton("🧑‍💻Bot admin"),
        ]
    ],
    resize_keyboard=True
)
back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("⬅️Ortga")
        ]
    ],
    resize_keyboard=True
)
attribution = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("✅ Ha"),
            KeyboardButton("❌ Yo'q"),
        ]
    ],
    resize_keyboard=True
)

profile_client = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("📍Qayerga boramiz"),
        ],
        [
            KeyboardButton("👤 Profil"),
            KeyboardButton("📝 Profilni o'zgartirish"),
            KeyboardButton("🗑️ Profileni o'chirish"),
        ],
    ],
    resize_keyboard=True
)
profile_taxi = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("📋 Ma'lumotlarim"),
        ],
        [
            KeyboardButton("🛣️ Yo’nalish qo’shish"),
            KeyboardButton("🛣️ Yo’nalishni o’chirish"),
        ],
        [
            KeyboardButton("👤 Profilni o'zgartirish"),
            KeyboardButton("🗑️ Profileni o'chirish"),
        ]
    ],
    resize_keyboard=True
)

loc = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("📍 Turgan manzilni yuborish", request_location=True)
        ]
    ],
    resize_keyboard=True
)
phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Telefon raqamni yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)

find = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🔴 Topildi")
        ]
    ],
    resize_keyboard=True
)
