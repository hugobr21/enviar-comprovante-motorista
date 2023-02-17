from dataclasses import dataclass
from dataclasses import field
import time
import os
import json

@dataclass
class pacotesInsucesso:
    """Classe para lidar com informações de pacotes"""

    id_: list[str] = field(default_factory=list)
    status: list[str] = field(default_factory=list)
    para: list[str] = field(default_factory=list)
    data_de_entrega: list[str] = field(default_factory=list)
    pacote_do_dia_vigente: list[str] = field(default_factory=list)

@dataclass
class motorista:
    """Classe para lidar com informações do motorista"""

    nome: str = ''
    transportadora: str = ''
    celular: str = ''
    
    def validar_numero(self) -> str:
        """Realiza validação de número de telefone"""

        if self.celular != '':
            if input(f'Desejar continuar o processo com o número {self.celular} (s/n): ').upper() == 'S':
                print('\nConsultando número...')
                return self.celular
            else: self.celular = ''
        if self.celular == '':
            while True:
                self.celular = input('Insira o número de WhatsApp do motorista: ')
                if len(self.celular) == 11 and self.celular[:2] == '21':
                    print('\nConsultando número...')
                    break
                else:
                    print('Número inválido! Por favor, tente novamente. ')
                    time.sleep(1)
                    os.system('cls')
        
        return self.celular
    
    def realizar_cadastro(self) -> list:
        """Realiza cadastro de motoristas caso não esteja na base"""

        relacao_transportadoras = '''\nTRANSPORTADORAS
                                1 - DELUNA
                                2 - DHL
                                3 - HAWK TRANSPORTES
                                4 - M.J. TRANSPORTES
                                5 - MURICI
                                6 - ON TIME SERVIÇOS
                                7 - PARCEIRO SPOT SOLUÇÕES
                                8 - LOGISTICSEIRELI
                                9 - PRALOG
                                10 - BEDENDO E VIANA
                                11 - ME EXTRA
                                12 - HELP
                                13 - KANGU\n
                                '''

        lista_transportadoras = ['DELUNA', 'DHL', 'HAWK TRANSPORTES', 'M.J. TRANSPORTES', 'MURICI',
        'ON TIME SERVIÇOS', 'PARCEIRO SPOT SOLUÇÕES', 'LOGISTICSEIRELI',
        'PRALOG', 'BEDENDO E VIANA', 'ME EXTRA', 'HELP', 'KANGU']
        
        self.validar_numero()

        while True:
            try:
                self.transportadora = lista_transportadoras[abs(int(input(f'{relacao_transportadoras}Insira o número correspondente à transportadora do motorista: ')))-1]
                break
            except IndexError:
                print('Transportadora inválida! Por favor, selecione uma transportadora válida.')
                time.sleep(1)
                os.system('cls')
                pass
        self.nome = input('Insira o nome completo do motorista: ').upper()
        return [[self.nome,self.transportadora,self.celular]]

@dataclass
class setupPrograma:
    """Classe para lidar com configurações do programa"""

    idPlanilhaBaseInsucesso: list[str] = field(default_factory=list)
    idBaseDeCadastroDeMotoristasDoForms: list[str] = field(default_factory=list)
    perfilFirefox: list[str] = field(default_factory=list)
    caminhoFirefox: list[str] = field(default_factory=list)

    def configurar_parametros(self) -> None:
        """Define os parâmetros do programa"""

        self.idPlanilhaBaseInsucesso = input('Insira o id da planilha base do insucesso: ').strip()
        self.idBaseDeCadastroDeMotoristasDoForms = input('Insira o id da base de cadastro de motoristas do forms: ').strip()
        self.perfilFirefox = input('Insira o caminho da pasta de perfil do Firefox: ').strip()
        self.caminhoFirefox = input('Insira o caminho do executável do Firefox: ').strip()
        self.salvar_parametros()

    def carregar_parametros(self) -> None:
        """Carrega parametros existentes de configuração do programa"""
    
        try:
            with open("parametros.json", "r") as infile:
                parametros = json.load(infile)
            self.idPlanilhaBaseInsucesso = parametros["idPlanilhaBaseInsucesso"]
            self.idBaseDeCadastroDeMotoristasDoForms = parametros["idBaseDeCadastroDeMotoristasDoForms"]
            self.perfilFirefox = parametros["perfilFirefox"]
            self.caminhoFirefox = parametros["caminhoFirefox"]
        except:
            self.configurar_parametros()

    def salvar_parametros(self):
        """Salvar em JSON arquivo com parâmetros"""

        parametros = {
        "idPlanilhaBaseInsucesso": self.idPlanilhaBaseInsucesso,
        "idBaseDeCadastroDeMotoristasDoForms": self.idBaseDeCadastroDeMotoristasDoForms,
        "perfilFirefox": self.perfilFirefox,
        "caminhoFirefox": self.caminhoFirefox
        }

        with open("parametros.json", "w") as outfile:
                json.dump(parametros, outfile)

    def mostrar_parametros(self):
        """Mostrar parâmetros atuais"""

        print('',"\n ID da planilha base do insucesso: ",self.idPlanilhaBaseInsucesso,'\n',
        "ID da base de cadastro de motoristas do forms: ", self.idBaseDeCadastroDeMotoristasDoForms,'\n',
        "Caminho da pasta de perfil do Firefox: ", self.perfilFirefox,'\n',
        "Caminho do executável do Firefox: ",self.caminhoFirefox,'\n')