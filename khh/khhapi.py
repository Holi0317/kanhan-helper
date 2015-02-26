#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import urllib
from http import cookiejar
import re
import logging

AUTH_URL = 'http://chinese.kanhan.com/zh-hant/user/login'
MAIN_URL = 'http://pth-reading.chinese.kanhan.com/'
SEARCH_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/article/search'
PRAC_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/quiz/{0}'
EXER_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/node/{0}/take'
RESULT_URL = 'http://pth-reading.chinese.kanhan.com/zh-hant/node/{0}/myresults'

# initialize logging
logger = logging.getLogger(__name__)


class kanhan_api(object):
    def __init__(self):
        # create cookiejar for cookies
        logger.info('Iniializing api')
        self.cj = cookiejar.CookieJar()
        self.cookie = urllib.request.HTTPCookieProcessor(self.cj)
        self.opener = urllib.request.build_opener(self.cookie)
        urllib.request.install_opener(self.opener)
        self.today_id = None
        self.answers = []
        return

    def login(self, id, passwd, school_id):
        """
        Login into kanhan_api
        return True if success, else, return False
        """
        value = {'name': '{0}_{1}'.format(school_id, id), 'pass': passwd,
                 'school_code': school_id, 'submit': '登入',
                 'form_id': 'user_login'}
        data = urllib.parse.urlencode(value).encode('utf-8')
        req = urllib.request.Request(AUTH_URL, data)
        try:
            with urllib.request.urlopen(req) as k:
                i = k.read().decode()
        except:
            logger.warn('Login got http Exception')
            return False
        if re.search(r"很抱歉", i):
            logger.warn('Login got incorrect data')
            return False
        logger.info('Login succeed')
        return True

    def get_id(self, date=None):
        """
        Get exercise ID
        Accept datetime.date as an input
        if date is None, will write the id into self.today_id and return it
        otherwise, it will return the id. Please store it for later on usage
        Will return None if there is no exercise for that day
        """
        if date is None:
            # Default behaviour, get today id
            logger.info('get_id will get today id')
            with urllib.request.urlopen(MAIN_URL) as k:
                i = k.read().decode()
            search = re.search(r'<a href="/zh-hant/quiz/(\d+/.+?)"', i)
            if search:
                self.today_id = search.group(1)
                logger.info('ID: {0}'.format(self.today_id))
                return self.today_id
            else:
                logger.warn('No exercise today')
                return None
        logger.info('get_id will get id for {0}'.format(date))
        date = '/'.join([str(date.day), str(date.month), str(date.year)])
        value = {'field_date2_value_1[min][date]': date,
                 'field_date2_value_1[max][date]': date}
        data = urllib.parse.urlencode(value)
        url = SEARCH_URL+'?'+data
        logger.debug('url: {0}'.format(url))
        with urllib.request.urlopen(url) as k:
            i = k.read().decode()
        s = re.search(
            r'views-field views-field-title.*<a href="/zh-hant/quiz/(\d+/.+?)">',
            i, re.DOTALL)
        if s:
            logger.info('ID: {0}'.format(s.group(1)))
            return s.group(1)
        else:
            logger.warn('No exercise for {0}'.format(date))
            return None

    def is_exercise_done(self, id=None):
        """
        Test if exercise has Done
        If true, it will return 0
        else, it will return the token for conducting the exercise
        This function will automatically be called by take_exercise
        As take_exercise will return false if the exercise has done,
        there is no reason for developers to call this function
        """
        if id is None and self.today_id is not None:
            logger.info('Already got id. Using today id.')
            id = self.today_id
        elif id is None and self.today_id is None:
            logger.info('Did not got today id. getting it')
            self.get_id()
            id = self.today_id
        else:
            logger.info('Received {0} as id'.format(id))

        url = PRAC_URL.format(id)
        logger.debug('Practise url: {0}'.format(url))
        with urllib.request.urlopen(url) as k:
            i = k.read().decode()
        token_s = re.search(r'"form_token" value="(.+)"', i)
        form_build_id_s = re.search(r'"form_build_id" value="(.+)"', i)
        if token_s and form_build_id_s:
            token = token_s.group(1)
            build_id = form_build_id_s.group(1)
            logger.info('Token: {0}'.format(token))
            logger.info('Form Build ID: {0}'.format(build_id))
            return [token, build_id]
        else:
            logger.warn('Did not got token. Perhaps exercise is done or api has changed')
            return 0

    def take_exercise(self, answers=None, id=None, wrong=0):
        """
        take the exercise module
        will call get_tokens automatically
        required augments
        answers: accept a list as input.
        id: accept question id, default as today, please use the one reutrned
            by get_id()
        wrong: accept int, specify number of wrong answer.
            raise IndexError if that is out of boundary
        This will return save the answer as self.answers
        Will return the successful of attempt
        Known Bug: This cannot be used for typing question, which is quite rare
            to see
        """
        # Get exercise ID
        if id is None and self.today_id is not None:
            id = self.today_id
            logger.info('Already got id. Using today id.')
        elif id is None and self.today_id is None:
            logger.info('Did not got today id. getting it')
            self.get_id()
            id = self.today_id
        else:
            logger.info('Received {0} as id'.format(id))

        # build informations for taking questions
        exercise_done = self.is_exercise_done(id)
        if exercise_done == 0:
            logger.warn('Exercise is done')
            return False
        else:
            token = exercise_done[0]
            form_build_id = exercise_done[1]

        value = {'op': '開始練習', 'form_build_id': form_build_id,
                 'form_token': token, 'form_id': 'quiz_start_quiz_button_form'}
        url = EXER_URL.format(id.split(r'/')[0])
        logger.debug('Exercise url: {0}'.format(url))

        # First attempt, take total number of questions
        data = urllib.parse.urlencode(value).encode('utf-8')
        with urllib.request.urlopen(urllib.request.Request(url, data)) as k:
            c = k.read().decode()
        total_qs = int(re.search('"quiz-num-questions".+(\d+)<?', c).group(1))
        logger.info('Total question: {0}'.format(total_qs))
        value['op'] = '下一題'

        # Error check
        if wrong == 0:
            pass
        elif wrong-1 > total_qs:
            logger.error('Wrong number is larger than total question')
            raise IndexError
        if wrong != 0 and answers is None:
            logger.error('Assigned wrong number but did not gave answer')
            raise IndexError("Answer is None")
        if answers is not None:
            logger.info('Given answers: {0}'.format(answers))

        # looping questions
        for i in range(total_qs):
            logger.info('Looping {0} of {1}'.format(i, total_qs))
            try_ans = re.findall(r'"tries\[answer?]".+"(\d+)"', c)
            logger.info('try_ans: {0}'.format(try_ans))

            value['form_id'] = 'quiz_question_answering_form'
            # Change op to '遞交' when it is the last question
            if i == total_qs-1:
                value['op'] = '遞交'

            if answers is None:
                logger.info('Random mode')
                value[r'tries[answer]'] = try_ans[0]
            elif wrong == 0:
                logger.info('Answering the correct answer.')
                logger.info('The answer of this qs is {0}'.format(answers[i]))
                value[r'tries[answer]'] = try_ans[answers[i]]
            else:
                logger.info('Wrong mode')
                if answers[i] == 3:
                    logger.info('Answer is D. Changing to C')
                    value[r'tries[answer]'] = try_ans[i-1]
                else:
                    value[r'tries[answer]'] = try_ans[i+1]
                wrong -= 1
            # make request
            data = urllib.parse.urlencode(value).encode('utf-8')
            req = urllib.request.Request(url, data)
            with urllib.request.urlopen(req) as k:
                c = k.read().decode()

        if answers is None:
            # read for answers
            self.answers = answer_parser(c, total_qs)
            logger.info('Parsed answer: {0}'.format(self.answers))
        else:
            self.answers = answers
        return True

    def get_answers(self, id=None):
        # Get exercise ID
        if id is None and self.today_id is not None:
            id = self.today_id
            logger.info('Already got id. Using today id.')
        elif id is None and self.today_id is None:
            logger.info('Did not got today id. getting it')
            self.get_id()
            id = self.today_id
        else:
            logger.info('Received {0} as id'.format(id))

        real_id = id.split(r'/')[0]
        url = RESULT_URL.format(real_id)
        logger.debug('entry page url: {0}'.format(url))
        try:
            with urllib.request.urlopen(url) as k:
                raw = k.read().decode()
        except urllib.error.HTTPError as exc:
            logger.error('Received http error, {0}'.format(exc))
            return None

        # search for answer url
        ex_code = re.search(
            r'<td><a href="/zh-hant/node/\d+/myresults/(\d+)">更多...', raw)
        if not ex_code:
            logger.warn('Exercise is not done or api has changed')
            return None
        url = '/'.join([url, ex_code.group(1)])
        logger.debug('Result url: {0}'.format(url))
        with urllib.request.urlopen(url) as k:
            c = k.read().decode()

        search = re.search(
            r'<div id="quiz_score_possible">.*?(\d{1})</em>', c)
        total_qs = int(search.group(1))
        logger.info('total questions: {0}'.format(total_qs))
        answers = answer_parser(c, total_qs)
        logger.info('Answers: {0}'.format(answers))
        return answers


def answer_parser(c, total_qs):
    answers = []
    con_alph = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    raw = re.findall(r'This option is correct.+<td><?p?>?(\w)', c)
    for i in range(total_qs):
        ans = con_alph[raw[i]]
        answers.append(ans)
    return answers
