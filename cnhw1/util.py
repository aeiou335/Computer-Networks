import sys
import random
import select
import requests
from bs4 import BeautifulSoup

class ircUtil():
	def dailyHoroscope():
		sentences = ["Like a boss!", "You're going to fall in love with someone today!", "Disaster!", "Healthy!", "Sorry but you're going to lose money!", "Life sucks", "Nothing special today!"]
		return random.choice(sentences)

	def guessNumber(ircSocket, sender):
		ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"Guess a number between 1~10! \r\n", encoding="utf-8"))
		ircSocket.settimeout(10)
		sol = random.randint(1,10)
		guessed = []
		while True:
			try:
				ircMsg = ircSocket.recv(4096).decode().split(" ")
				if ircMsg[0].split("!")[0][1:] != sender:
					continue
			except:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"Game over due to timeout! \r\n", encoding="utf-8"))
				break
			try:
				number = int(ircMsg[3][1:])
				if number > 10 or number < 1:
					ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"Plz read the rule! \r\n", encoding="utf-8"))
					continue
			except:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"Oops!Something wrong! \r\n", encoding="utf-8"))
				continue
			if number in guessed:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"You have already guessed it! \r\n", encoding="utf-8"))
				continue
			else:
				guessed.append(number)
			if number > sol:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"The number is too high! \r\n", encoding="utf-8"))
			elif number < sol:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"The number is too low! \r\n", encoding="utf-8"))
			else:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"You're right! The answer is {} \r\n".format(number), encoding="utf-8"))
				break

	def musicBot(name):
		print(name)
		queryname = "+".join(name.split(" ")).lower()
		r = requests.get("https://www.youtube.com/results?search_query="+queryname)
		soup = BeautifulSoup(r.text, "html.parser")
		s = soup.find_all("div", {"class":"yt-lockup-content"})
		for i,data in enumerate(s):
			h = data.find("a")["href"]
			if h[:6] == "/watch":
				break
		return "https://www.youtube.com"+h

	def chat(ircSocket,sender):
		print("Start Chatting!")
		#print(">", end="")
		while True:
			#print("sender:",sender)
			i, _, _ = select.select( [ircSocket], [], [], 0.1 )
			i2, _, _ = select.select( [sys.stdin], [], [], 0.1 )
			if (i):
				receive = ircSocket.recv(4096).decode().split(" ", 3)
				#print("rec:",receive)
				msg = receive[-1].strip("\r\n")
				if receive[0].split("!")[0][1:] != sender or receive[2] != "bot_r06723025":
					continue
				if receive[0].strip("\r\n") == "PING":
					ircSocket.send(bytes("PONG  \r\n", encoding="utf-8"))
					continue
				if "text to send" in msg:
					continue
				if msg[1:] == "!bye" or msg == "lost":
					print("{} has left!".format(sender))
					break
				print (sender+msg)
			if (i2):
				#print(sys.stdin.readline().strip())
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+sys.stdin.readline(), encoding="utf-8"))
			
			





