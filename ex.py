import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6119488567:AAHKnMH8xRuS1NkSpZeq95KKeS-ZWLCJGNU')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands = ['start', 's'])
def start (message):
    bot.send_message(message.chat.id, 'Hey, please write the amount:')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
      amount = int(message.text.strip())
    except ValueError:
      bot.send_message(message.chat.id, 'Please, write the correct format')
      bot.register_next_step_handler(message, summa)
      return

    if amount > 0:
      markup = types.InlineKeyboardMarkup(row_width = 2)
      btn1 = types.InlineKeyboardButton('USD/EUR', callback_data = 'usd/eur')
      btn2 = types.InlineKeyboardButton('EUR/USD', callback_data = 'eur/usd')
      btn3 = types.InlineKeyboardButton('PLN/USD', callback_data = 'pln/usd')
      btn4 = types.InlineKeyboardButton('USD/PLN', callback_data = 'usd/pln')
      btn5 = types.InlineKeyboardButton('UZS/USD', callback_data = 'uzs/usd')
      btn6 = types.InlineKeyboardButton('USD/UZS', callback_data = 'usd/uzs')
      btn7 = types.InlineKeyboardButton('Another currencies', callback_data = 'another currencies')
      markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
      bot.send_message(message.chat.id, 'Choose the currency', reply_markup = markup)
    else:
      bot.send_message(message.chat.id, 'The amount should be higher than 0.\n\nPlease, write the correct format')
      bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    try:
        if call.data != 'another currencies':
          values = call.data.upper().split('/')
          res = currency.convert(amount, values[0], values[1])
          bot.send_message(call.message.chat.id, f'Result:  {round(res, 2)}\n\nYou can write another amount:')
          bot.register_next_step_handler(call.message, summa)
        else:
          bot.send_message(call.message.chat.id, 'Write the desirable currency:')
          bot.register_next_step_handler(call.message, my_currency)
    except ValueError:
        bot.send_message(call.message.chat.id, 'UZS is not a supported currency \n\nPlease, write the another currency')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
      values = message.text.upper().split('/')
      res = currency.convert(amount, values[0], values[1])
      bot.send_message(message.chat.id, f'Result:  {round(res, 2)}\n\nYou can write another amount:')
      bot.register_next_step_handler(message, summa)
    except Exception:
      bot.send_message(message.chat.id, 'Something is wrong. \n\nPlease, write the correct currency')
      bot.register_next_step_handler(message, my_currency)


bot.polling(non_stop = True)