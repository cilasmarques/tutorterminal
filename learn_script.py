#!/usr/bin/python3
import os
import re
import shlex
import subprocess
import sys


try:
    from ansimarkup import parse, ansiprint
except:
    ansiprint = lambda x: print(re.sub('<.*?>', '', x))


script = open(sys.argv[1]).readlines()

help_txt = []
expect = ''


def checkfile(fname, exists=True):
    if exists ^ os.path.exists(content):
        ansiprint("<fg red> Arquivo/diretório " + ('inexistente' if exists else 'existente') + ": " + content + ". Procure por ajuda.")
        return False
    return True


def prompt():
    ansiprint("<bold><green>[In]</green></bold> <light-blue>" + os.path.abspath('.') + "</light-blue>$ ", end='')


def query_user(content):
    fancy_input = lambda : prompt() or input()
    user_input = fancy_input()
    while not user_input:
        ansiprint("Comando nao pode ser vazio.")
        user_input = fancy_input()
    while not re.match(content, user_input):
        ansiprint("<fg red>Certeza que deseja continuar? A entrada parece ser diferente do indicado.</fg red> <bold>[s/N]</bold> ", end="")
        user_test = input()
        if user_test == "n" or not user_test:
            user_input = fancy_input()
        else:
            break
    return user_input


def enter():
    ansiprint('<bold><white>Aperte ENTER para continuar...</white></bold>')
    input()


def run_command(content, free=False, auto=False):
    user_input = content
    if auto:
        prompt()
        ansiprint(content)
    else:
        user_input = query_user(content)
    output = "<bold><red>[Out]</red></bold> "
    if free:
        process = subprocess.Popen(user_input, shell=True)
    else:
        process = subprocess.Popen(shlex.split(user_input), shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.stdin.write(user_input.encode('utf-8') + b'\n')
        for line in process.stdout.readlines():
            ansiprint(output + line.decode('utf-8'), end='')
    process.wait()
    if process.returncode != 0:
        ansiprint("Algo parece ter dado errado... procure por ajuda ou verifique os comandos executados.")
        return False
    return True


processing = ''
tmp_processing = ''

for line in script:
    if processing:
        if line.strip() == "###":
            open(processing, 'w').write(tmp_processing)
            processing = ''
            tmp_processing = []
        tmp_processing += line
        continue

    if not line.strip():
        continue

    line = line.strip()

    if ' ' not in line:
        line += ' '

    command, content = line.split(' ', 1)
    content = content.strip()

    if command == '!checkfile':  # checkfile not exists
        if not checkfile(content, False):
            break
    if command == 'checkfile':  # checkfile
        if not checkfile(content):
            break
    if command == '##':
        ansiprint(content)
        help_txt.append(content)
    if command == '#':
        ansiprint(content)
    if command == 'enter':
        enter()
    if command == 'run_free':
        if not run_command(content, free=True):
            break
    if command == 'run':
        if not run_command(content):
            break
    if command == 'run_auto':
        if not run_command(content, auto=True):
            break
    if command == '###':
        processing = content