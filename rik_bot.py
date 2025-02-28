import os
import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# Получаем ключи из переменных среды (более безопасный способ)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Роль бота
ASSISTANT_ROLE = "Ты — музыкальный бизнесмен Рик. Ты помогаешь артистам с музыкой, маркетингом и вдохновением. Ты строг, но понимающий, умеешь разгонять творческие идеи."

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Настройка бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Функция обработки сообщений
@dp.message_handler()
async def chat_with_gpt(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ASSISTANT_ROLE},
                {"role": "user", "content": message.text},
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        await message.reply(answer)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply("Что-то пошло не так.")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
