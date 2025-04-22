import requests
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from datetime import datetime

API_TOKEN = "7691732315:AAEjdF14vzqgowS5I4cht-DtCeYv65z2wXA"
ADMIN_ID = 5793264698  # Замените на реальный Telegram ID администратора

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)

# Список одобренных пользователей
approved_users = set()
pending_users = {}

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    if user_id in approved_users:
        await message.answer("Привет! Напишите мне что-то, и я сохраню ваше сообщение.")
    else:
        pending_users[user_id] = message.from_user
        await bot.send_message(ADMIN_ID, f"👤 Новый пользователь хочет войти:\n"
                                         f"ID: {user_id}\n"
                                         f"Имя: {message.from_user.first_name}\n"
                                         f"Фамилия: {message.from_user.last_name or 'Не указано'}\n"
                                         f"Username: @{message.from_user.username or 'Не указан'}\n\n"
                                         f"✅ Для одобрения напишите: **да**\n"
                                         f"❌ Для отказа напишите: **нет**")
        await message.answer("⏳ Ваша заявка отправлена администратору. Ждите подтверждения.")

@router.message()
async def handle_admin_response(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        command = message.text.lower()
        if command == "да" or command == "нет":
            for user_id, user in list(pending_users.items()):
                if command == "да":
                    approved_users.add(user_id)
                    del pending_users[user_id]
                    await bot.send_message(user_id, "✅ Администратор одобрил ваш доступ! Теперь вы можете пользоваться ботом.")
                    await message.answer(f"✅ Пользователь {user_id} одобрен.")
                elif command == "нет":
                    del pending_users[user_id]
                    await bot.send_message(user_id, "❌ Вам отказано в доступе.")
                    await message.answer(f"❌ Пользователь {user_id} отклонен.")
                return

    user_id = message.from_user.id
    if user_id not in approved_users:
        await message.answer("⛔ Вы не можете пользоваться ботом, пока администратор не одобрит вас.")
        return

    # Сохранение сообщения
    payload = {
        'user_id': user_id,
        'username': message.from_user.username or "Не указан",
        'first_name': message.from_user.first_name or "Не указано",
        'last_name': message.from_user.last_name or "Не указано",
        'text': message.text,
        'timestamp': datetime.now().isoformat()
    }
    response = requests.post('http://127.0.0.1:8000/botmessages/', json=payload)

    if response.status_code == 201:
        await message.answer("✅ Ваше сообщение сохранено в базе.")
    else:
        await message.answer("❌ Ошибка при сохранении сообщения.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
