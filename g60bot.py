import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
import os

# Load environment variables
load_dotenv()

# Get API keys from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def get_gemini_response(query):
    try:
        genai.configure(api_key="AIzaSyDhqdOpzU2PMadKHQfOctzqi-NU9FrpsTU")
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        print(f"Gemini Response: {response.text}")
        return {"response": response.text}
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return {"error": f"Failed to get a response from Gemini: {e}"}

async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Initialize bot and dispatcher
    bot = Bot("7976222070:AAHgljEOPQDU0KCydKtEkqCoY5XeBT-xwHA")
    dp = Dispatcher()

    @dp.message(Command(commands=["start"]))
    async def start_command(message: Message):
        await message.answer("Hello! Srishti(G60) here. Ask me anything!")

    @dp.message()
    async def handle_message(message: Message):
        user_query = message.text
        ai_response = get_gemini_response(user_query)

        if "error" in ai_response:
            await message.answer("Sorry, I couldn't get a response. Please try another question.")
        else:
            await message.answer(ai_response["response"])

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())