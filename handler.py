#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
	port_num = 3306

	def set_port(self, port_num):
		self.port_num = port_num

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()

	def _html(self):
		return f'<html><body>{self.port_num}</body></html>'.encode('utf8')

	def do_GET(self):
		self._set_headers()
		self.wfile.write(self._html())

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		self._set_headers()
		self.wfile.write(self._html())
