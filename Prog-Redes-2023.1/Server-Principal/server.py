import socket, threading, os, sys, subprocess, platform, logging, logging.config

dir_atual = os.path.dirname(os.path.abspath(__file__))  # pegando a pasta atual
dir_arq =  os.path.abspath(__file__)
system = platform.system()
dir_pid = dir_atual + "\\pid.temp"
dir_logconf = dir_atual + "\\log.ini"
dir_log = dir_atual + "\\log_server.log"
dir_pastdownload = dir_atual + '\\server_files'

# ============================================================================================================

''' VERIFICAÇÃO SE TODOS OS ARQUIVOS/PASTAS DE FUNÇÕES ESTÃO PRESENTES '''

def VERIFICATION_FUNCTIONS():
    dir_past = dir_atual + '\\Functions-and-Variables'
    sys.path.append(dir_past) # adicionando a pasta de funções na config de pesquisa de funções do sistema
    name_arqs = [
        'functions_bot.py',
        'functions_client.py',
        'functions_others.py',
        'functions_server.py',
        'functions_download.py',
        'variables.py']
    try:
        functions_arq = os.listdir(dir_past) # listando arquivos da pasta onde está as funções para verificar se todos os arquivos necessários estão lá
        for arquivos in name_arqs: 
            if arquivos not in functions_arq: # vendo qual o arquivo que falta
                print(f'\nO Arquivo "{arquivos}" não está presente dentro da pasta "Functions and Variables" faça o download dele!\n')
                sys.exit()
    except SystemExit:
        sys.exit()
    except FileNotFoundError: # para caso a pasta não exista
        print('\nA pasta "Functions and Variables" não foi encontrada, faça o download dela [com todas suas dependencias]!\n')
        sys.exit()
    except:
        print(f'\nErro na Verificação dos arquivos da Pasta de Funções...{sys.exc_info()[0]}')  
        sys.exit() 

VERIFICATION_FUNCTIONS()

logging.config.fileConfig(dir_logconf, defaults={'log_path': dir_log.replace('\\', '\\\\')})
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.WARNING)
loggerServer  = logging.getLogger('Server')
loggerBot = logging.getLogger('BotTelegram')
loggerDebug = logging.getLogger('Debug')


from variables import SERVER, PORT
from functions_server import CLIENT_INTERACTION
from functions_others import CREATE_PAST, SEARCH_FILES
from functions_bot import START_BOT, NOTIFICATION_BOT

# ============================================================================================================

try: 

    ''' CRIAÇÃO THREAD BOT / CRIAÇÃO DO SERVER / CRIAÇÃO DE PASTA'''

    clients_connected = dict() # lista de clientes conectados (IP:PORTA)
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # conexão IPV4/TCP
    sock_tcp.bind((SERVER, PORT)) # atribuindo Porta e Local
    CREATE_PAST(dir_atual + '\\server_files') # criando pasta onde sera guardado arquivos do server
    loggerServer.info(f'Servidor Iniciado: {SERVER} / {PORT}')
    thread_bot = threading.Thread(target=START_BOT, args=(clients_connected,)) # adicionando a thread do bot (pois sem ela, eu não consegueria rodar o server e o bot ao mesmo tempo)
    thread_bot.start() # iniciando a thread do bot
    sock_tcp.listen() # deixando indefinido quantidade máxima de conexões

# ============================================================================================================

    ''' CONEXÃO DE CLIENTES / NOTIFICAÇÃO BOT / THREAD CLIENTE ''' 

    while True: 
        try:
            sock_client, info_client = sock_tcp.accept() # aceitando clientes 
            msg_connected = f"O Cliente de IP: {info_client[0]} | Na Porta: {info_client[1]}\nFoi conectado com sucesso!"
            loggerServer.info(msg_connected) # printando o cliente conectado
            NOTIFICATION_BOT(msg_connected) # enviando mensagem para o bot do cliente que se conectou
            clients_connected[info_client[1]] = [info_client[0], sock_client] # adicionando o cliente ao dicionario de clientes conectados (PORTA:IP,SOCKET)
            thread_client = threading.Thread(target=CLIENT_INTERACTION, args=(sock_client, info_client, clients_connected, dir_atual)) # adicionando uma thread para cada cliente
            thread_client.start() # iniciando a thread

# ============================================================================================================

        except:
            loggerServer.critical(f'\nErro na Inicialização da Thread...{sys.exc_info()[0]}')  
            sys.exit() 
            
except OSError as e: # exceção para quando a porta do servidor atual estiver ocupada
    if e.errno == 98:
        loggerServer.error('\nA porta atual do servidor se encontra ocupada\n')
        sys.exit()
except SystemExit:
    ...
except:
    loggerServer.critical(f'\nErro na Inicialização do Server...{sys.exc_info()}')  
    sys.exit() 

# ============================================================================================================




'''def PROCESS_RUNNER():
    if platform.system() == 'Windows':
        subprocess.Popen(["pythonw", "server.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif platform.system() == 'Linux':
        subprocess.Popen(["python", "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)

    with open(dir_pid, "w") as file:
        file.write(str(os.getpid()))
def VERIFICATION_PID(pid):
    if system == 'windows':
        process = subprocess.run(['Powershell', 'Get-Process', '-Id', pid], capture_output=True, text=True).stdout.strip()
    elif system == 'linux':
        process = subprocess.run(['ps', '-p', pid], capture_output=True, text=True).stdout.strip()
    if process:
        print(f'\nO Server já está sendo rodado em 2° Plano com o PID: {pid}\n')
        sys.exit()
    else:
        PROCESS_RUNNER()
    
def START():
    if os.path.isfile('pid.temp'):
        with open(dir_pid, 'r') as arquive:
            pid = arquive.readline().strip()
        VERIFICATION_PID(pid)
    else:
        PROCESS_RUNNER()'''