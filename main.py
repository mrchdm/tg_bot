import telebot, wikipedia, re
from telebot import types
import Create_notebook
import csv

token = "5737846883:AAHpkd55saWsQhLzc7lRZuM_qotVS64hss8"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    Create_notebook.create_list()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вступить в клуб печенек")
    item2 = types.KeyboardButton("Найти информацию")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Привет! Я бот-всезнайка. Ты можешь узнать что-то новенькое и вступить в клуб печенек!', reply_markup=markup)

@bot.message_handler(content_types=['text'])

def root(message):
    if message.text == "Вступить в клуб печенек":
        bot.register_next_step_handler(message, register_me)
    elif message.text == "Найти информацию":
        msg = bot.send_message(message.chat.id, 'Введите слово для поиска информации')
        bot.register_next_step_handler(msg, handle_text)

def register_me(message):
    msg = bot.send_message(message.chat.id, 'Введите Имя')
    bot.register_next_step_handler(msg, enter_fio)

def enter_fio(message):
    new_user = []
    new_user.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите Фамилию')
    bot.register_next_step_handler(msg, enter_surname, new_user)

def enter_surname(message, new_user):
    new_user.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(msg, enter_tel, new_user)

def enter_tel(message, new_user):
    new_user.append(message.text)
    bot.send_message(message.chat.id, 'Вы успешно приняты!')

    with open('notebook.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(new_user)

wikipedia.set_lang("ru")

def get_wiki(request):
    try:
        page = str(wikipedia.page(request))
        page = page.content[:1000]
        page = list(page.split('.'))
        page =  page[:-1]

        wiki_output = ''
        for string in page:
            if not ('==' in string):
                wiki_output = wiki_output + string + '.'
        re.sub('\([^()]*\)', '', wiki_output)
        return wiki_output
    except Exception as e:
        return 'Ничего не найдено'

def handle_text(message):
    bot.send_message(message.chat.id, get_wiki(message.text))



bot.infinity_polling()