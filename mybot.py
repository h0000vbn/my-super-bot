import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand
from yt_dlp import YoutubeDL

# التوكن مالتك
API_TOKEN = '7772250171:AAGf5EI6zPlkBYp3owZcDfZEq_QPX2Q6YMo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- دالة إضافة القائمة (Menu) السفلية ---
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🚀 بدء تشغيل البوت"),
        BotCommand(command="help", description="❓ تعليمات  التحميل"),
        BotCommand(command="admin", description="👑 المطور (ابو خنياب)")
    ]
    await bot.set_my_commands(commands)

# الأزرار الشفافة الفخمة
def get_vip_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💎 المطور ابو خنياب", url="https://t.me/Alooooonely"))
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👑 أهلاً بك عزيزي في بوت عمك ابو خنياب\n\n"
        f"🌍 يمكنك التحميل من كافة مواقع العالم\n"
        f"(TikTok, Instagram, YouTube, Facebook, X...)\n\n"
        f"🚀 فقط أرسل الرابط وسأقوم برفعه لك هنا فوراً!"
    )
    await message.answer(text=welcome_text, reply_markup=get_vip_keyboard())

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    # هذا الأمر يطلع بس إلك لأنك المطور
    await message.answer("👑 أهلاً بك يا مهندس (ابو خنياب).. لوحة الإدارة قيد التطوير.")

@dp.message()
async def universal_downloader(message: types.Message):
    url = message.text
    if not url or "http" not in url: return

    status_msg = await message.answer("🔍 👷‍♂️ ابو خنياب\n┗ ⚡ يتم تحميل الفيديو لخاطر عيونك...")
    
    # إعدادات الوحش بدون FFmpeg
    ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # يختار أسرع صيغة جاهزة
    'outtmpl': f'khalidy_{message.from_user.id}_%(id)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'nocheckcertificate': True, # يتخطى فحص الأمان لتسريع البداية
}

    filename = None
    try:
        def download_file():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
                return ydl.prepare_filename(info)

        loop = asyncio.get_event_loop()
        filename = await loop.run_in_executor(None, download_file)

        await status_msg.edit_text("📤 عمك ابو خنياب\n┗ 🚀 خلص ماضل شي صبرك علينا...")

        ext = filename.lower().split('.')[-1]
        caption_text = f"✅  أتفضل هاك الفيديو\n👑 المطور : عمك ابو خنياب"

        if ext in ['mp4', 'mkv', 'webm', 'mov']:
            await message.answer_video(video=types.FSInputFile(filename), caption=caption_text, reply_markup=get_vip_keyboard())
        elif ext in ['jpg', 'jpeg', 'png', 'webp']:
            await message.answer_photo(photo=types.FSInputFile(filename), caption=caption_text, reply_markup=get_vip_keyboard())
        else:
            await message.answer_document(document=types.FSInputFile(filename), caption=caption_text, reply_markup=get_vip_keyboard())

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"عذراً مهندس\nالرابط محمي أو به مشكلة، جرب رابط آخر.\n(راح يساعدك عمك ابو حنياب)")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # تفعيل القائمة السفلية أول ما يشتغل البوت
    await set_bot_commands(bot)
    print("🔥 بوت الخالدي شغال هسه والقائمة السفلية تفعلت!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())