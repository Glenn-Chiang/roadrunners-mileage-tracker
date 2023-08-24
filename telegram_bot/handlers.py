from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
import requests


async def getCallsign(update: Update, context: CallbackContext):
    await update.message.reply_text(text='Enter your callsign/name')
    return 'team'


async def getTeam(update: Update, context: CallbackContext):
    context.user_data['callsign'] = update.message.text.upper()
    await update.message.reply_text(text='Enter your team e.g. A')
    return 'register'


async def register(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    callsign = context.user_data['callsign']
    teamId = update.message.text

    if teamId.upper() not in ['A', 'B', 'C']:
        await update.message.reply_text('Invalid team')
        return 'team'

    try:
        await update.message.reply_text('Processing...')
        requests.post(
            f'https://registeruser-znvjhrzzxa-uc.a.run.app/?userId={user_id}&callsign={callsign}&teamId={teamId}')
        await update.message.reply_text('Registration successful! Type "/clock <distance>" to clock distance in km\n\ne.g. /clock 2.4')
    except Exception as error:
        await update.message.reply_text(f'ERROR: {error}')
    return ConversationHandler.END


registerHandler = ConversationHandler(
    entry_points=[CommandHandler('start', getCallsign)],
    states={
        'team': [MessageHandler(filters=filters.TEXT, callback=getTeam)],
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
            f'https://clockmileage-znvjhrzzxa-uc.a.run.app/?userId={user_id}&mileage={mileage}').json()['totalMileage']
        await update.message.reply_text(f'Mileage clocked! Your total mileage so far: {total_mileage}km')
    except Exception as error:
        print(error)
        await update.message.reply_text(f'ERROR: {error}')


async def rankHandler(update: Update, context: CallbackContext):
    try:
        users = requests.get(f'https://getranking-znvjhrzzxa-uc.a.run.app').json()
        formatted_users = ('\n').join(
            [f"{idx + 1}. {user['callsign']} {user['totalMileage']}km" for idx, user in enumerate(users)])
        await update.message.reply_text(formatted_users)
    except Exception as error:
        print(error)
        await update.message.reply_text(f'ERROR: {error}')


async def teamRankHandler(update: Update, context: CallbackContext):
    try:
        teams_list = []
        teams = requests.get(f'https://getteamranking-znvjhrzzxa-uc.a.run.app/').json()
        for team in teams:
            team_id: str = team['id']
            team_mileage: str = team['mileage']
            team_members: list = team['members']
            formatted_team_members = ('\n').join(
                [f"{idx + 1}. {user['callsign']} {user['totalMileage']}km" for idx, user in enumerate(team_members)])
            formatted_team = f"TEAM {team_id} ({team_mileage} KM)\n{formatted_team_members}"
            teams_list.append(formatted_team)
        formatted_teams_list = ('\n\n').join(teams_list)
        await update.message.reply_text(formatted_teams_list)
    except Exception as error:
        print(error)
        await update.message.reply_text(f'ERROR: {error}')
