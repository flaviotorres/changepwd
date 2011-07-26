#!/usr/bin/env python
import subprocess
import MySQLdb

### Para mkpass
import random
import string
import time

### Para socket client: envpasswd
import socket
import sys
import os

def main():
	if os.geteuid() != 0:
		print "Este programa precisa de privilegio root para ser executado."
		sys.exit()
	else:
		chpass()		

### Funcao destinada a gerar uma senha randomica
def mkpass(size=10):
    chars = []  
    chars.extend([i for i in string.ascii_letters])
    chars.extend([i for i in string.digits])
    chars.extend([i for i in '!@#$%&*()-_=+[{}]~^,<.>;:/?'])

    passwd = ''

    for i in range(size):
        passwd += random.choice(chars) 

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
                db = MySQLdb.connect(host="192.168.122.209",user="user-chpasswd", passwd="chpasswd", db="chpasswd")
                cursor = db.cursor()
                #cursor.execute("UPDATE dados SET senha = AES_ENCRYPT('" + password + "', 'key123') where host='" + host + "';")
		cursor.execute("INSERT INTO dados (host, senha) VALUES('" + hostname + "', AES_ENCRYPT('" + password + "', 'key123') ) ON DUPLICATE KEY UPDATE senha = AES_ENCRYPT('" + password + "', 'key123');")

		# Altera a senha
		subprocess.call(('usermod', '-p', shadow_password, login))
		print "usuario: %s teve sua senha alterada para: %s" %(login, password)

        except MySQLdb.OperationalError, message:
		print "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
                sys.exit()


if __name__ == "__main__":
	main()
