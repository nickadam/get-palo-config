import paramiko
import time
import os
import sys

USERNAME = sys.argv[1]
HOSTNAME = sys.argv[2]
PASSWORD = os.environ.get('PASSWORD')
PORT = 22

def send_get_output(chan, command):
    chan.send(command + '\n')
    buff = ''
    while not (buff.endswith('> ') or buff.endswith('# ')):
        time.sleep(1)
        resp = chan.recv(9999)
        if len(resp) == 0:
            break
        buff += str(resp, 'UTF-8')
    return buff

def get_config(username=USERNAME, password=PASSWORD, hostname=HOSTNAME, port=PORT):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname, port, username, password)
    chan = client.invoke_shell()
    send_get_output(chan, 'set cli pager off')
    send_get_output(chan, 'set cli config-output-format set')
    send_get_output(chan, 'configure')
    print(send_get_output(chan, 'show'))
    send_get_output(chan, 'exit')
    send_get_output(chan, 'exit')
    client.close()

if __name__ == '__main__':
    get_config()
