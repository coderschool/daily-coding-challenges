import nextcord
from nextcord.ext import commands
import pandas as pd
import requests, json, random, datetime, asyncio, os, pygsheets

#get environment var
bot_token = os.getenv('BOT_TOKEN')
ds_id = int(os.getenv('DS_SERVER'))
web_id = int(os.getenv('WEB_SERVER'))


#authorization
gc = pygsheets.authorize(service_account_env_var='GOOGLE_CREDS')

#nextcord init
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command(name="hi")
async def SendMessage(ctx):
	await ctx.send("Hello")

@bot.command(name="dc")
async def logout(ctx):
	await bot.close()

async def schedule_daily_message():
	#open google sheet
	sh = gc.open("code_challenge_db")

	#format spreadsheet into DF
	all = sh.sheet1.get_all_records()
	df = pd.DataFrame(all)

	#get current time
	now = datetime.datetime.now()
	while True:
    		#get latest message info for DS
		row_ds = df[(df['posted'] == '') & (df['discord_server'] == 'DS')].head(1)
		row_ds.time = pd.to_datetime(row_ds.time)
		print(row_ds)
		
		#get latest message info for WEB
		row_web = df[(df['posted'] == '') & (df['discord_server'] == 'Web')].head(1)
		row_web.time = pd.to_datetime(row_web.time)
		print(row_web)
		
		#get wait time
		wait_time = (row_ds.time-now).dt.total_seconds().values[0]
		print(f"Wait-time: {wait_time}")

		
		if wait_time >= 0: #check if the message is in the future (>=0) or in the past (<0)
			await asyncio.sleep(wait_time)
			
			#--------------------------
			
			#posting message for DS
			ds_channel = bot.get_channel(ds_id)
			content = f"Hello Coderschool Virgil DS Learners, the challenge for today is ** {row_ds.challenge_used.values[0]} **. \n The difficulty is ** {row_ds.difficulty.values[0]} ** \n The contest's link is {row_web.url.values[0]}. \n Submission time will be valid for 1 day after this announcement. Good luck!"
			msg = await ds_channel.send(content)
			print(f'Posted message with id: {row_ds.id_challenge.values[0]} on DS server')

			#update spreadsheet, E column for "posted"
			cell = 'E' + str(row_ds.id_challenge.values[0] + 1)
			sh.sheet1.update_value(cell, 'yes')

			#get message url and update spreadsheet H column for "message_url"
			link_cell = 'F' + str(row_ds.id_challenge.values[0] + 1)
			sh.sheet1.update_value(link_cell, msg.jump_url)

			#--------------------------

			#posting message for WEB
			web_channel = bot.get_channel(web_id)
			content = f"Hello Coderschool Virgil Web Learners, the challenge for today is ** {row_web.challenge_used.values[0]} **. \n The difficulty is ** {row_web.difficulty.values[0]} ** \n The contest's link is {row_web.url.values[0]}. \n Submission time will be valid for 1 day after this announcement. Good luck!"
			msg = await web_channel.send(content)
			print(f'Posted message with id: {row_web.id_challenge.values[0]} on Web server')

			#update spreadsheet, E column for "posted"
			cell = 'E' + str(row_web.id_challenge.values[0] + 1)
			sh.sheet1.update_value(cell, 'yes')

			#get message url and update spreadsheet H column for "message_url"
			link_cell = 'F' + str(row_web.id_challenge.values[0] + 1)
			sh.sheet1.update_value(link_cell, msg.jump_url)

			#sync spreadsheet and update on memory df
			sh.sheet1.refresh(update_grid=False)
			all = sh.sheet1.get_all_records()
			df = pd.DataFrame(all)
		else:
			#create artificial buffer wait-time for github to action a new scheduled run
			await asyncio.sleep(abs(wait_time))
			
			#sync spreadsheet and update on memory df
			sh.sheet1.refresh(update_grid=False)
			all = sh.sheet1.get_all_records()
			df = pd.DataFrame(all)
@bot.event
async def on_ready():
	print(f"Logged in as: {bot.user.name}")
	await schedule_daily_message()

if __name__ == '__main__':
	bot.run(bot_token)
