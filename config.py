import telebot
from obtener_noticias import *

TELEGRAM_TOKEN = '6965899907:AAEXwFsBL7l5WRwzpNSlsxyQwg2qYnysO-M'

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "¡Hola!, ¿En que puedo ayudarte?")

@bot.message_handler(commands=['salud'])
def show_news(message):
	news = scrap_page("salud")
	bot.reply_to(message, "Noticias de hoy en salud:")
	for i in range(len(news)):
		bot.reply_to(message, news[i])

@bot.message_handler(commands=['tecnologia'])
def show_news(message):
	news = scrap_page("tecno")
	bot.reply_to(message, "Noticias de hoy en tecnologia:")
	for i in range(len(news)):
		bot.reply_to(message, news[i])

@bot.message_handler(commands=['politica'])
def show_news(message):
	news = scrap_page("politica")
	bot.reply_to(message, "Noticias de hoy en politica:")
	for i in range(len(news)):
		bot.reply_to(message, news[i])

@bot.message_handler(commands=['economia'])
def show_news(message):
	news = scrap_page("economia")
	bot.reply_to(message, "Noticias de hoy en economia:")
	for i in range(len(news)):
		bot.reply_to(message, news[i])

if __name__=='__main__':
	print('Bot is running...')
	bot.polling()
	print('Bot is stopped')