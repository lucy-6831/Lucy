import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import os

API_TOKEN = "8338932561:AAGJl-sstHFrqsWcjJu1l9NgnD7LT_SWEq4"
CHANNEL_ID = -1003438739880  # آیدی کانال برای فوروارد شماره
VERIFIED_FILE = "verified_numbers.txt"  # فایل ذخیره شماره‌های احراز شده
ADMINS = [5922608780]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# دکمه‌ی احراز هویت
contact_button = KeyboardButton(text="احراز هویت شماره", request_contact=True)
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[contact_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# دکمه‌های بعد از احراز هویت
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="پریمیوم 🦋"), KeyboardButton(text="استارز ⭐")],
        [KeyboardButton(text="گیفت"), KeyboardButton(text="گیفت NFT")],
        [KeyboardButton(text="V2ray")]
    ],
    resize_keyboard=True
)

# پیام‌های دکمه‌ها (مرتب و فاصله‌دار)
messages = {
    "پریمیوم 🦋": """فعال سازی پرمیوم گیفتی بدون ورود به اکانت و فقط با یک آیدی 🦋

پرمیوم سه ماهه ⭐️
قیمت: 13.5 تتر 💵

پرمیوم شیش ماهه ⭐️
قیمت تمام شده: 17.5 تتر 💵

پرمیوم یک ساله 🌟
قیمت: 31 تتر 💵

به صورت ارزی با ارز Ton هم میتونید خریداری کنید.
قیمت هر تتر: https://nobitex.ir/price/usdt/

جهت خرید: @lucyim""",

    "استارز ⭐": """⚜ لیست قیمت استارز تلگرام ⚜

⭐ 13 استارز ⏪ 30,000 تومان
⭐ 21 استارز ⏪ 52,000 تومان
⭐ 50 استارز ⏪ 100,000 تومان
⭐ 100 استارز ⏪ 198,000 تومان
⭐ 200 استارز ⏪ 380,000 تومان
⭐ 250 استارز ⏪ 580,000 تومان
⭐ 350 استارز ⏪ 650,000 تومان
⭐ 500 استارز ⏪ 950,000 تومان
⭐ 750 استارز ⏪ 1,280,000 تومان
⭐ 1000 استارز ⏪ 1,950,000 تومان

‼️ بین پلن های بالا میتونید خورده هم سفارش بدید.
تمامی سفارشات بدون ورود به اکانت فقط با آیدی انجام میشه❗️

جهت خرید: @lucyim""",

    "گیفت": """🧸 (۱۵ استار) 30,000 تومان
💝 (۱۵ استار) 30,000 تومان
🌹 (۲۵ استار) 47,000 تومان
🎁 (۲۵ استار) 47,000 تومان
💐 (۵۰ استار) 94,000 تومان
🎂 (۵۰ استار) 94,000 تومان
🚀 (۵۰ استار) 94,000 تومان
💎 (۱۰۰ استار) 188,000 تومان
💍 (۱۰۰ استار) 188,000 تومان
🏆 (۱۰۰ استار) 188,000 تومان

جهت خرید: @lucyim""",

    "گیفت NFT": """برای خرید گیفت NFT به آیدی زیر پیام بدید:
@lucyim""",

    "V2ray": "موجود نیست"
}

# مدیریت کاربران
def load_verified_numbers():
    if not os.path.exists(VERIFIED_FILE):
        return set()
    with open(VERIFIED_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_verified_number(number):
    with open(VERIFIED_FILE, "a") as f:
        f.write(number + "\n")

verified_numbers = load_verified_numbers()

# گرفتن عکس پروفایل
async def get_profile_photo(user_id: int):
    photos = await bot.get_user_profile_photos(user_id=user_id, limit=1)
    if photos.total_count > 0:
        return photos.photos[0][0].file_id
    return None

# handler /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    phone_verified = user_id in verified_numbers

    if phone_verified:
        await message.answer(
            "شماره شما قبلا احراز شده ✅\nلطفا گزینه مورد نظر را انتخاب کنید:",
            reply_markup=menu_keyboard
        )
    else:
        await message.answer(
            "خوش آمدید 🦋\nجهت استفاده از ربات احراز هویت را کامل کنید",
            reply_markup=start_keyboard
        )

# handler اصلی (احراز هویت و دکمه‌ها)
@dp.message()
async def main_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # احراز هویت
    if message.contact:
        phone = message.contact.phone_number
        if phone in verified_numbers:
            await message.answer(
                "شماره شما قبلا احراز شده ✅",
                reply_markup=menu_keyboard
            )
            return

        verified_numbers.add(phone)
        save_verified_number(phone)

        user = message.from_user
        text_msg = (
            f"📌 اطلاعات احراز هویت جدید:\n\n"
            f"👤 اسم: {user.full_name}\n"
            f"🔗 آیدی: @{user.username if user.username else 'ندارد'}\n"
            f"🆔 ID: {user.id}\n"
            f"📱 شماره: {phone}"
        )

        photo_id = await get_profile_photo(user.id)
        if photo_id:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_id, caption=text_msg)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=text_msg)

        await message.answer(
            "احراز هویت با موفقیت انجام شد! ✅\nلطفا گزینه مورد نظر را انتخاب کنید:",
            reply_markup=menu_keyboard
        )
        return

    # دکمه‌های معمولی
    if text in messages:
        await message.answer(messages[text])

# اجرای بات
async def main():
    print("✅ ربات لوفی در حال اجراست...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
