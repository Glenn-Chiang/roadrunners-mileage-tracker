from handlers import startHandler, registerCallsign, registerTeam, clockMileageHandler, rankHandler, teamRankHandler
import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
load_dotenv()


async def main(event):
    app = Application.builder().token(token=os.getenv('BOT_TOKEN')).build()

    app.add_handler(CommandHandler('start', startHandler))
    app.add_handler(CommandHandler('callsign', registerCallsign))
    app.add_handler(CommandHandler('team', registerTeam))
    app.add_handler(CommandHandler('clock', clockMileageHandler))
    app.add_handler(CommandHandler('rank', rankHandler))
    app.add_handler(CommandHandler('teamrank', teamRankHandler))

    await app.initialize()
    update = Update.de_json(data=json.loads(event['body']), bot=app.bot)
    await app.process_update(update=update)


def lambda_handler(event, context):
    asyncio.run(main(event))


# def main():
#     app = Application.builder().token(token=os.getenv('BOT_TOKEN')).build()

#     app.add_handler(registerHandler)
#     app.add_handler(CommandHandler('clock', clockMileageHandler))
#     app.add_handler(CommandHandler('rank', rankHandler))
#     app.add_handler(CommandHandler('teamrank', teamRankHandler))

#     print('Bot running...')
#     app.run_polling()

# if __name__ == "__main__":
#     main()