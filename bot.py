from aiogram import Bot, Dispatcher, executor, types
import config
import keyboards
import handlers

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Merhaba! Butona bas ve mesajı al!", reply_markup=keyboards.menu)

handlers.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp)
