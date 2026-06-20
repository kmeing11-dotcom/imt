import telebot
import random
from telebot import types  # <-- Импорт для кнопок

# ========== 1. ВСТАВЬ СЮДА СВОЙ ТОКЕН ==========
TOKEN = "8784834347:AAE3ZRdEUp0Nd8uiGhyDClCOEaCZSDyjsvE"
# ==============================================

# ========== 2. СОЗДАЕМ БОТА (теперь переменная bot существует) ==========
bot = telebot.TeleBot(TOKEN)

# ========== 3. ТВОИ СПИСКИ И ДАННЫЕ ==========
quotes = [
    "Ты уже пожал 100 кг в 14 лет. Код — это легче.",
    "Не бойся ошибок. Бойся скуки.",
    "Свобода начинается там, где заканчивается страх.",
    "Делай сегодня то, что другие не хотят, и завтра будешь жить так, как другие не могут."
]

# ========== 4. ВСЕ ОБРАБОТЧИКИ (пишем их ПОСЛЕ создания bot) ==========

# Обработчик команды /start (с кнопками)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📝 Цитата')
    btn2 = types.KeyboardButton('💪 Мой ИМТ')
    btn3 = types.KeyboardButton('🐶 Собака')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Выбирай кнопку:", reply_markup=markup)

# Обработчик команды /quote (старый, но мы его оставим для надежности)
@bot.message_handler(commands=['quote'])
def quote_message(message):
    quote = random.choice(quotes)
    bot.send_message(message.chat.id, quote)

# Обработчик команды /imt (старый)
@bot.message_handler(commands=['imt'])
def imt_command(message):
    bot.send_message(message.chat.id, "Напиши свой вес и рост через пробел. Например: 70 1.75")
    bot.register_next_step_handler(message, calculate_imt)

# Функция расчета ИМТ (она отдельно)
def calculate_imt(message):
    try:
        weight, height = map(float, message.text.split())
        imt = weight / (height * height)
        if imt < 18.5:
            status = "недостаток веса"
        elif 18.5 <= imt < 25:
            status = "норма"
        elif 25 <= imt < 30:
            status = "избыток"
        else:
            status = "ожирение"
        bot.send_message(message.chat.id, f"Твой ИМТ: {round(imt, 1)} — это {status}.")
    except:
        bot.send_message(message.chat.id, "Ошибка! Пиши так: вес пробел рост (например, 70 1.75)")

@bot.message_handler(commands=['dog'])
def dog_message(message):
    try:
        # Пробуем отправить картинку с первого сайта
        bot.send_photo(message.chat.id, 'https://random.dog/woof.jpg')
    except:
        # Если не получилось — шлем запасную милую картинку-заглушку
        bot.send_photo(message.chat.id, 'https://i.imgur.com/8VYwz9S.jpeg')

# УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК КНОПОК И ТЕКСТА (должен быть САМЫМ ПОСЛЕДНИМ!)
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == '📝 Цитата':
        quote_message(message)
    elif message.text == '💪 Мой ИМТ':
        imt_command(message)
    elif message.text == '🐶 Собака':
        dog_message(message)
    # Если просто написать какой-то текст (не команду и не кнопку), бот просто повторит его
    else:
        bot.reply_to(message, f"Ты написал: {message.text}")

# ========== 5. ЗАПУСК (вечный цикл) ==========
while True:
    try:
        print("Бот запущен. Жду команды...")
        bot.polling(none_stop=True, timeout=60, interval=0)
    except Exception as e:
        print(f"Ошибка: {e}. Переподключение через 15 секунд...")
        time.sleep(15)