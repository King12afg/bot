from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import requests

# توکن ربات
TOKEN = '7579063722:AAFghS2ckIYPzoW4nQYV39br_kZVM5nTP-0'

# تابع شروع و پیام خوش‌آمدگویی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! من یک ربات تلگرام هستم. دستورات قابل استفاده: /help, /about")

# تابع راهنما
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "/start - شروع\n/help - راهنما\n/about - درباره ما\n/weather - وضعیت آب‌وهوا"
    await update.message.reply_text(help_text)

# تابع درباره ما
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("این ربات با Python ساخته شده است!")

# تابع برای نمایش وضعیت آب‌وهوا
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("لطفاً نام شهر را وارد کنید:")

# تابعی برای دریافت و نمایش وضعیت آب‌وهوا
async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = update.message.text
    # کلید API را از سایت‌های آب و هوا بگیرید (برای مثال OpenWeatherMap)
    api_key = '926a9d6b78890ff4fa6465d375fa397f'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url).json()
    
    if response.get("cod") != "404":
        main = response["main"]
        temperature = main["temp"]
        weather_description = response["weather"][0]["description"]
        weather_info = f"شهر: {city}\nدمای فعلی: {temperature}°C\nوضعیت: {weather_description}"
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("متاسفانه شهر مورد نظر یافت نشد.")

# تابع اصلی برای تنظیمات ربات
def main():
    application = Application.builder().token(TOKEN).build()

    # هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("weather", weather))
    
    # هندلر برای دریافت نام شهر از کاربر و نمایش وضعیت آب و هوا
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()