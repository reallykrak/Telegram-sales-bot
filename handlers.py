from aiogram import Dispatcher, types

async def button_handler(call: types.CallbackQuery):
    await call.message.answer("denem1234 baba")

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(button_handler, text="clicked")
