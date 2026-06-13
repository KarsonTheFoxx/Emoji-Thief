# Emoji Theif bot
# A simple bot that can steal the emojis from any server regardless of if it is private or not
# Written by KarsonTheFoxx

from disnake.ext import commands
from disnake import Status, Activity, ActivityType, Intents
from os import environ
from dotenv import load_dotenv
from asyncio import run

# Main loop
async def main(TOKEN:str):
    INTENTS = Intents.default()

    bot = commands.InteractionBot(intents=INTENTS, reload=True)

    bot.load_extensions("./extensions/")

    @bot.event
    async def on_ready():
        await bot.wait_until_ready()
        print("Ready")
        await bot.change_presence(status=Status.idle, activity=Activity(name="Stealing emojis", type=ActivityType.custom))
    

    await bot.start(TOKEN)

if __name__ == "__main__":

    load_dotenv("./.env")
    TOKEN = environ.get("TOKEN")

    run(main=main(TOKEN=TOKEN))
