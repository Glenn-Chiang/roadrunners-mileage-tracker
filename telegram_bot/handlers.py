from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler
import requests

async def registerHandler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    # request to register user
    await update.message.reply_text('Registration successful! Type "/clock <distance>" to clock distance in km\n\ne.g. /clock 2.4')

async def clockMileageHandler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    mileage = context.args[0]
    # requests.post()
    total_mileage = 10
    await update.message.reply_text(f'Mileage clocked! Total mileage: {total_mileage}')