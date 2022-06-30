import nextcord
import pygsheets
from nextcord.ext import commands
import pandas as pd
import requests, json, random, datetime, asyncio

#authorization
gc = pygsheets.authorize(service_file='data/creds.json')

#nextcord init
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command(name="hi")
async def SendMessage(ctx):
	await ctx.send('Hellopp!')

@bot.command(name="dc")
async def logout(ctx):
	await ctx.close()

async def schedule_daily_message():
	#open google sheet
	sh = gc.open("Prototype Spreadsheet")

	#format spreadsheet into DF
	all = sh.sheet1.get_all_records()
	df = pd.DataFrame(all)

	#get current time
	now = datetime.datetime.now()
	while True:
    	#get latest message info 
		row = df[(df['posted'] == '') & (df['discord_server'] == 'DS')].head(1)
		row.time = pd.to_datetime(row.time)

		#get wait time
		wait_time = abs((row.time-now).dt.total_seconds().values[0])
		print(f"Wait-time: {wait_time}")
		await asyncio.sleep(wait_time)

		#update spreadsheet before posting
		cell = 'E' + str(row.id_challenge.values[0] + 1)
		sh.sheet1.update_value(cell, 'yes')

		#posting message
		channel = bot.get_channel(#INSERT CHANNEL ID HERE)
		content = f"Hello Coderschool Learners, here is the challenge's link for today {row.url.values[0]}. Good luck!"
		await channel.send(content)

		#sync spreadsheet and update on memory df
		sh.sheet1.refresh(update_grid=False)
		all = sh.sheet1.get_all_records()
		df = pd.DataFrame(all)

@bot.event
async def on_ready():
	print(f"Logged in as: {bot.user.name}")
	await schedule_daily_message()

if __name__ == '__main__':
	bot.run("#INSERT BOT TOKEN HERE")