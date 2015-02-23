#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

import kanhan_api
import getpass
import json
import datetime
import click
import os


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        main()
    elif ctx.invoked_subcommand == 'add_user':
        add_user()
    elif ctx.invoked_subcommand == 'get_answer':
        get_answer


def main():
    api = kanhan_api.kanhan_api()
    login(api)

    # answering section
    click.echo("Randomly filling answers...")
    api.get_id()

    # TODO: allow user to change target_id
    exercise_result = api.take_exercise()
    if exercise_result:
        click.echo("Done!")
    else:
        click.echo("You have already done that day's exercise")
        exit(1)

    dump(api.answers)
    exit(0)


@cli.command()
@click.option('--id',  '-d', default=None, help='Account of user')
@click.option('--passwd', '-p', default=None, help='Password of user')
@click.option('--school_id', '-s', default=None, help='School ID of user')
def add_user(id, passwd, school_id):
    click.echo('Adding user...')
    if id is None:
        id = input("User's account: ")
    if passwd is None:
        passwd = getpass.getpass()
    if school_id is None:
        school_id = input("User's School ID: ")

    path = os.path.join('data', 'account')
    data = [id, passwd, school_id]
    data = json.dumps(data, sort_keys=True, indent=4)
    with open(path, 'w') as f:
        f.write(data)


@cli.command()
@click.option('--day', '-d', default=None, help='Date of the exercise')
def get_answer(day):
    api = kanhan_api.kanhan_api()
    login(api)
    if day is None:
        id = api.get_id()
        day = datetime.date.today().day
    else:
        id = api.get_id(day=day)
    click.echo("Getting answer for {0}".format(day))
    ans = api.get_answers(id=id)
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
        account = input('User Name: ')
        pwd = getpass.getpass()
        school_id = input('School ID: ')
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
    ans = json.dumps(target, sort_keys=True, indent=4)
    with open(path, 'w') as f:
        f.write(ans)
    return


if __name__ == '__main__':
    cli()
