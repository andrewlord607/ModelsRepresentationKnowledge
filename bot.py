import telebot
from telebot import apihelper

from Parser.Parser import Parser

apihelper.proxy = {'https': 'https://75.146.218.153:55768'}


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    print(str(message.chat.id)+": "+message.text)
    bot.send_message(message.chat.id, parser.parse_input(message.text))


if __name__ == '__main__':
    f = open('token.sec')
    global bot
    bot = telebot.TeleBot(f.readline())
    f.close()
    global parser
    parser = Parser()
    bot.polling(none_stop=True, timeout=500000)
