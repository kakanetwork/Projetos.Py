import socket
from functions_others import *

def connection():
    ...

def LIST_CLIENTS(clients_connected):
    for chave, valor in clients_connected.items():
        ip = valor[0]
        msg = f"IP: {ip}\nPORT: {chave}"

def OPTIONS():
    opções_descritivas = {
        '/l': 'Realizar Pull do GitHub'
        }
    
def CLIENT_INTERACTION(sock_client, info_client, clients_connected):
    print('oiii')
    msg = b'' # definindo uma mensagem binária
    while msg != b'/q': # o while 
        try:
            opções = {'/l': LIST_CLIENTS(clients_connected)}
            msg = sock_client.recv(512) 
            for msg in opções:
                opções[msg]()
            broadCast (msg, info_client)
        except:
            msg = b'/q'
    del clients_connected[info_client[1]]
    sock_client.close()
    return msg

def broadCast(msg, addrSource):
    msg = f"{addrSource} -> {msg.decode('utf-8')}"
    PRINT_DIV(msg)
    for sockConn, addr in clients_connected:
        if addr != addrSource:
            sockConn.send(msg.encode('utf-8'))