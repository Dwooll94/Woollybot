import discord
import asyncio
from datetime import datetime, date, time, timedelta
from discord.ext.commands import Bot
from threading import Timer

my_bot = Bot(command_prefix=">")
up_yours_fname = "upyurs.jpg"

timeToCountMessagesIn= 3
maxMessagesInXSeconds = 3
maxCharsInXSeconds = 2500
spamStrikes = 3
maxKickRememberanceTime = 86400

userDict = {}



class woollyUser:
	mention=""
	_messages = []
	_kicks = []
	
	def __init__(self, mention):
		self.mention = mention
	
	def processMessage(self, newMessage):
		while self._messages and datetime.utcnow() - self._messages[0].timestamp > timedelta(0,timeToCountMessagesIn):
			self._messages.pop(0)
		self._messages.append(newMessage)
		print(self.mention + ":" + str(len(self._messages)))
		if len(self._messages) > maxMessagesInXSeconds:
			return 1
		chars = 0
		for message in self._messages:
			chars += len(message.content)
		if chars > maxCharsInXSeconds:
			return 1
		return 0
	
	def purgeMessages(self):
		self._messages = []
		
	def processKick(self):
		while self._kicks and datetime.utcnow() - self._kicks[0] > timedelta(0,maxKickRememberanceTime):
			self._kicks.pop(0)
		self._kicks.append(datetime.utcnow())
		if len(self._kicks) >= spamStrikes:
			return 1
		return 0
		
	def purgeKicks(self):
		self._kicks = []
	
class woollyReminder:
	
@my_bot.event
@asyncio.coroutine 
def  on_read():
    print("Client logged in")
@my_bot.event
@asyncio.coroutine 
def on_message(message):
	#Anti-spam handler
	if message.author.mention != my_bot.user.mention:
		print("Got Message!: " + message.content)
		if message.author.mention in userDict.keys():
			print("Processing Message")
			if userDict[message.author.mention].processMessage(message) == 1:
				print("Kicking thy ass.")
				yield from my_bot.send_message(message.channel, "SPAM DETECTED!")

				if userDict[message.author.mention].processKick() == 1:
					try:
						yield from my_bot.send_message(message.channel, "Ok, " + message.author.mention + ", put your head between your legs and kiss your butt goodbye!")
					except Forbidden:
						yield from my_bot.kick(message.author)
					yield from my_bot.ban(message.author)
				else:
					imakik = "I'm gonna kick your ass, " + message.author.mention + "!"
					yield from my_bot.send_message(message.channel, imakik)
					yield from my_bot.kick(message.author)
		else:
			print("Added User:" + message.author.mention)
			userDict[message.author.mention] = woollyUser(message.author.mention)
			userDict[message.author.mention].processMessage(message)
		#Commands and etc.	
		if message.content.startswith(">"):
			#Greentext
			print("Greentext!")
			output = "```css\n>" + message.content[1:] +"\n```"
			yield from my_bot.send_message(message.channel, output)
		elif message.content.startswith("^"):
			print("Up Yours!")
			#Posts later-censored Inkling doing the european up-yours gesture
			yield from my_bot.send_file(message.channel, up_yours_fname)
			statement = "Up yours, " + message.content[1:] + "!"
			yield from my_bot.send_message(message.channel, statement)
		elif message.content.startswith("$"):
			#commands
			commandString = message.content[1:]
			lowerString = commandString.lower()
			if lowerString.startswith("remindme"):
				#reminder command
				#syntax $remindme <a/r>[<time>] <reminder text>
				if lowerString[9] == "a":
					#absoluteTime
				elif lowerSTring[9] == "r":
					#relativeTime
		elif message.content.lower().startswith("good job, woollybot"):
			print("YAY!")
			statement = "Thank you, master " + message.author.mention +"!"
			yield from my_bot.send_message(message.channel, statement)
			yield from my_bot.add_reaction(message, '\N{THUMBS UP SIGN}');
		elif message.content.lower().startswith("bad woollybot"):
			print("Aww :<")
			statement = "Sorry, master " + message.author.mention + "!"
			yield from my_bot.send_message(message.channel, statement)
			yield from my_bot.add_reaction(message, '\U0001F62C');
	return 0

my_bot.run('Change Me')