from schedule import Schedule
from telegram import TelegramBot

SPREADSHEET_ID = "1aeQ7my0K_YB5iP19OzWWawqVJH1gctqPUjjeq4GEiwQ"
SERVICE_ACCOUNT_FILE = 'D:\\visiting.json'
TELEGRAM_TOKEN = '7296422640:AAHr8GLP4wyVKMmm5Kg3ggfCSxUiOM-p3Fw'

schedule = Schedule(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID)
telegram_bot = TelegramBot(TELEGRAM_TOKEN, schedule)
telegram_bot.start()