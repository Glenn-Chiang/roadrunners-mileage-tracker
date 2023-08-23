from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(text='Enter your callsign/name')
    return 'register'


async def register(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    callsign = update.message.text
    try:
        await update.message.reply_text('Processing...')
        requests.post(
            f'{BASE_URL}/registerUser?userId={user_id}&callsign={callsign}')
        await update.message.reply_text('Registration successful! Type "/clock <distance>" to clock distance in km\n\ne.g. /clock 2.4')
    except Exception as error:
        await update.message.reply_text(f'ERROR: {error}')

registerHandler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        'register': [MessageHandler(filters=filters.TEXT, callback=register)]
    },
    fallbacks=[]
)


async def clockMileageHandler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    if len(context.args) < 1:
        await update.message.reply_text('Please specify the distance clocked in km\n\ne.g. /clock 2.4')
        return
    
    mileage = context.args[0]
    
    try:
        total_mileage = requests.post(
            f'{BASE_URL}/addMileage?userId={user_id}&mileage={mileage}').json()['totalMileage']
        await update.message.reply_text(f'Mileage clocked! Your total mileage so far: {total_mileage}km')
    except Exception as error:
        await update.message.reply_text(f'ERROR: {error}')
