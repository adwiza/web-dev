import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, callback_query
from aiogram.utils import executor
from aiogram.utils.exceptions import TelegramAPIError, MessageNotModified

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=('start', 'help'))
async def command_start(message: types.Message):
    text = 'Hello'
    if message.text.startswith('/help'):
        text += ' help'
    text += '!'
    await message.reply(text)


@dp.message_handler(commands='key')
async def send_markup(message: types.Message):
    kb = ReplyKeyboardMarkup()
    # yes = KeyboardButton('YES')
    # no = KeyboardButton('NO')
    kb.add(*(KeyboardButton(text) for text in ('YES', 'NO')))
    ask_phone = KeyboardButton('Send phone number', request_contact=True)
    kb.add(ask_phone)
    ask_location = KeyboardButton('Send location', request_location=True)
    kb.add(ask_location)
    remove = KeyboardButton('remove')
    remove_cmd = KeyboardButton('/remove')
    kb.add(remove)
    kb.add(remove_cmd)
    await message.reply('Kb is here:', reply_markup=kb)


# @dp.message_handler(commands=['start', 'help'])
# async def command_help(message: types.Message):
#     await message.reply('Hello help!')

@dp.message_handler(commands='btn')
async def send_inline_keyboard(message: types.Message):
    kb = InlineKeyboardMarkup()
    yes = InlineKeyboardButton('YES', callback_data='yes')
    no = InlineKeyboardButton('NO', callback_data='no')
    kb.add(yes, no)
    # kb.add(*(InlineKeyboardButton(text) for text in ('YES', 'NO')))
    await message.reply('Buttons here:', reply_markup=kb)


@dp.callback_query_handler(text='yes')
async def handle_callback_query_yes(callback_query: types.CallbackQuery):
    await callback_query.answer('Cool!')


@dp.callback_query_handler(text='no')
async def handle_callback_query_no(callback_query: types.CallbackQuery):
    await callback_query.answer('Why not?', show_alert=True)


@dp.callback_query_handler()
async def handle_all_callback_queries(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id)
    await callback_query.answer()


@dp.message_handler(text='remove')
@dp.message_handler(commands='remove')
async def remove_markup(message: types.Message):
    await message.reply('Removed...', reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(message.chat.id, 'Removed...', reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def echo_message(message: types.Message):
    # bot = Bot.get_current()
    # await bot.send_message(message.chat.id, message.text)
    await message.reply(message.text)


@dp.message_handler(content_types=ContentType.STICKER)
async def echo_sticker(message: types.Message):
    # await bot.send_sticker(message.chat.id, message.sticker.file_id)
    await message.reply_sticker(message.sticker.file_id, reply=False)


@dp.errors_handler(exception=MessageNotModified)
async def handler_error_message_not_modified(update: types.Update, e):
    pass


@dp.errors_handler(exception=TelegramAPIError)
async def handle_telegram_api_error():
    pass


if __name__ == "__main__":
    executor.start_polling(dp)
