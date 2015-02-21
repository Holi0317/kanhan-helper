#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import module_api.kanhan_api
import getpass
import json
import datetime


class App(object):
    """
    Main object for the ui
    """
    def __init__(self):
        self.api = module_api.kanhan_api.kanhan_api()
        self.today_answer = None
        self.target_id = None
        return

    def login(self):
        try:
            with open('data/account', 'r', encoding='UTF-8') as f:
                account = f.readline()
                pwd = f.readline()
                school_id = f.readline()
                use_file_to_login = True
        except FileNotFoundError:
            use_file_to_login = False

        print('Logging in...')
        if not use_file_to_login:
            account = input('User Name: ')
            pwd = getpass.getpass()
            school_id = input('School ID: ')
        else:
            print("Account file found! Using it to login")

        try:
            login_attempt = self.api.login(account, pwd, school_id)
        except:
            print("Login Failed!")
        if login_attempt:
            print("Login Success!")
            return True
        else:
            print("Login Failed")

        print("Would you like to retry? (Y/n)")
        rec = rec_yes()
        if rec:
            self.login()
        else:
            return False

    def do_exercise(self):
        print("Randomly filling answers...")
        self.api.get_id()
        self.target_id = self.api.today_id
        exercise_result = self.api.take_exercise()
        if exercise_result:
            print("Done!")
        else:
            print("You have already done today's exercise")
            return
        self.dump()
        return

    def dump(self):
        month = datetime.date.today().month
        filename = '/'.join(['data', str(month)])
        ans = json.dumps(self.api.answers, sort_keys=True, indent=4)
        with open(filename, 'w') as f:
            f.write(ans)
        return


def rec_yes(default=True):
    """
    Read user true/false input handler
    """
    while True:
        i = input()
        if i == 'y' or i == 'Y' or i == 'yes':
            return True
        elif i == 'n' or i == 'N' or i == 'no':
            return False
        elif i == '':
            return default
        else:
            print('invaild option')


def main():
    app = App()
    if app.login():
        app.do_exercise()

if __name__ == '__main__':
    main()
