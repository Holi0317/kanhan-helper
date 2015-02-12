#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import urllib
from http import cookiejar
import re
import datetime

AUTH_URL = 'http://chinese.kanhan.com/zh-hant/user/login'
MAIN_URL = 'http://pth-reading.chinese.kanhan.com/'
SEARCH_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/article/search'
PRAC_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/quiz/{0}'
EXER_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/node/{0}/take'

class kanhan_api(object):
	def __init__(self):
		# create cookiejar for cookies
		self.cj = cookiejar.CookieJar()
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
		urllib.request.install_opener(self.opener)
		return
	
	def login(self, id, passwd, school_id):
		"""
		Login into kanhan
		return True if success, else, return False
		"""
		value = {'name' : '{0}_{1}'.format(school_id, id), 'pass' : passwd, 'school_code' : school_id, 'submit' : '登入', 'form_id' : 'user_login'}
		data = urllib.parse.urlencode(value).encode('utf-8')
		req = urllib.request.Request(AUTH_URL, data)
		with urllib.request.urlopen(req) as k:
			i = k.read().decode()
		if re.search(r"很抱歉", i):
			return False
		return True
	
	def get_id(self, day=None):
		"""
		Get exercise ID
		if day is none, will write the id into self.today_id
		otherwise, it will return the id. Please store it for lateron usage
		"""
		if day == None:
			with urllib.request.urlopen(MAIN_URL) as k:
				i = k.read().decode()
			self.today_id = re.search(r'<a href="/zh-hant/quiz/(\d+/.+?)"', i).group(1)
			return
		else:
			day = str(day)
		today = datetime.date.today()
		month = str(today.month)
		year = str(today.year)
		date = '/'.join([day, month, year])
		value = {'field_date2_value_1[min][date]' : date, 'field_date2_value_1[max][date]' : date}
		data = urllib.parse.urlencode(value)
		url = SEARCH_URL+'?'+data
		with urllib.request.urlopen(url) as k:
			i = k.read().decode()
		s = re.search(r'<tr class="odd views.+<a href="/zh-hant/quiz/(\d+/.+?)">', i, re.DOTALL)
		return s.group(1)
	
	def get_tokens(self, id):
		"""
		Return tokens
		Please don't call it
		this will be automatically callud by take_exercise()
		"""
		url = PRAC_URL.format(id)
		with urllib.request.urlopen(url) as k:
			i = k.read().decode()
		token = re.search(r'"form_token" value="(.+)"', i).group(1)
		form_build_id = re.search(r'"form_build_id" value="(.+)"', i).group(1)
		return token, form_build_id
	
	def take_exercise(self, is_random , answers = None, id = None):
		"""
		take the exercise module
		will call get_tokens automatically
		required augments
			is_ramdom: if true, will input all answers as A. Else, it will send answers out
			answers: is_random must be False, accept a dict as input. format is qid:answer_id
			id: accept question id, default as today, please use the one reutrned by get_id()
		This will return the answers and save as self.answers
		Known Bug: This cannot be used for typing question, which is quite rare to see
		"""
		if id == None and self.today_id != None:
			id = self.today_id
		elif id == None and self.today_id == None:
			get_id()
			id = self.today_id
			print('Warning: did not call get_id before doing this. Please contact the developer of the client')
		if not is_random and answer == None:
			raise ValueError

		# build informations for taking questions
		token, form_build_id = self.get_tokens(id)
		value = {'op' : '開始練習', 'form_build_id' : form_build_id , 'form_token' : token, 'form_id' : 'quiz_start_quiz_button_form'}
		url = EXER_URL.format(id.split(r'/')[0])
		qs_db = {}
		qs_nid_db = []
		self.answers = {}

		# First attempt, take total number of questions
		data = urllib.parse.urlencode(value).encode('utf-8')
		with urllib.request.urlopen(urllib.request.Request(url, data)) as k:
			c = k.read().decode()
		total_qs = int(re.search('"quiz-num-questions".+(\d+)<?', c).group(1))
		value['op'] = '下一題'

		# looping questions
		for i in range(total_qs):
			qs_nid = re.search(r'"question_nid".+"(\d+)"', c).group(1)
			try_ans = re.findall(r'"tries\[answer?]".+"(\d+)"', c)
			# prep for the next stage
			qs_db[qs_nid] = try_ans
			qs_nid_db.append(qs_nid)

			value['form_id'] = 'quiz_question_answering_form'
			# Change op to '遞交' when it is the last question
			if i == total_qs-1:
				value['op'] = '遞交'
			if is_random:
				value[r'tries[answer]'] = try_ans[0]
			else:
				value[r'tries[answer]'] = answers[qs_nid]
			# make request
			data = urllib.parse.urlencode(value).encode('utf-8')
			with urllib.request.urlopen(urllib.request.Request(url, data)) as k:
				c = k.read().decode()
		
		# read for answers
		raw = re.findall(r'This option is correct.+<td>(\w)', c)
		con_alph = {'A':0, 'B':1, 'C':2, 'D':3}
		for i in range(total_qs):
			ans = con_alph[raw[i]]
			qs_nid = qs_nid_db[i]
			qs_try_ans = qs_db[qs_nid][ans]
			self.answers[qs_nid] = qs_try_ans
		return self.answers

def main():
	api = kanhan_api()
	if api.login(17132, 'wgfqty', 'stmarks'):
		api.get_id()
		#api.take_exercise(True)

	return

if __name__ == '__main__':
	main()
