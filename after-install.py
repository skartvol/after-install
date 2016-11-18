#!/usr/bin/env python3
# -*-coding: utf-8 -*-
__author__ = 'Yatskanych Oleksandr'
import getpass
import os


def install(file):
    file_data = open(file)
    line = file_data.readline()
    while line:
        if line.strip() != '' and line[0] != '#':
            os.system(line)
        line = file_data.readline()
    file_data.close()


def ssh_generator():
    email = input('Enter e-mail for ssh-key:')
    if email == '':
        ssh_generator()

    os.system('ssh-keygen -t rsa -C "{0}"'.format(email))
    os.system('xclip -sel clip < ~/.ssh/id_rsa.pub')
    print('Key copy to clipboard...')


def install_soft():
    install('soft.txt')


def change_apache_user(user_name):
    with open('/etc/apache2/envvars', 'r') as f:
        data = f.read()
        new_data = data.replace('www-data', user_name)

    with open('/tmp/env.tmp', 'wt') as n:
        n.write(new_data)

    os.system('sudo mv /tmp/env.tmp /etc/apache2/envvars')


def make_www_in_home(user_name):
    os.system('sudo cp /etc/apache2/apache2.conf /tmp/apache_conf.tmp')

    with open('/tmp/apache_conf.tmp', 'wt') as new_apache_conf:
        conf = '<Directory /home/{username}/www/>\n'.format(username=user_name)
        conf += '\tOptions Indexes FollowSymLinks\n'
        conf += '\tAllowOverride All\n'
        conf += '\tRequire all granted\n'
        conf += '</Directory>'
        new_apache_conf.write(conf)

    os.system('sudo mv /tmp/apache_conf.tmp /etc/apache2/apache2.conf')


if __name__ == "__main__":
    install('commands.txt')

    ss = input('Generate SSH key (y/n):')
    if ss == 'y':
        ssh_generator()

    ch = input('Install other soft (y/n):')
    if ch == 'y':
        install_soft()

    user_name = getpass.getuser()
    mess = 'Run apache with current user {0} (y/n):'.format(user_name)

    uc = input(mess)
    if uc == 'y':
        change_apache_user(user_name)
    
    mess = 'Make www dir in {username} home folder? (y/n):'.format(username=user_name)
    user_choice = input(mess)
    if user_choice == 'y':
        make_www_in_home(user_name)
