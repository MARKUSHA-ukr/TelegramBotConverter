
import telebot 
from currency_converter import CurrencyConverter
from telebot import types

info = 0
bot = telebot.TeleBot("7268113633:AAGeIfUm7uvxKCaQ9EV-Pw8hdD-BhKNk5UE")
cur = CurrencyConverter()

user_data = {}

@bot.message_handler(commands=["start"])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Введи суму:")
    bot.register_next_step_handler(message ,summa)

def summa(message):

    global info
    try:
        info = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id,"Введи число!!")
        bot.register_next_step_handler(message,summa)
        return #щоб решта коду не виповнялось
    if info > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)#В рядку максимум 2 кнопки
        btn1 = types.InlineKeyboardButton("USD/EUR",callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("USD/CNY", callback_data="usd/cny")
        btn3 = types.InlineKeyboardButton("GBP/USD", callback_data="gbp/usd")
        btn4 = types.InlineKeyboardButton("USD/JPY", callback_data="usd/jpy")
        btn5 = types.InlineKeyboardButton("Інше", callback_data="else")
        markup.add(btn1,btn2,btn3,btn4,btn5)
        bot.send_message(message.chat.id, " Виберіть валютну пару:" ,reply_markup=markup)
    else:
        bot.send_message(message.chat.id,"БІЛЬШЕ НУЛЯ,Тварь")
        bot.register_next_step_handler(message,summa)

@bot.callback_query_handler(func=lambda call: True)
def calback(call):
    if call.data != "else":
        values = call.data.upper().split("/")#upper - приводить у верхній регістр callback_data,a split("/") - розділяє на /
        res = cur.convert(info, values[0],values[1])
        bot.send_message(call.message.chat.id, f"Получаєтся {round(res,2)},Можете повторити")
        bot.register_next_step_handler(call.message,summa)
    else:
        bot.send_message(call.message.chat.id, "Введіть валютну пару через '/' :")
        bot.register_next_step_handler(call.message,currency)

def currency(message):
    try:
        values = message.text.upper().split("/")  # бере текст, який написав юзер у Telegram 
        res = cur.convert(info, values[0], values[1])
        bot.send_message(message.chat.id, f"Получаєтся {round(res, 2)}, Можете повторити")
        bot.register_next_step_handler(message, summa)
        
    except ValueError:
        bot.send_message(message.chat.id, "ПОГАНИЙ ФОРМАТ! Ще раз введи валютну пару")
        bot.register_next_step_handler(message, currency)
        


if __name__ == "__main__":
    bot.infinity_polling()



