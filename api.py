#!/usr/bin/env python3.8
# encoding: utf-8
import json
import paramiko
import time
import re
from flask import Flask, request, jsonify


def send_command(chan, command):
    chan.send(command + '\n')
    buff = ''
    while not (buff.endswith('> ') or buff.endswith('# ')):
        time.sleep(1)
        resp = chan.recv(9999)
        if len(resp) == 0:
            break
        buff += str(resp, 'UTF-8')
    # remove command from output
    buff = re.sub('^' + command + '\r\n', '', buff)
    # remove \r
    buff = re.sub('\r', '', buff)
    return buff


def get_config(username, password, hostname, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname, port, username, password)
    chan = client.invoke_shell()
    send_command(chan, 'set cli pager off')
    send_command(chan, 'set cli config-output-format set')
    send_command(chan, 'configure')
    config = send_command(chan, 'show')
    # remove last two lines from show output
    config = re.sub('\n[^\n]+\n[^\n]+$', '', config)
    send_command(chan, 'exit')
    send_command(chan, 'exit')
    client.close()
    return config


app = Flask(__name__)


@app.route('/', methods=['POST'])
def update_record():
    r = json.loads(request.data)
    for prop in ['username', 'password', 'hostname']:
        if prop not in r:
            return jsonify('Bad request')

    config = get_config(r['username'], r['password'], r['hostname'])
    return jsonify(config)


app.run(debug=True)
