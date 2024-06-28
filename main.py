import telebot
from telebot import types
import requests

bot = telebot.TeleBot('7264301837:AAG85q-_oX7_iSZa3ovIvHpEjlP5-BAFaK8')

# Словари для отслеживания предпочтений языка пользователя и контактной информации
user_language = {}
user_contacts = {}


@bot.message_handler(commands=['start'])  # стартовая команда
def start(message):
    user_id = message.from_user.id
    if user_id not in user_contacts:
        # Предложить пользователю выбрать язык
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🇷🇺 Русский")
        btn2 = types.KeyboardButton('🇬🇧 English')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)
    else:
        # Показать главное меню на основе предпочтений пользователя
        send_main_menu_by_language(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id

    # Русский язык
    if message.text == '🇷🇺 Русский':
        user_language[user_id] = 'ru'
        if user_id not in user_contacts:
            request_contact(message)
        else:
            send_main_menu(message)

    elif message.text == '🔙 Вернуться к выбору языка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🇷🇺 Русский")
        btn2 = types.KeyboardButton('🇬🇧 English')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)

    elif message.text == '📰 Новости':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn1)
        bot.send_message(message.from_user.id,
                         'Здесь будут все новости о ваших курсах',
                         reply_markup=markup, parse_mode='Markdown')

    elif message.text == '📜 Правила сайта':
        bot.send_message(message.from_user.id,
                         'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)',
                         parse_mode='Markdown')

    elif message.text == '🔙 Главное меню':
        send_main_menu(message)

    # Английский язык
    elif message.text == '🇬🇧 English':
        user_language[user_id] = 'en'
        if user_id not in user_contacts:
            request_contact(message)
        else:
            send_main_menu_en(message)

    elif message.text == '🔙 Back to language selection':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🇷🇺 Русский")
        btn2 = types.KeyboardButton('🇬🇧 English')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)

    elif message.text == '📰 News':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🔙 Main menu')
        markup.add(btn1)
        bot.send_message(message.from_user.id,
                         'All the news about your courses will be here',
                         reply_markup=markup, parse_mode='Markdown')

    elif message.text == '📜 Site Rules':
        bot.send_message(message.from_user.id,
                         'You can read the site rules by following the ' + '[link](https://habr.com/en/docs/help/rules/)',
                         parse_mode='Markdown')

    elif message.text == '🔙 Main menu':
        send_main_menu_en(message)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    user_id = message.from_user.id
    contact = message.contact
    send_contact_to_site(contact.phone_number)
    bot.send_message(message.chat.id, f"Спасибо за предоставление вашей контактной информации, {contact.first_name}!")

    # Отметить пользователя как предоставившего контакт
    user_contacts[user_id] = contact.phone_number

    # Проверить предпочтение языка пользователя и вернуться в главное меню
    send_main_menu_by_language(message)


def request_contact(message):
    user_id = message.from_user.id
    if user_language.get(user_id) == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("📱 Поделиться контактом", request_contact=True)
        markup.add(btn1)
        bot.send_message(message.chat.id, "Пожалуйста, поделитесь вашим номером телефона:", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("📱 Share Contact", request_contact=True)
        markup.add(btn1)
        bot.send_message(message.chat.id, "Please share your contact number:", reply_markup=markup)


def send_contact_to_site(phone_number):
    url = 'https://coursegram.ru/api/endpoint'  # Замените на ваш фактический конечный пункт
    data = {'phone_number': phone_number}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Возбудить HTTPError для плохих ответов
        print(f"Успешно отправлены данные на {url}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке данных на {url}: {e}")


def send_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📰 Новости")
    btn2 = types.KeyboardButton('📜 Правила сайта')
    btn3 = types.KeyboardButton('🔙 Вернуться к выбору языка')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "👀 Выберите интересующий вас раздел", reply_markup=markup)


def send_main_menu_en(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📰 News")
    btn2 = types.KeyboardButton('📜 Site Rules')
    btn3 = types.KeyboardButton('🔙 Back to language selection')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, '👀 Select the section you are interested in', reply_markup=markup)


def send_main_menu_by_language(message):
    user_id = message.from_user.id
    if user_language.get(user_id) == 'ru':
        send_main_menu(message)
    else:
        send_main_menu_en(message)


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
