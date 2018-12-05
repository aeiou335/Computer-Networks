import socket # Include library
import time
import sys
import select
ircSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#IRCSocket.settimeout(1)
ircSocket.connect( ( "127.0.0.1", 6667 ) )
Msg = "NICK TA233 \r\n USER rrrr \r\n JOIN #CN_DEMO \r\n  PRIVMSG #CN_DEMO :Hello \r\n"
ircSocket.send( bytes( Msg , encoding = "utf-8") )
while True:
	#print("sender:",sender)
	i, _, _ = select.select( [ircSocket], [], [], 0.1 )
	i2, _, _ = select.select( [sys.stdin], [], [], 0.1 )
	if (i):
		print (ircSocket.recv(4096).decode())
	if (i2):
		#print(sys.stdin.readline().strip())
		#ircSocket.send(bytes("PRIVMSG bot_r06723025 :"+sys.stdin.readline(), encoding="utf-8"))
		ircSocket.send(bytes("PRIVMSG #CN_DEMO :"+sys.stdin.readline(), encoding="utf-8"))