from telegram import Update
from telegram.ext import CallbackContext
import requests


async def startHandler(update: Update, context: CallbackContext):
    await update.message.reply_text('To register, please enter the following command:\n/callsign <your_callsign_or_name>\n\ne.g.\n/callsign Glenn')


async def registerCallsign(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    callsign = ('_').join(context.args) # Join name into 1 word if it contains spaces

    try:
        requests.post(
            f'https://registercallsign-znvjhrzzxa-uc.a.run.app/?userId={user_id}&callsign={callsign}')
        await update.message.reply_text('You have registered your callsign! Please register which team you are in by entering the following command:\n/team <your_team>\n\ne.g.\n/team C')
    except Exception as error:
        await update.message.reply_text(f'ERROR: {error}')


async def registerTeam(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    teamId = context.args[0]

    if teamId.upper() not in ['A', 'B', 'C']:
        await update.message.reply_text('Invalid team')
        return

    try:
        requests.post(f'https://registerteam-znvjhrzzxa-uc.a.run.app/?userId={user_id}&teamId={teamId}')
        await update.message.reply_text('You have registered your team! To start clocking your mileage in KM, enter: /clock <mileage>\n\ne.g. /clock 2.4\n\nAlternatively, type /help to view more commands')
    except Exception as error:
        await update.message.reply_text(f'ERROR: {error}')


async def helpHandler(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "/clock <mileage>\nClock mileage in KM\n\n/rank\nView mileage ranking across all personnel\n\n/teamrank\nView mileage ranking for each team\n\n/callsign <your_callsign>\nReenter your callsign if you previously entered it incorrectly\n\n/team <your_team>\nReenter your team if you previously entered it incorrectly"
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
        users = requests.get(
            f'https://getranking-znvjhrzzxa-uc.a.run.app').json()
        formatted_users = ('\n').join(
            [f"{idx + 1}. {user['callsign']} {user['totalMileage']}km" for idx, user in enumerate(users)])
        await update.message.reply_text(formatted_users)
    except Exception as error:
        print(error)
        await update.message.reply_text(f'ERROR: {error}')


async def teamRankHandler(update: Update, context: CallbackContext):
    try:
        teams_list = []
        teams = requests.get(
            f'https://getteamranking-znvjhrzzxa-uc.a.run.app/').json()
        for team in teams:
            team_id: str = team['id']
            team_total_mileage: str = team['mileage']
            team_members: list = team['members']
            team_average_mileage = round(int(team_total_mileage) / len(team_members))
            formatted_team_members = ('\n').join(
                [f"{idx + 1}. {user['callsign']} {user['totalMileage']}km" for idx, user in enumerate(team_members)])
            formatted_team = f"TEAM {team_id} (AVG {team_average_mileage} KM)\n{formatted_team_members}"
            teams_list.append(formatted_team)
        formatted_teams_list = ('\n\n').join(teams_list)
        await update.message.reply_text(formatted_teams_list)
    except Exception as error:
        print(error)
        await update.message.reply_text(f'ERROR: {error}')
