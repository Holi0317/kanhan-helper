#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import kanhan_api
import json
import datetime
import click
import os
import sys.platform


@click.group()
def cli():
    pass


@cli.command()
@click.option('--day', '-d', default=None, help='The target day of exercise')
@click.option('--month', '-m', default=None,
              help='The target Month of exercise')
@click.option('--year', '-y', default=None, help='The target year of exercise')
def main(day, month, year):
    api = kanhan_api.kanhan_api()
    login(api)

    # Option formatter
    today = datetime.date.today()
    if day is None and month is None and year is None:
        date = today
    else:
        if day is not None:
            date = today.replace(day=day)
        if month is not None:
            date = today.replace(month=month)
        if year is not None:
            date = today.replace(year=year)

    # Gathering informations
    id = api.get_id(date)
    if id is None:
        click.echo("No exercise on that day")
        exit(1)

    # Answering section
    click.echo("Checking if there is any answer...")
    path = os.path.join('data', str(date.year), str(date.month),
                        str(date.day))
    if os.path.isfile(path):
        click.echo("Found answer. Filling it in...")
        with open(path, 'r') as f:
            raw = f.read()
        answer = json.loads(raw)
        exercise_result = api.take_exercise(id=id, answers=answer)
    else:
        click.echo("Answer not found. Randomly filling answers...")
        exercise_result = api.take_exercise(id=id)
    if exercise_result:
        click.echo("Done!")
    else:
        click.echo("You have already done that day's exercise")
        exit(1)

    if not os.path.isfile(path):
        click.echo("Dumping answers to data...")
        dump(api.answers)
        click.echo("Done!")
    exit(0)


@cli.command()
@click.option('--id',  '-d', help='Account of user', prompt='Your id: ')
@click.option('--passwd', '-p', help='Password of user', hide_input=True,
              prompt='(This input will be hidden) Your password: ')
@click.option('--school_id', '-s', help='School ID of user',
              prompt='Your school id: ')
def add_user(id, passwd, school_id):
    click.echo('Adding user...')
    path = os.path.join('data', 'account')
    data = [id, passwd, school_id]
    data = json.dumps(data, sort_keys=True, indent=4)
    with open(path, 'w') as f:
        f.write(data)
    click.echo("Done")

    if sys.platform.startswith('linux'):
        click.echo("Thank you for supporting open source, using GNU/Linux")
        click.echo("Changing permission to 400 for secutity")
        os.chmod(path, 0o400)


@cli.command()
@click.option('--day', '-d', default=None, help='The target day of exercise')
@click.option('--month', '-m', default=None,
              help='The target Month of exercise')
@click.option('--year', '-y', default=None, help='The target year of exercise')
def get_answer(day, month, year):
    api = kanhan_api.kanhan_api()
    login(api)

    # date format module
    today = datetime.date.today()
    if day is None and month is None and year is None:
        date = today
    else:
        if day is not None:
            date = today.replace(day=day)
        if month is not None:
            date = today.replace(month=month)
        if year is not None:
            date = today.replace(year=year)

    id = api.get_id(date=date)
    click.echo("Getting answer for {0}".format(day))
    ans = api.get_answers(id=id)
    if ans is None:
        click.echo("You have not done that day's exercise")
        exit(1)
    dump(ans)
    exit(0)


def login(api):
    path = os.path.join('data', 'account')
    if os.path.isfile(path):
        with open(path, 'r', encoding='UTF-8') as f:
            account = f.readline()
            pwd = f.readline()
            school_id = f.readline()
            use_file_to_login = True
    else:
        use_file_to_login = False

    click.echo('Logging in...')
    if not use_file_to_login:
        account = click.prompt('User Name: ')
        pwd = click.prompt('Password: ', hide_input=True)
        school_id = click.prompt('school ID: ')
    else:
        click.echo("Account file found! Using it to login")

    try:
        login_attempt = api.login(account, pwd, school_id)
    except:
        click.echo("Login Failed!")
        exit(1)
    if login_attempt:
        click.echo("Login Success!")
    else:
        click.echo("Login Failed")
        exit(1)


def dump(target):
    today = datetime.date.today()
    path = os.path.join('data', str(today.year), str(today.month),
                        str(today.day))
    if not path.exists:
        os.path.makedirs(path)
    ans = json.dumps(target, sort_keys=True, indent=4)
    with open(path, 'w') as f:
        f.write(ans)
    return


if __name__ == '__main__':
    cli()
