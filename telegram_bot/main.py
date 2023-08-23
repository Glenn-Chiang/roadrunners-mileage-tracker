from handlers import registerHandler, clockMileageHandler
import requests
import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
load_dotenv()


def main():
    app = Application.builder().token(token=os.getenv('BOT_TOKEN')).build()

    app.add_handler(handler=registerHandler)
    app.add_handler(handler=CommandHandler('clock', clockMileageHandler))

    # await app.initialize()
    # update = Update.de_json(data=json.loads(event['body']), bot=app.bot)
    # await app.process_update(update=update)
    print('Bot running...')
    app.run_polling()

def lambda_handler(event, context):
    asyncio.run(main(event))


if __name__ == "__main__":
    main()