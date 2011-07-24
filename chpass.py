#!/usr/bin/env python
import subprocess

### Para mkpass
import random
import string
import time

### Para socket client: envpasswd
import socket
import sys

### Funcao destinada a gerar uma senha randomica
def mkpass(size=10):
    chars = []  
    chars.extend([i for i in string.ascii_letters])
    chars.extend([i for i in string.digits])
    chars.extend([i for i in '!@#$%&*()-_=+[{}]~^,<.>;:/?'])

    passwd = ''

    for i in range(size):
        passwd += chars[random.randint(0,  len(chars) - 1)]

        random.seed = int(time.time())
        random.shuffle(chars)

    return passwd


### Funcao destinada a trocar a senha
def chpass():
	login = 'teste'
	password = mkpass()
	hostname = socket.gethostname()

	print "Senha gerada: " + password + " para o host: " + hostname

	### Gera o hash da senha
	try:
		p = subprocess.Popen(('openssl', 'passwd', '-1', password), stdout=subprocess.PIPE)
		shadow_password = p.communicate()[0].strip()
	except:
		print 'Erro para hash de: ' + login

	### Altera a senha
	try:
		subprocess.call(('usermod', '-p', shadow_password, login))
	except:
    		print 'Erro alterando a senha de: ' + login

	return password

### Funcao destinada a enviar a senha trocada para o server via socket
def envpasswd():
	host = '192.168.1.5'
	porta = 50007
	hostname = socket.gethostname()

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, porta))
                pwd = chpass()
		mensagem = pwd + ' ' + hostname
                s.send(mensagem)
                data = s.recv(1024)
                s.close()
                print 'Senha trocada', data
	except:
		print 'Erro ao conectar com servidor: ' + host
		sys.exit()

envpasswd()
