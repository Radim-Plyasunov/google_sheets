import gspread
import telebot
import datetime
from telebot import types
from create_week import create_week
from gs_utils import find_user, get_subjects

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1aeQ7my0K_YB5iP19OzWWawqVJH1gctqPUjjeq4GEiwQ"
SERVICE_ACCOUNT_FILE = 'D:\\visiting.json'

gc = gspread.service_account(SERVICE_ACCOUNT_FILE)

sheet = gc.open_by_key(SPREADSHEET_ID);
user_ws = sheet.worksheet('users')
subject_ws = sheet.worksheet('schedule')
name = "08.07.2024"

#create_week(name, sheet)

bot = telebot.TeleBot('7296422640:AAHr8GLP4wyVKMmm5Kg3ggfCSxUiOM-p3Fw')


@bot.message_handler(commands=['start'])
def MessageHandler(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_full_name = find_user(user_ws, user_id, user_name)    
    bot.reply_to(message, f'Hello {user_full_name}')
    weekday = datetime.datetime.today().weekday()
    subjects = get_subjects(subject_ws, weekday)
    keyboard = types.InlineKeyboardMarkup()
    for subject in subjects:
        button = types.InlineKeyboardButton(subject, callback_data='subject_button')
        keyboard.add(button)
    bot.send_message(message.chat.id, text=f"select subject", reply_markup=keyboard)
    #print(message)

bot.polling(none_stop=True)