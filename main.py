import logging
from aiogram import Bot, Dispatcher, executor, types
from db import add_user, subscribe, admin_check, get_subscribed_users, add_app_desc, get_app_status, get_app_name, delete_app
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from checker import parse_2, parse_test
import asyncio


loop = asyncio.get_event_loop()


API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class Sendler_Text(StatesGroup): # States for Text sendler(mailing)
    text = State()
    sureor = State()


@dp.message_handler(commands=['start', 'help']) # start/help commands for users with info
async def send_welcome(message: types.Message):
    user_into_db = add_user(user_id=message.from_user.id)
    await message.reply("Привет! Если ты хочешь получать оповещения о забаненых прилах, дневных капах и лимитах - подпи"
                        "шись на рассылку с помощью команды /follow. Ты в любой момент можешь отменить подписку с "
                        "помощью команды /unfollow")


@dp.message_handler(commands=['follow']) # follow to mailing
async def follow(message: types.Message):
    subscribe(subscription=1, user_id=message.from_user.id)
    await message.reply("Отлично! Теперь мы будем оповещать тебя обо всех важных событиях. ")


@dp.message_handler(commands=['unfollow']) # unfollow from mailing
async def unfollow(message: types.Message):
    subscribe(subscription=0, user_id=message.from_user.id)
    await message.reply("Вы отписались от наших оповещений.")


@dp.message_handler(commands=['oliadm']) # Bot admin interface for permited users only
async def admin_checking_bruh(message: types.Message):
    role = admin_check(user_id=message.from_user.id)
    print(role)
    if role == 'admin':
        await message.reply("Привет. Ты успешно авторизовался. Ниже ты сможешь найти список всех доступных команд для админа:\n"
                            "/sendtoall - запуск рассылки. Пишешь текст и затем подтверждаешь отправку.\n"
                            "/allfollowers - узнать количество подписчиков(в разработке)\n"
                            "/newapp - позволяет добавить новую прилу в базу данных. Будьте внимательны при добавлении ссылки.\n")
    else:
        await message.reply("Вам сюда нельзя!")
        print('Error')


class UrlChecker(StatesGroup): # URL checking states for aiogram.
    URL = State()
    NAME = State()


@dp.message_handler(commands=['newapp']) # Add new application into the DB. Only https/http links.
async def test_f(message: types.Message):
    await message.answer("Вставьте ссылку на приложение.\n Ссылка должна начинаться с http:// или https:// и вести в "
                         "Google Play.")
    await UrlChecker.URL.set()


@dp.message_handler(state=UrlChecker.URL) # Checking app availability, using states for url checker.
async def test_ff(message: types.Message, state: FSMContext):
    await state.update_data(url_name=message.text)
    app_data = await state.get_data()
    print(app_data['url_name'])
    get_app_name = parse_2(url=app_data['url_name'])
    print(get_app_name)
    if 'play.google' in app_data['url_name']:
        adc = add_app_desc(url=app_data['url_name'], name=get_app_name)
        print(adc)
        await message.answer(f"Прила под названием " + get_app_name + ' добавлена в базу')
        await state.finish()
    else:
        await message.answer(f"Введите ссылку в Google Store!")
        await state.finish()


@dp.message_handler(commands=['sendtoall']) # Mailing to all users in DB using states in aiogram.
async def test_f(message: types.Message):
    await message.answer("Напишите текст")
    await Sendler_Text.text.set()


@dp.message_handler(state=Sendler_Text.text) # Next step of mailing states
async def test_ff(message: types.Message, state: FSMContext):
    await state.update_data(food=message.text)
    user_data = await state.get_data()
    await message.answer(f"Ваш текст: {user_data['food']}.\n Вы уверены что хотите отправить сообщение? Да или Нет")
    await Sendler_Text.next()


@dp.message_handler(state=Sendler_Text.sureor) # Users confirmation
async def test_ff(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text == "Да":
        role = admin_check(user_id=message.from_user.id)
        if role == 'admin':
            user_ids = get_subscribed_users()
            for i in user_ids:
                for b in i:
                    await bot.send_message(chat_id=b, text=user_data['food'])
                    await state.finish()
        else:
            await message.answer('У вас недостаточно прав')
            print('Error')
    else:
        await message.answer('Отправка отменена')
        await state.finish()

"""
@dp.message_handler(commands=['cancel']) # 
async def command_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Текст с рассылкой", reply_markup=types.ReplyKeyboardRemove())
"""


async def send_note(bot: Bot): # Auto mailing if app is banned.
    while True:
        await asyncio.sleep(8)
        await parse_test()
        app_status = get_app_status()
        print(app_status)
        if app_status:
            get_name = get_app_name()
            await bot.send_message(chat_id=245070829, text = 'Прила ' + get_name + ' забанена. Просьба, '
                                                                                   'переключить трафик. ')
            delete_app(url=app_status)


async def startup(dp: Dispatcher): # Send note startup
    asyncio.create_task(send_note(dp.bot))

executor.start_polling(dp, on_startup=startup)


if __name__ == '__main__': # Bot startup
    executor.start_polling(dp, skip_updates=True)
