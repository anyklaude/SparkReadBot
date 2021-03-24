from telegram import Bot, Update
from telegram.utils.request import Request
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from db import init_db, add_user
from config import token


def start_handler(bot: Bot, update: Update):
	user = update.message.from_user['username']
	update.message.reply_text(f"Привет, {user}! "
							  f"Я помогу подобрать тебе собеседника по твоим книжным интересам. "
							  f"Напиши мне что-нибудь.")
	return 0


def first_handler(bot: Bot, update: Update, user_data: dict):
	update.message.reply_text("Ваша последняя прочитанная книга?")
	return 1


def second_handler(bot: Bot, update: Update, user_data: dict):
	user_data[1] = update.message.text
	update.message.reply_text("Ваша недавно прочитанная книга?")
	return 2


def third_handler(bot: Bot, update: Update, user_data: dict):
	user_data[2] = update.message.text
	update.message.reply_text("Другая недавно прочитанная книга?")
	return 3


def finish_handler(bot: Bot, update: Update, user_data: dict):
	user_data[3] = update.message.text
	update.message.reply_text(f"Отлично! \n"
	 						  f"1) {user_data[1]} \n"
	 						  f"2) {user_data[2]} \n"
	 						  f"3) {user_data[3]}")


	add_user(update.message.from_user['username'], user_data[1], user_data[2], user_data[3])
	return ConversationHandler.END


def cancel_handler(bot: Bot, update: Update):
	return ConversationHandler.END


def main():
	bot = Bot(token=token)
	updater = Updater(bot=bot)

	init_db()

	req = Request(connect_timeout=0.5, read_timeout=1)

	conversation_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start_handler)],
		states={
			0: [MessageHandler(Filters.all, first_handler, pass_user_data=True)],
			1: [MessageHandler(Filters.all, second_handler, pass_user_data=True)],
			2: [MessageHandler(Filters.all, third_handler, pass_user_data=True)],
			3: [MessageHandler(Filters.all, finish_handler, pass_user_data=True)],
		},
		fallbacks=[CommandHandler('cancel', cancel_handler)]
	)

	updater.dispatcher.add_handler(conversation_handler)

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
