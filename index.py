import telegram
from models.TelegramBot import TelegramBot, os

if __name__ == '__main__':
  telegram_bot = TelegramBot(os.environ['TOKEN'])
  telegram_bot.init()