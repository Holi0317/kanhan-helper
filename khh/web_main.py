#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import khh.khhapi
import json
import click
import os
from random import randrange
import datetime
import sys


class App(object):
    def __init__(self):
        self.api = khh.khhapi.kanhan_api()
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
def main(sacrifice):
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
    remove_list = []
    for i in range(len(object_list)):
        # Login
        current_obj = object_list[i]
        current_id = login_data[i][0]
        current_passwd = login_data[i][1]
        current_school_id = login_data[i][2]
        current_obj.login(current_id, current_passwd, current_school_id)
        if current_obj.failed:
            click.echo('{0} Failed to login'.format(current_obj.id))
            remove_list.append(current_obj)

    # Remove failed object
    for i in remove_list:
        object_list.remove(i)

    # Check answers
    today = datetime.date.today()
    path = os.path.join('data', str(today.year), str(today.month))
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, str(today.day))
    if os.path.isfile(path):
        with open(path) as f:
            raw = f.read()
        answer = json.loads(raw)
        if sacrifice is None:
            click.echo('No need to sacrifice')
    else:
        # Sacrifice
        if len(object_list) == 1:
            the_selected_one = object_list[0]
        elif sacrifice is not None:
            # select to sacrifice module
            the_selected_one = None
            for i in len(object_list):
                current_obj = object_list[i]
                if current_obj.id == sacrifice:
                    the_selected_one = object_list.pop(i)
                    break
            if the_selected_one is None:
                # pargment is not in the list
                click.echo("Wrong pargment. Could not find sacrificer")
                exit(1)
        else:
            ran = randrange(0, len(object_list)-1)
            the_selected_one = object_list.pop(ran)
        click.echo("Sacrificing {0} for todays answwer".format(
            the_selected_one.id))

        do_return = the_selected_one.api.take_exercise()
        if do_return:
            click.echo("Successfuly sacrificed")
            answer = the_selected_one.api.answers
        else:
            click.echo("He has done his exercise. getting answer")
            answer = the_selected_one.api.get_answers()
            if answer is None:
                click.echo('No exercise today')
                exit(1)

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
@click.option('--id', '-i', help='Account of user', prompt='ID')
@click.option('--passwd', '-p', help='Password of user', hide_input=True,
              prompt='Password')
@click.option('--school_id', '-s', help='School ID of user', prompt='School id')
def add_user(id, passwd, school_id):
    click.echo('Adding user...')
    path = os.path.join('data', 'web_data')
    if sys.platform.startswith('linux'):
        os.chmod(path, 0o600)
    dump([id, passwd, school_id], path)
    if sys.platform.startswith('linux'):
        os.chmod(path, 0o400)
    click.echo('Done')


def dump(value, path):
    if not os.path.exists('data'):
        os.makedirs('data')
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
    return
