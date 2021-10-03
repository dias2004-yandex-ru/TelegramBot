# полноценный бот рафинированный
# имя бота MikeSFbot
# username Mike_SkillFactBot
import telebot
from MyBotConfig import TOKEN, currency
from MyBotExtensions import APIException, Converter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_help(message: telebot.types.Message):
    text = 'Наберите команду в формате:\n<из какой валюты> <в какую валюту перевести> <количество>, например:' \
           '\nЕвро рубль 0.64\nВ ответ на такой запрос придёт стоимость 64-х евроцентов в рублях по текущему курсу.' \
           '\nСписок доступных валют выводится командой /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def send_values(message: telebot.types.Message):
    t = 'Названия доступных валют:'
    for key in currency.keys():
        t = '\n'.join((t, key, ))
    bot.reply_to(message, t)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')
        if len(val) != 3:
            raise APIException('Недопустимое количество параметров.')
        else:
            base, quote, amount = val
            answer = Converter.convert(base, quote, amount)
    except APIException as err:
        bot.reply_to(message, f'Ошибка ввода:\n{err}')
    except Exception as err:
        bot.reply_to(message, f'Не удалось обработать команду\n{err}')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()
