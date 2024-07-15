import telebot
from config import *
from logic import *
bot = telebot.TeleBot(TOKEN)
user_marker_colors = {}
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды: \n/start - приветствие\n/help - помощь\n/city - отображение города/городов\n/remember_city - добавление существующего города в свои любимые\n/show_my_cities - отображение ваших любимых городов\n/color - выбор цвета маркера\n/water - показ городов с океанами")
@bot.message_handler(commands=['color'])
def handle_set_marker_color(message):
    color = message.text.split()[1]
    user_marker_colors[message.chat.id] = color
    bot.send_message(message.chat.id, f'Цвет маркера установлен на {color}')
@bot.message_handler(commands=['city'])
def handle_show_city(message):
    city_names = message.text.split()[1:]
    color = user_marker_colors.get(message.chat.id, 'blue')  # По умолчанию синий цвет
    manager.create_grap('image/world.png', city_names, color)
    with open('image/world.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
@bot.message_handler(commands=['water'])
def handle_show_city(message):
    city_names = message.text.split()[1:]
    color = user_marker_colors.get(message.chat.id, 'blue')  # По умолчанию синий цвет
    manager.create_grapf('image/world.png', city_names, color)
    with open('image/world.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')
@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    color = user_marker_colors.get(message.chat.id, 'blue')  # По умолчанию синий цвет
    manager.create_grapf('image/world.png', cities, color)
    with open('image/world.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
@bot.message_handler(commands=['show_city_by_country'])
def handle_show_city_by_country(message):
    country_name = message.text.split()[1]
    cities = manager.get_cities_by_country(country_name)
    color = user_marker_colors.get(message.chat.id, 'blue')  # По умолчанию синий цвет
    manager.create_grapf('image/world.png', cities, color)
    with open('image/world.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['show_city_by_density'])
def handle_show_city_by_density(message):
    min_density, max_density = map(int, message.text.split()[1:])
    cities = manager.get_cities_by_density(min_density, max_density)
    color = user_marker_colors.get(message.chat.id, 'blue')  # По умолчанию синий цвет
    manager.create_grapf('image/world.png', cities, color)
    with open('image/world.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['show_city_by_density_and_country'])
def handle_show_city_by_density_and_country(message):
    country_name = message.text.split()[1]
    min_density, max_density = map(int, message.text.split()[2:])
    cities = manager.get_cities_by_density_and_country(country_name, min_density, max_density)
    color = user_marker_colors.get(message.chat.id, 'blue')  # По умолчанию синий цвет
    manager.create_grapf('image/world.png', cities, color)
    with open('image/world.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
if __name__ == "__main__":
    manager = DB_Map(DATABASE)
    bot.polling()