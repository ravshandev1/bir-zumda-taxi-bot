from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yes_no = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton("✅ Ha", callback_data='yes'),
        InlineKeyboardButton("❌ Yo'q", callback_data='no'),
    ]
])

no_yes = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton("✅ Ha", callback_data='ha'),
        InlineKeyboardButton("❌ Yo'q", callback_data='yuq'),
    ]
])


def routes(res: dict):
    keyboard = list()
    cnt = 0
    row = list()
    for (i, obj) in zip(range(1, len(res) + 1), res):
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"delete_id:{obj['id']}"))
        cnt += 1
        if cnt == 4:
            keyboard.append(row)
            row = list()
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
