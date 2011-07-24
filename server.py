import socket
import sys
import commands
import MySQLdb
from pyparsing import commaSeparatedList, Word, alphas

host = ''
porta = 50007
rede_valida = '127.0.0.1'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, porta))
s.listen(1)

def acl():
	tmp = addr[0].find(rede_valida)
	if tmp == 0:
        	print 'Rede valida - OK'
		return 1
	else:
        	print 'Recebi tentativa de uma Rede invalida', addr[0]
		return 0

def grava(data):
	
	parts = data.split(" ")
	senha = parts[0]
	host = parts[1]
	db = MySQLdb.connect(host="IP_SERVIDOR_DB",user="USUARIO", passwd="SENHA", db="DATABASE")
	cursor = db.cursor()
	cursor.execute("UPDATE dados SET senha = AES_ENCRYPT('"+senha+"', 'key123') where host='"+host+"';")
	#cursor.execute("SELECT host, AES_DECRYPT(senha,'key123') FROM dados where host='"+host+"';")
	#result = cursor.fetchall()
	#for record in result:  print record[0] , "-->", record[1]

while 1:
	conn, addr = s.accept()
	data = conn.recv(1024)
	if not data:
		break
	acl()
	if data:
		print 'Recebi os dados do cliente: %s' % data
		conn.send(data)
		grava(data)
	conn.close()
