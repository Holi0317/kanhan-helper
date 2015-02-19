#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import module_api.kanhan_api
import getpass
import os
import json


class App(object):
    """
    Main object for the ui
    """
    def __init__(self):
        self.api = module_api.kanhan_api.kanhan_api()
        self.is_logined = False
        self.today_answer = None
        self.target_id = None
        return

    def main_menu(self):
        clear()
        print('* * * Chinese Kanhan Command line interface * * *')
        print('Welcome, user!')
        print('Main menu:')
        print('[ 1 ] Login')
        print('[ 2 ] Do today exercise')
        print('[ 3 ] Do other exercise')
        print('[ 4 ] Share answers with others')
        print('[ 0 ] Exit')
        print()
        i = rec_input(4)
        if i == '1':
            self.login()
        elif i == '2':
            self.do_exercise()
        elif i == '3':
            self.select_exercise()
        elif i == '4':
            self.share()
        elif i == '0':
            clear()
            exit()
        return

    def login(self):
        os.chdir('data')
        try:
            with open('account', 'r', encoding='UTF-8') as f:
                account = f.readline()
                pwd = f.readline()
                school_id = f.readline()
                use_file_to_login = True
        except FileNotFoundError:
            use_file_to_login = False

        logouted = False
        if self.is_logined:
            print('Logging Out...')
            self.api.__init__()
            self.__init__()
            logouted = True
        print('Logging in...')
        if not use_file_to_login:
            account = input('User Name: ')
            pwd = getpass.getpass()
            school_id = input('School ID: ')
        elif logouted:
            account = input('User Name: ')
            pwd = getpass.getpass()
            school_id = input('School ID: ')
        else:
            print("Account file found! Using it to login")

        try:
            login_attempt = self.api.login(account, pwd, school_id)
        except:
            print("Login Failed!")
            failed = True
        if login_attempt:
            print("Login Success!")
            self.is_logined = True
            return
        else:
            print("Login Failed")
            failed = True

        if failed:
            print("Would you like to retry? (Y/n)")
            rec = rec_yes()
            if rec:
                self.login()
            else:
                return
        return

    def do_exercise(self):
        if not self.is_logined:
            print("You have not logined")
            print("Would you like to login? (Y/n)")
            rec = rec_yes()
            if rec:
                self.login()
            else:
                return

        print("Connecting to server for today's answer...")
        got_answer = self.get_answer()
        if got_answer:
            print("Got today answers")
            print("Would you like to do it now? (Y/n)")
            rec = rec_yes()
            if rec:
                print("Doing exercise...")
            else:
                return
        else:
            print("No one has done today's exercise yet")
            print("Would you like to contribute? (Y/n)")
            rec = rec_yes()
            if rec:
                print("Randomly filling answers...")
            else:
                return

        self.api.get_id()
        self.target_id = self.api.today_id
        if got_answer:
            exercise_result = self.api.take_exercise(answers=self.today_answer)
        else:
            exercise_result = self.api.take_exercise()
        if exercise_result:
            print("Done!")
        else:
            print("You have done today's exercise")
            return
        if not got_answer:
            print("Would you like to share your answer? (Y/n)")
            rec = rec_yes()
            if rec:
                self.dump()
        return

    def get_answer(self):
        """
        Connect to server for today's answer
        return a bool for successful
        store answer in self.today_answer
        """
        return False

    def dump(self):
        os.chdir('data')
        ans = json.dumps(self.api.answers, sort_keys=True, indent=4)
        with open(self.target_id, 'w') as f:
            f.write(ans)
        return

    def select_exercise(self):
        return

    def share(self):
        print("[ Debug ] Input the answer")
        ans = [1, 0, 2, 2, 3]
        dump = json.dumps(ans, sort_keys=True, indent=4)
        with open('debug', 'w') as f:
            f.write(dump)
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


def rec_input(maximum):
    """
    Read user input handler
    """
    while True:
        i = input('>>>')
        if i == 'q' or i == 'Q':
            return '0'
        elif i.isdigit() and int(i) <= maximum:
            return i
        elif i.isdigit():
            print('Inupt is out of boundary')
        else:
            print('Incorrect option')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    app = App()
    while True:
        app.main_menu()

if __name__ == '__main__':
    main()
