import telebot
from obtener_noticias import *
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from obtener_noticias import *
import threading
import time
import logging
import re

TELEGRAM_TOKEN = '6965899907:AAEXwFsBL7l5WRwzpNSlsxyQwg2qYnysO-M'

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

salud = InlineKeyboardButton(text="❤️‍🩹 Salud", callback_data="salud")
tecnologia = InlineKeyboardButton(text="💻 Tecnologia", callback_data="tecno")
deportes = InlineKeyboardButton(text="🏃🏻 Deportes", callback_data="deportes")
economia = InlineKeyboardButton(text="💸 Economia", callback_data="economia")
salud2 = InlineKeyboardButton(text="❤️‍🩹 Salud", callback_data="resume_salud")
tecnologia2 = InlineKeyboardButton(text="💻 Tecnologia", callback_data="resume_tecno")
deportes2 = InlineKeyboardButton(text="🏃🏻 Deportes", callback_data="resume_deportes")
economia2 = InlineKeyboardButton(text="💸 Economia", callback_data="resume_economia")

keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[[salud, tecnologia], [deportes, economia]])
keyboard_inline2 = InlineKeyboardMarkup(inline_keyboard=[[salud2, tecnologia2], [deportes2, economia2]])

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_message = (
        "¡Bienvenido RobotTimes el Bot de Noticias definitivo! 📰\n"
        "Estoy aquí para ayudarte a mantenerte informado con las últimas noticias.\n\n"
        "Puedes usar los siguientes comandos:\n"
        "/noticias - Obtén noticias de diferentes categorías.\n"
        "/hoy - Descubre los resúmenes diarios de noticias.\n"
        "/resume - Envía el enlace de una noticia y te proporcionaré un resumen.\n"
        "/dolar - Obtén la cotización del dólar al día de hoy.\n\n"
        "¡Explora las noticias y mantente al tanto de lo que sucede en el mundo!"
    )
    await message.reply(welcome_message)

@dp.message_handler(commands=['dolar'])
async def show_dolar_price(message: types.Message):
    dolar_bn, dolar_libre = obtener_precio_dolar()
    
    response_message = (
        "Precio del Dólar:\n"
        f"🏛️ Banco Nación: {dolar_bn}\n"
        f"💵 Dólar Libre: {dolar_libre}"
    )
    
    await message.reply(response_message)


@dp.message_handler(commands=['resume'])
async def resume_new(message: types.Message):
    message_text = message.text
    url_pattern = r'https?://\S+'
    url_match = re.search(url_pattern, message_text)
    if url_match:
        url = url_match.group()
        response = requests.get(url)
        await message.reply('Resumiendo...')
        title_text, texto = scrap_new(response)
        if url in today_news['url'].values:
            resume_new = today_news[today_news['url'] == url]['resumen'].values
        else:
            resume_new = generate_summaries([texto])
        await message.reply(title_text)
        await message.reply(resume_new[0])
    else:
        await message.reply('No se encontró ninguna URL en el mensaje.')

@dp.message_handler(commands=['noticias'])
async def show_news(message: types.Message):
    await message.reply("¿De qué categoría quieres ver las noticias?", reply_markup=keyboard_inline)

@dp.message_handler(commands=['hoy'])
async def show_resume(message: types.Message):
    await message.reply("¿Que te gustaría saber?", reply_markup=keyboard_inline2)

@dp.callback_query_handler(lambda c: c.data in {'salud', 'tecno', 'deportes', 'economia', 'resume_salud', 'resume_tecno', 'resume_deportes', 'resume_economia'})
async def news_callback_handler(call: types.CallbackQuery):
	
    if call.data == 'salud':
        news = scrap_page("salud")
        await call.message.reply("Top 5 noticias de salud:")
        for i in range(5):
            time.sleep(1)
            await call.message.reply(news[i])

    elif call.data == 'tecno':
        news = scrap_page("tecno")
        await call.message.reply("Top 5 noticias de tecnología:")
        for i in range(5):
            time.sleep(1)
            await call.message.reply(news[i])

    elif call.data == 'deportes':
        news = scrap_page("deportes")
        await call.message.reply("Top 5 noticias de deportes:")
        for i in range(5):
            time.sleep(1)
            await call.message.reply(news[i])

    elif call.data == 'economia':
        news = scrap_page("economia")
        await call.message.reply("Top 5 noticias de economía:")
        for i in range(5):
            time.sleep(1)
            await call.message.reply(news[i])
    
    elif call.data == 'resume_salud':
        category_messages = [f"<b>Hoy en Salud:</b>\n"]
        category = 'salud'
        category_news = today_news[today_news['categoria'] == category]
        for index, row in category_news.iterrows():
            # Agrega la URL al final del resumen con el texto "Enlace a la nota"
            message = f"<b>{row['titulo']}</b>\n{row['resumen']} - <a href='{row['url']}'>Enlace a la nota</a>"
            category_messages.append(message)
        message_text = '\n\n'.join(category_messages)
        await call.message.reply(message_text, parse_mode='HTML')

    elif call.data == 'resume_tecno':
        category_messages = [f"<b>Hoy en Tecnología:</b>\n"]
        category = 'tecno'
        category_news = today_news[today_news['categoria'] == category]
        for index, row in category_news.iterrows():
            # Agrega la URL al final del resumen con el texto "Enlace a la nota"
            message = f"<b>{row['titulo']}</b>\n{row['resumen']} - <a href='{row['url']}'>Enlace a la nota</a>"
            category_messages.append(message)
        message_text = '\n\n'.join(category_messages)
        await call.message.reply(message_text, parse_mode='HTML')

    elif call.data == 'resume_deportes':
        category_messages = [f"<b>Hoy en Deportes:</b>\n"]
        category = 'deportes'
        category_news = today_news[today_news['categoria'] == category]
        for index, row in category_news.iterrows():
            # Agrega la URL al final del resumen con el texto "Enlace a la nota"
            message = f"<b>{row['titulo']}</b>\n{row['resumen']} - <a href='{row['url']}'>Enlace a la nota</a>"
            category_messages.append(message)
        message_text = '\n\n'.join(category_messages)
        await call.message.reply(message_text, parse_mode='HTML')

    elif call.data == 'resume_economia':
        category_messages = [f"<b>Hoy en Economía:</b>\n"]
        category = 'economia'
        category_news = today_news[today_news['categoria'] == category]
        for index, row in category_news.iterrows():
            # Agrega la URL al final del resumen con el texto "Enlace a la nota"
            message = f"<b>{row['titulo']}</b>\n{row['resumen']} - <a href='{row['url']}'>Enlace a la nota</a>"
            category_messages.append(message)
        message_text = '\n\n'.join(category_messages)
        await call.message.reply(message_text, parse_mode='HTML')

    await call.answer()

# Configurar el registro (log)
logging.basicConfig(level=logging.INFO)

def load_data():
    global today_news
    logging.info('Iniciando carga de datos...')
    try:
        today_news = load_csv()  # Carga el DataFrame en today_news global
        logging.info('Carga de datos exitosa. Registros cargados: %d', len(today_news))
    except Exception as e:
        logging.error('Error al cargar datos: %s', str(e))

data_loading_thread = threading.Thread(target=load_data)
data_loading_thread.start()
    

if __name__ == '__main__':
    print('Bot is running...')
    executor.start_polling(dp, skip_updates=True)
    print('Bot is stopped')