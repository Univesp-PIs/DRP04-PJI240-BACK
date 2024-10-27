import os
import datetime
import inspect
import logging

class MyLogger:
    def __init__(self):
        # Variáveis gerais
        self.status = False
        self.sucesso = f'SUCESSO - {__name__}'
        self.falha = f'FALHA - {__name__}'
        self.erro = f'ERRO - {__name__}'

        # Variáveis específicas
        self.pasta_log_name = 'logs'
        self.nome_plataforma = 'engsol'
        self.logger = None
        self.pasta_log_path = None
        self.subpasta_log_path = None
        self.nome_log = None
        self.arquivo_log_path = None
        self.nome_arquivo = None

        # Variáveis de data
        self.data_atual = datetime.datetime.now().strftime('%d-%m-%Y')
        self.hora_atual = datetime.datetime.now().strftime('%H-%M-%S')
        self.data_hora = datetime.datetime.now().strftime('%Y-%m-%d - %H-%M-%S')

        # Funções nativas
        self.configurar_log()

    # Função para realizar criação das pastas e arquivos do log
    def criar_log(self):

        try:

            # Obtem o diretorio do projeto
            dir_path = os.path.dirname(os.path.realpath(__name__))

            # Cria o caminho para a pasta de log
            self.pasta_log_path = os.path.join(dir_path, self.pasta_log_name)

            # Criação da pasta de log e subpasta de data
            if not os.path.exists(self.pasta_log_path):
                os.makedirs(self.pasta_log_path)

            # Criar caminho da subpasta
            self.subpasta_log_path = os.path.join(self.pasta_log_path, self.data_atual)

            # Criar subpasta
            if not os.path.exists(self.subpasta_log_path):
                os.makedirs(self.subpasta_log_path)

            # Cria o nome do arquivo de log
            self.nome_log = self.data_atual + '.log'
            self.arquivo_log_path = os.path.join(self.subpasta_log_path, self.nome_log)

            # Criar arquivo
            if not os.path.exists(self.arquivo_log_path):
                # Mensagem inicial do log
                mensagem = 'Log criado com sucesso.'
                with open(self.arquivo_log_path, 'a') as arquivo_log:
                    arquivo_log.write(f'[{self.data_hora}] - ' + mensagem + '\n')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao criar as pastas e arquivos do log: {aviso}')

    # Função para realizar as configurações iniciais do log
    def configurar_log(self):

        try:

            # Chamar função para criar o log
            self.criar_log()

            if not self.logger:

                # Configurar o logger inicial
                self.logger = logging.getLogger(__name__)

                # Configurar o nivel para DEBUG
                self.logger.setLevel(logging.DEBUG)

                # Remover manipuladores para não dulpicar
                for handler in self.logger.handlers:
                    self.logger.removeHandler(handler)

                # Criar o manipulador (HANDLER) para escrever no log
                file_handler = logging.FileHandler(self.arquivo_log_path, encoding='utf-8')

                # Formatar mensagens do log
                formatter = logging.Formatter(f'[%(asctime)s] - {self.nome_plataforma} - %(levelname)s - requests: %(message)s')
                
                # Atribuir no HANDLER
                file_handler.setFormatter(formatter)

                # Atribuir manipulador no logger
                self.logger.addHandler(file_handler)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao realizar as configurações iniciais do log: {aviso}')

    def myname_logger(self):
        try:
            # Obter a pilha de execução (qual bot chamou)
            pilha_execucao = inspect.stack()

            # O arquivo que chamou diretamente sempre será o segundo da lista [0, 1, 2, ... ] - logo, [1]
            chamador = pilha_execucao[3]

            # Obtem o nome do arquivo que chamou
            nome_arquivo_chamador = os.path.basename(chamador.filename)

            # Atualizar variáveis
            self.nome_arquivo = nome_arquivo_chamador

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao obter o nome do arquivo chamador: {aviso}')

    def log_debug(self, message):

        try:
            self._log('DEBUG', message)
        
        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao escrever DEBUGS no log: {aviso}')

    def log_info(self, message):

        try:
            self._log('INFO', message)
        
        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao escrever INFORMAÇÕES no log: {aviso}')

    def log_warn(self, message):

        try:
            self._log('WARN', message)
        
        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao escrever AVISOS no log: {aviso}')

    def log_error(self, message):

        try:
            self._log('ERROR', message)

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao escrever ERROS no log: {aviso}')

    def _log(self, level, message):

        try:

            # Chamar função para buscar o nome
            self.myname_logger()

            # 'getattr' irá pegar o atributo por nome
            self.logger.log(getattr(logging, level), f'{self.nome_arquivo} - {message}')

            # Sem o 'getattr', é necessário passar o atributo como int
            # Lista de int do atributos(levels) = [debug = 10, info = 20, warn = 30, error = 40]
            #self.logger.log(level, f'{self.nome_arquivo} - {message}')

        except Exception as aviso:
            self.status = False
            print(self.erro)
            print(f'Erro ao configurar as mensagens no log: {aviso}')

    

