"""
Автоматизация: Заявки из Telegram-бота → Google Sheets
Демонстрационный проект для портфолио.
Зависимости: pip install aiogram gspread oauth2client
"""
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ЗАМЕНИТЕ НА ВАШИ ДАННЫЕ
BOT_TOKEN = "YOUR_TOKEN_HERE"
GOOGLE_CREDENTIALS = "credentials.json"  # Файл ключей от Google Cloud
SHEET_NAME = "Заявки"  # Название вашей Google-таблицы

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ── Настройка Google Sheets ──
# Для работы нужен файл credentials.json, скачанный из Google Cloud Console
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    
    # Создаём заголовки, если таблица пустая
    if not sheet.get_all_values():
        sheet.append_row(["Дата", "Имя", "Телефон", "Сообщение", "TG Username"])
except Exception as e:
    print(f"⚠️ Ошибка подключения к Google Sheets: {e}. Убедитесь, что файл credentials.json существует.")
    sheet = None

# ── Машина состояний для опроса ──
class OrderForm(StatesGroup):
    name = State()
    phone = State()
    message = State()

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("📩 Добро пожаловать! Оставьте заявку.\n\nКак вас зовут?")
    await msg.bot.set_state(msg.from_user.id, OrderForm.name)

@dp.message(OrderForm.name)
async def get_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("📱 Ваш номер телефона?")
    await state.set_state(OrderForm.phone)

@dp.message(OrderForm.phone)
async def get_phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await msg.answer("📝 Опишите ваш запрос или вопрос:")
    await state.set_state(OrderForm.message)

@dp.message(OrderForm.message)
async def get_message(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    username = f"@{msg.from_user.username}" if msg.from_user.username else "—"

    # Запись в Google Sheets
    if sheet:
        sheet.append_row([now, data["name"], data["phone"], msg.text, username])
        await msg.answer("✅ Спасибо! Ваша заявка сохранена в нашей системе. Мы свяжемся с вами в течение часа.")
    else:
        await msg.answer("⚠️ Заявка принята, но возникла ошибка с таблицей (см. логи).")

    await state.clear()

async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
