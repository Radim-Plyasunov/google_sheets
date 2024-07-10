import telebot
from datetime import *
from telebot import types
from schedule import Schedule

class TelegramBot:
    def __init__(self, telegram_token, schedule: Schedule):
        self.schedule = schedule
        self.bot = telebot.TeleBot(telegram_token)
        self.init_commands()

    def start(self):
        self.bot.infinity_polling();
    
    def init_commands(self):
        self.start_command = self.bot.message_handler(commands=['start'])(self.start_command)
        self.on_button_click = self.bot.callback_query_handler(func = lambda message: True)(self.on_button_click)

    # по команде /start формируем список предметов за сегодняшнюю дату
    def start_command(self, message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.username
        user_full_name = self.schedule.find_user(user_id, user_name)

        # если пользователь не найден, прекращаем работу
        if user_full_name is None:
            self.bot.reply_to(message, f'Мы вас не узнали, обратитесь к администратору бота.') 
            return
        
        self.bot.reply_to(message, f'Приветствую, {user_full_name}!')
        weekday = datetime.today().weekday()
        subjects = self.schedule.get_subjects(weekday)
        keyboard = types.InlineKeyboardMarkup()
        for subject in subjects:
            button = types.InlineKeyboardButton(subject, callback_data = f"{user_full_name}:{subject}")
            keyboard.add(button)
        self.bot.send_message(message.chat.id, text=f"Выберите предмет", reply_markup=keyboard)

    def on_button_click(self, call):
        # если первый символ ~, то значит мы обрабатываем кнопки посещений
        if call.data[0] == '~':
            self.bot.send_message(call.message.chat.id, text="Одну минуту...")
            success = self.mark(call.data)
            if success:
                self.bot.send_message(call.message.chat.id, text="Данные успешно обновлены")
            else:
                self.bot.send_message(call.message.chat.id, text="Извините, произошла какая-то ошибка. Обратитесь к администратору бота.")
            return
        else:
            user_and_subject = call.data

        plus_button = types.InlineKeyboardButton("Был", callback_data=f"~:+:{user_and_subject}")
        minus_button = types.InlineKeyboardButton("Не был", callback_data=f"~:-:{user_and_subject}")
        sick_button = types.InlineKeyboardButton("Болел", callback_data=f"~:Б:{user_and_subject}")
        clear_button = types.InlineKeyboardButton("Очистить", callback_data=f"~::{user_and_subject}")

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(plus_button, minus_button, sick_button, clear_button)
        self.bot.send_message(call.message.chat.id, text=f"Выберите отметку", reply_markup=keyboard)
        
    def mark(self, data):
        (dummy, mark, user, subject) = data.split(":")    #   ~:mark:user:subject
        return self.schedule.set_mark(user, subject, mark)


