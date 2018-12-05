import socket 
from util import ircUtil

ircSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
ircSocket.connect( ( "140.112.28.129", 6667 ) )
#ircSocket.connect( ( "127.0.0.1", 6667 ) )
Msg = "NICK bot_r06723025 \r\n USER r06723025 \r\n LIST \r\n JOIN #CN_DEMO \r\n PRIVMSG #CN_DEMO :I'm r06723025! \r\n"
ircSocket.send( bytes( Msg , encoding = "utf-8") )
while True :
	try:
		ircMsg = ircSocket.recv(4096).decode()
	except:
		continue
	print ("init:",ircMsg)
	msg = ircMsg.split(" ", 4)
	
	if msg[0] == "PING":
		ircSocket.send(bytes("PONG  \r\n", encoding="utf-8"))
	elif msg[1] == "PRIVMSG":
		sender = msg[0].split("!")[0][1:]
		if sender.strip("\r\n") == "#CN_DEMO":
			continue
		horoscopes = ["Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", \
					"Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius"]
		command = msg[3][1:].strip("\r\n")
		#print("Command:" , command)
		if command in horoscopes:
			response = ircUtil.dailyHoroscope()
			ircSocket.send(bytes("PRIVMSG {} :".format(sender)+response+"\r\n", encoding = "utf-8"))

		elif command == "!guess":
			ircUtil.guessNumber(ircSocket, sender)
		elif command == "!song":
			print(msg)
			try:
				name = msg[4].strip("\r\n")
			except:
				ircSocket.send(bytes("PRIVMSG {} :".format(sender)+"No song name!"+"\r\n", encoding="utf-8"))
				continue
			url = ircUtil.musicBot(name)
			ircSocket.send(bytes("PRIVMSG {} :".format(sender)+url+"\r\n", encoding="utf-8"))

		elif command == "!chat":
			ircUtil.chat(ircSocket,sender)
		#else:
		#	ircSocket.send(bytes("PRIVMSG {} :No such command! \r\n".format(sender), encoding="utf-8"))

	
