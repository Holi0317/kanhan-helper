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
import logging


home_dir = os.path.expanduser('~')
base = os.path.join(home_dir, '.khh')

# Logging module initialize
# Create diretory
path = os.path.join(base, 'log')
if not os.path.exists(path):
    os.makedirs(path)
path = os.path.join(path, 'web.log')
# setup logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# setup file handler and set level to debug
file_handler = logging.FileHandler(path)
file_handler.setLevel(logging.DEBUG)
# setup console handler and set level to error
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
# create and install formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
# add handler to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


@click.group()
def cli():
    pass


@cli.command()
def main():
    # Initial variables
    logger.info('================= Running main() ==========================')
    logger.debug('Base dir is {0}'.format(base))
    api = khh.khhapi.kanhan_api()
    failed = 0

    # Read json file
    path = os.path.join(base, 'web_data.json')
    if not os.path.isfile(path):
        logger.error('{0} Not found'.format(path))
        logger.error('Please Create one with add_user')
        exit(1)
    with open(path, 'r') as f:
        raw = f.read()
    login_data = json.loads(raw)
    logger.debug('Login data is {0}'.format(login_data))
    logger.info('There are {0} users in the file'.format(len(login_data)))

    # Check answer
    today = datetime.date.today()
    file_name = str(today.day) + '.json'
    path = os.path.join(base, str(today.year), str(today.month), file_name)
    logger.debug("The path of today's answer is {0}".format(path))
    if os.path.isfile(path):
        logger.info('Answer found')
        with open(path, 'r') as f:
            raw = f.read()
        answer = json.loads(raw)
        logger.info('Today answer is {0}'.format(answer))
        need_sacrifice = False
    else:
        logger.info('Answer not found')
        need_sacrifice = True

    # Main loop
    for i in range(len(login_data)):
        api.__init__()
        current_id = login_data[i][0]
        current_passwd = login_data[i][1]
        current_school_id = login_data[i][2]
        login_attempt = api.login(current_id, current_passwd, current_school_id)

        if not login_attempt:
            logger.warn('{0} failed to login'.format(current_id))
            failed += 1
            continue

        logger.info('{0} Login succeed'.format(current_id))

        # Get id
        id = api.get_id()
        logger.info("Today id is {0}".format(id))
        if id is None:
            logger.error('Today has no exercise')
            exit(1)

        # Sacrifice
        if i == 0 and need_sacrifice:
            logger.info('Sacrificer: {0}'.format(current_id))
            exercise_result = api.take_exercise()
            if exercise_result:
                logger.info("Sacrificer exercise done")
                answer = api.get_answers()
            else:
                answer = api.answers
            logger.debug('Answer: {0}'.format(answer))

            # Dump to data
            logger.info('Dumping answers to data')
            path = os.path.join(base, str(today.year), str(today.month))
            file_name = str(today.day) + '.json'
            logger.debug('Path to answer: {0}'.format(path))
            if not os.path.exists(path):
                logger.info('Path not exist')
                os.makedirs(path)
            path = os.path.join(path, file_name)
            dump_data = json.dumps(answer, sort_keys=True, indent=4)
            with open(path, 'w') as f:
                f.write(dump_data)
            need_sacrifice = False
            continue

        # Answering question for others
        if not need_sacrifice:
            ran = randrange(0, 3)
            exercise_result = api.take_exercise(answers=answer, wrong=ran)
            if exercise_result:
                logger.info('{0} Succeed to complete with {1} wrong answer'.format(current_id, ran))
            else:
                logger.info('{0} already completed his exercise'.format(current_id))

    # Loop ended
    if failed != 0:
        logger.warn('{0} of {1} failed to login'.format(failed, len(login_data)))
    return


@cli.command()
@click.option('--id', '-i', help='Account of user', prompt='ID')
@click.option('--passwd', '-p', help='Password of user', hide_input=True,
              prompt='Password')
@click.option('--school_id', '-s', help='School ID of user', prompt='School id')
def add_user(id, passwd, school_id):
    # Logging
    logger.info('==========Running add_user()======================')
    logger.info('Base dir: {0}'.format(base))

    click.echo('Adding user...')
    path = os.path.join(base, 'web_data.json')
    logger.info('web_data path: {0}'.format(path))
    if sys.platform.startswith('linux'):
        logger.info('System platform is linux')
        os.chmod(path, 0o600)

    # Dump
    if not os.path.exists(base):
        logger.info('Base does not exist')
        os.makedirs(base)
    if os.path.isfile(path):
        with open(path, 'r') as f:
            raw = f.read()
        data = json.loads(raw)
    else:
        data = []
    logger.info('Loaded data: {0}'.format(data))
    data.append([id, passwd, school_id])
    json_dump = json.dumps(data, sort_keys=True, indent=4)
    with open(path, 'w') as f:
        f.write(json_dump)

    if sys.platform.startswith('linux'):
        os.chmod(path, 0o400)
    click.echo('Done')
