# daily-coding-challenges
<h2>A discord bot that sends scheduled messages, data stored from google spreadsheets, input data with pygsheets then coded with nextcord lib</h2>

1. Create project in Google Cloud console and create a service account
2. Get google sheets API Key and google drive key, download credentials as JSON file
3. Set up discord bot in discord developer mode then connect it to desired discord server
4. Get channel id where you want the messages to be in (right click channel name to copy ID)
5. Enable SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT in discord dev portal: Select Bot > Bot > Enable intent
6. Make sure spreadsheet with correct name and columns format desired
7. IMPORTANT: Make sure that you share the spreadsheet with the service account's email that you created earlier with editor's permission. 
8. Then just run the code and the bot should automatically login and set a timer.

To be implemented/In Progress:
Resend challenges that hasn't been posted at the correct time. 
