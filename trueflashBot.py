from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
from aiogram.types import ParseMode

bot = Bot(token="2052426131:AAHd7dx8ytigpOlMTK0yjEdcKWOZXE7vxf8")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(_):
    print('Online')


class Form(StatesGroup):
    FIO = State()
    Age = State()
    City = State()
    PhoneNumber = State()
    Email = State()
    Education = State()
    AdobePhotoshop = State()
    Experience = State()
    Portfolio = State()
    WorkDay = State()
    Salary = State()
    Source = State()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await message.delete()
        await bot.send_message(message.from_user.id, "Привет, чтобы пройти опрос введите команду /opros")
    except:
        await message.reply('Напишите боту в ЛС https://t.me/trueflashBot')


# Начинаем наш диалог
@dp.message_handler(commands='opros')
async def cmd_start(message: types.Message):
    await Form.FIO.set()
    await message.reply("Привет! Как тебя зовут?")


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Сюда приходит ответ с FIO
@dp.message_handler(state=Form.FIO)
async def process_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['FIO'] = message.text

    await Form.next()
    await message.reply("Сколько тебе лет?")


# Проверяем возраст
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.Age)
async def process_age_invalid(message: types.Message):
    return await message.reply("Напиши возраст или напиши /cancel")


# Принимаем возраст и узнаем город проживания
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.Age)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(Age=int(message.text))

    await message.reply("В каком часовом поясе вы живете?")


# Проверяем часовой пояс
@dp.message_handler(lambda message: not message.text.lstrip("-").isdigit(), state=Form.City)
async def process_city_invalid1(message: types.Message):
    return await message.reply("Напиши свой часовой пояс, например (4) или напиши /cancel")


# Проверяем часовой пояс
@dp.message_handler(
    lambda message: message.text.lstrip("-").isdigit() and (int(message.text) < -12 or int(message.text) > 12),
    state=Form.City)
async def process_city_invalid2(message: types.Message):
    return await message.reply("Напиши свой часовой пояс, от -12 до 12 или напиши /cancel")


# Принимаем часовой пояс и узнаем номер телефона
@dp.message_handler(
    lambda message: message.text.lstrip("-").isdigit() and (int(message.text) >= -12) and (int(message.text) <= 12),
    state=Form.City)
async def process_city(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(City=message.text)

    await message.reply("Укажите свой номер телефона, например +79002613100")


# Принимаем номер телефона и узнаем почту
@dp.message_handler(state=Form.PhoneNumber)
async def process_phonenumber(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(PhoneNumber=message.text)

    await message.reply("Укажите свою электронную почту")


# Принимаем почту и узнаем образование
@dp.message_handler(state=Form.Email)
async def process_email(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(Email=message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("полное высшее", "среднее")
    await message.reply("Укажите наличие образования", reply_markup=markup)


# Проверяем образование
@dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=Form.Education)
async def process_education_invalid(message: types.Message):
    return await message.reply("Укажите образование кнопкой или напиши /cancel")


# Принимаем образование и узнаем знание фотошопа
@dp.message_handler(state=Form.Education)
async def process_education(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(Education=message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Да", "Нет")
    await message.reply("Умеете ли вы работать в Adobe Illustrator и Photoshop?", reply_markup=markup)


# Проверяем фотошоп
@dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=Form.AdobePhotoshop)
async def process_adobephotoshop_invalid(message: types.Message):
    return await message.reply("Укажите умение работы в фотошопе кнопкой или напиши /cancel")


# Принимаем фотошоп и узнаем стаж работы
@dp.message_handler(state=Form.AdobePhotoshop)
async def process_adobephotoshop(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(AdobePhotoshop=message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("меньше 3 лет", "больше 3 лет")
    await message.reply("Укажите свой стаж работы графическим дизайнером", reply_markup=markup)


# Проверяем стаж работы
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.Experience)
async def process_experience_invalid(message: types.Message):
    return await message.reply("Укажите стаж работы графическим дизайнером или напиши /cancel")


# Принимаем стаж работы и узнаем портфолио
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.Experience)
async def process_experience(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(Experience=message.text)

    await message.reply("Укажите сылку на портфолио")


# Принимаем портфолио и спрашиваем про полную занятость
@dp.message_handler(state=Form.Portfolio)
async def process_portfolio(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(Portfolio=message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Да", "Нет")
    await message.reply("Готовы ли вы к работе на полную занятость в нашей компании? 5-8ч/день", reply_markup=markup)


# Проверяем полную занятость
@dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=Form.WorkDay)
async def process_workday_invalid(message: types.Message):
    return await message.reply("Укажите полную занятость кнопкой на клавиатуре или напиши /cancel")


# Принимаем полную занятость и узнаем зарплату
@dp.message_handler(state=Form.WorkDay)
async def process_workday(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(WorkDay=message.text)
    markup = types.ReplyKeyboardRemove()
    await message.reply("Укажите желаемую зарплату", reply_markup=markup)


# Проверяем зарплату
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.Salary)
async def process_salary_invalid(message: types.Message):
    return await message.reply("Укажите зарплату или напиши /cancel")


# Принимаем зарплату и узнаем источник о вакансии
@dp.message_handler(state=Form.Salary)
async def process_salary(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(Salary=int(message.text))

    await message.reply("Расскажите, откуда вы узнали про вакансию")


# Принимаем вакансию и выводим анкету
@dp.message_handler(state=Form.Source)
async def process_source(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Source'] = message.text
        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.from_user.id,
            md.text(
                md.text('Спасибо, результаты опроса будут рассмотрены. Мы вам позвоним(нет)'),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    await state.finish()

@dp.message_handler()
async def echo_send(message : types.Message):
    if message.text=='Слава Украине':
        await message.reply('Героям слава')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)