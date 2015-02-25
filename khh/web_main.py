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


@click.group()
def cli():
    pass


@cli.command()
def main():
    api = khh.khhapi.kanhan_api()
    # Read json file
    path = os.path.join('data', 'web_data')
    if not os.path.isfile(path):
        click.echo('Web_data file not found')
        click.echo('Please Create one with add_user')
        exit(1)
    with open(path, 'r') as f:
        raw = f.read()
    login_data = json.loads(raw)

    # Check answer
    today = datetime.date.today()
    path = os.path.join('data', str(today.year), str(today.month), str(today.day))
    if os.path.isfile(path):
        click.echo('Found answer')
        with open(path, 'r') as f:
            raw = f.read()
        answer = json.loads(raw)
        need_sacrifice = False
    else:
        need_sacrifice = True

    # Main loop
    for i in range(len(login_data)):
        api.__init__()
        current_id = login_data[i][0]
        current_passwd = login_data[i][1]
        current_school_id = login_data[i][2]
        try:
            login_attempt = api.login(current_id, current_passwd, current_school_id)
        except:
            failed = True
        if login_attempt:
            failed = False
        else:
            failed = True
        if failed:
            click.echo('{0} failed to login'.format(current_id))
        else:
            click.echo('{0} Login succeed'.format(current_id))

            # Get id
            id = api.get_id()
            if id is None:
                click.echo('Today has no exercise')
                exit(1)

            # Sacrifice
            if need_sacrifice and i == 0:
                click.echo('Sacrificing {0} for answer'.format(current_id))
                exercise_result = api.take_exercise()
                if exercise_result:
                    click.echo("He has done today's exercise. getting the answer...")
                    answer = api.get_answers()
                else:
                    answer = api.answers

                # Dump to data
                click.echo('Dumping answers to data')
                path = os.path.join('data', str(today.year), str(today.month))
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, str(date.day))
                dump_data = json.dumps(answer, sort_keys=True, indent=4)
                with open(path, 'w') as f:
                    f.write(dump_data)
                need_sacrifice = False

            # Answering question for others
            if not need_sacrifice:
                ran = randrange(0,2)
                exercise_result = api.take_exercise(answers=answer, wrong=ran)
                if exercise_result:
                    click.echo('{0} Succeed'.format(current_id))
                else:
                    click.echo('{0} Have finished his exercise'.format(current_id))

    return


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
    # Dump
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

    if sys.platform.startswith('linux'):
        os.chmod(path, 0o400)
    click.echo('Done')


