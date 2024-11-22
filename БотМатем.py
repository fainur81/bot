import telebot
import random
API_TOKEN = '7759433752:AAHSnCPqWW9j5kY4Fd59X4cdXFO-Cqtb5Ks'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)
user_games = {}
questions = [
    {"question": "Сколько будет 5 + 3?", "answer": 8},
    {"question": "Сколько будет 10 - 4?", "answer": 6},
    {"question": "Сколько будет 6 * 7?", "answer": 42},
    {"question": "Сколько будет 20 / 4?", "answer": 5},
    {"question": "Сколько будет 9 + 10?", "answer": 19},
    # Добавьте больше вопросов по желанию
]
@bot.message_handler(commands=['start'])
def start_game(message):
    bot.send_message(message.chat.id, "Привет! Давай сыграем в веселую математическую игру! Напиши /math, чтобы начать!")
@bot.message_handler(commands=['math'])
def math_game(message):
    score = 0
    total_questions = 5  # Количество вопросов
    user_games[message.chat.id] = {"score": score, "total": total_questions, "current_question": 0}
    send_question(message.chat.id)
def send_question(chat_id):
    if user_games[chat_id]["current_question"] < user_games[chat_id]["total"]:
        question_data = random.choice(questions)
        question = question_data["question"]
        user_games[chat_id]["current_answer"] = question_data["answer"]
        bot.send_message(chat_id, question)
    else:
        score = user_games[chat_id]["score"]
        bot.send_message(chat_id, f"Игра окончена! Ты набрал {score} из {user_games[chat_id]['total']} баллов.")
        del user_games[chat_id]  # Удаляем игру для пользователя
@bot.message_handler(func=lambda message: message.chat.id in user_games)
def check_math_answer(message):
    try:
        user_answer = int(message.text)
        correct_answer = user_games[message.chat.id]["current_answer"]
        if user_answer == correct_answer:
            user_games[message.chat.id]["score"] += 1
            bot.send_message(message.chat.id, "Поздравляю! Ты правильно ответил! 🎉")
        else:
            bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {correct_answer}")
        
        # Переходим к следующему вопросу
        user_games[message.chat.id]["current_question"] += 1
        send_question(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введи корректный ответ.")
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Я могу помочь тебе сыграть в математическую игру! Напиши /start, чтобы начать.")
# Запуск бота
bot.polling(none_stop=True)
