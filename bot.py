import telebot
from telebot import apihelper

from Parser.Parser import Parser

apihelper.proxy = {'https': 'https://75.146.218.153:55768'}
f = open('token.sec')
bot = telebot.TeleBot(f.readline())
f.close()


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    print(str(message.chat.id)+": "+message.text)
    output_str = parser.parse_input(message.text)
    print(output_str)
    bot.send_message(message.chat.id, output_str)


if __name__ == '__main__':
    global parser
    parser = Parser()
    bot.polling(none_stop=True, timeout=500000)
