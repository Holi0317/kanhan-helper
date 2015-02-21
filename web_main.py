#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import module_api.kanhan_api
import json
import click
import getpass
import os
from random import randrange
import datetime


class App(object):
    def __init__(self):
        self.api = module_api.kanhan_api.kanhan_api()
        self.failed = False
        return

    def login(self, id, passwd, school_id):
        self.id = id
        if self.api.login(id, passwd, school_id):
            return
        else:
            self.failed = True
            return


@click.group()
def cli():
    pass


@cli.command()
@click.option('--sacrifice', default=None,
              help='specify one user to sacrifice by using the id')
def do_exercise(sacrifice):
    click.echo('Initializing...')
    path = os.path.join('data', 'web_data')
    if not os.path.isfile(path):
        click.echo('Web_data file not found')
        click.echo('Please Create one with add_user')
        exit(1)
    with open(path, 'r') as f:
        raw = f.read()
        login_data = json.loads(raw)
    object_list = [App() for i in range(len(login_data))]
    for i in range(len(object_list)):
        # Login
        current_obj = object_list[i]
        current_id = login_data[i][0]
        current_passwd = login_data[i][1]
        current_school_id = login_data[i][2]
        current_obj.login(current_id, current_passwd, current_school_id)
        if current_obj.failed:
            click.echo('{0} Failed to login'.format(current_obj.id))
            object_list.remove(current_obj)

    # Check answers
    today = datetime.date.today()
    path = os.path.join('data', str(today.year), str(today.month))
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, str(today.day))
    if os.path.isfile(path):
        with open(path) as f:
            raw = f.read()
        answer = json.loads(raw)[today.day]
        if sacrifice is None:
            click.echo('No need to sacrifice')
    else:
        if len(object_list) == 1:
            the_selected_one = object_list[0]
        elif sacrifice is not None:
            the_selected_one = None
            for i in object_list:
                if i.id == sacrifice:
                    the_selected_one = i
                    break
            if the_selected_one is None:
                click.echo("sacrificer is not in my list")
                click.echo("Randomly generating it")
                ran = randrange(0, len(object_list)-1)
                the_selected_one = object_list[ran]
        else:
            ran = randrange(0, len(object_list)-1)
            the_selected_one = object_list[ran]
        click.echo("Sacrificing {0} for todays answwer".format(
            the_selected_one.id))
        if not the_selected_one.api.take_exercise():
            click.echo("Failed, he has done his exercise")
            exit(1)
        answer = the_selected_one.api.answers
        dump(answer, path)

    # Answer question
    for i in range(len(object_list)):
        current_obj = object_list[i]
        ran = randrange(0, 2)
        if not current_obj.api.take_exercise(answers=answer, wrong=ran):
            click.echo("{0} has done his exercise".format(
                current_obj.id))
        else:
            click.echo("{0} succeed with {1} mistake(s)".fomrat(
                current_obj.id, ran))


@cli.command()
@click.option('--id', default=None, help='Account of user')
@click.option('--passwd', default=None, help='Password of user')
@click.option('--school_id', default=None, help='School ID of user')
def add_user(id, passwd, school_id):
    click.echo('Adding user...')
    if id is None:
        id = input("User's account: ")
    if passwd is None:
        passwd = getpass.getpass()
    if school_id is None:
        school_id = input("User's School ID: ")

    path = os.path.join('data', 'web_data')
    dump([id, passwd, school_id], path)


def dump(value, path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            raw = f.read()
        data = json.loads(raw)
    else:
        data = []
    data.append(value)
    data = json.dumps(data, sort_keys=True, indent=4)
    with open(path, 'w') as f:
        f.write(data)

if __name__ == '__main__':
    cli()
