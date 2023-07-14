
def PRINT_DIV(dados):
    print('\n'+'-'*100)
    print(dados)
    print('-'*100)

def COMAND_SPLIT(msg):
    try:
        msg_split = msg.split(':')
    except:
        print(f'\nErro no Split do Comand...{sys.exc_info()[0]}')  
        exit() 
    return msg_split

def QUIT(clients_connected, sock_client, info_client):
    msg = f"\nVocê será desconectado, volte sempre!\n"
    sock.send(msg.encode(UNICODE))
    del clients_connected[info_client[1]] # quando o cliente digitar /q ele exclui socket do cliente da lista de clientes ativos
    sock_client.close()