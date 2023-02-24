from dataclasses import dataclass
from dataclasses import field
import time
import os
import json
import pandas as pd
import re


@dataclass
class pacotesInsucesso:
    """Classe para lidar com informações de pacotes"""

    id_s: list[str] = field(default_factory=list)
    status: list[str] = field(default_factory=list)
    para: list[str] = field(default_factory=list)
    data_de_entrega: list[str] = field(default_factory=list)
    pacote_do_dia_vigente: list[str] = field(default_factory=list)
    FINALIZAR: str = None
    CANCELAR: str = None
    
    def limpar_dados_de_pacotes(self) -> None:
        """Limpa dados de input de pacotes"""

        self.id_s = []
        self.status = []
        self.para = []
        self.data_de_entrega = []
        self.pacote_do_dia_vigente = []

    def coletar_pacotes(self) -> None:
        """Coleta os pacotes validando código do id"""

        os.system('cls')
        input_coletor = input('Para cancelar a coleta e voltar ao menu principal digite CANCELAR e pressione ENTER.\nBipe o ID do pacote ou digite FINALIZAR e aperte ENTER para finalizar a coleta de IDs: ')
        if input_coletor.strip().upper() == 'FINALIZAR': self.FINALIZAR = 'FINALIZAR'
        if input_coletor.strip().upper() == 'CANCELAR': self.CANCELAR = 'CANCELAR'
        elif str(type(re.search(r'4\d\d\d\d\d\d\d\d\d\d',input_coletor)))=="<class 'NoneType'>" and self.FINALIZAR != 'FINALIZAR' and self.CANCELAR != 'CANCELAR':
            os.system('cls')
            print('O ID escaneado ou a opção é invalida. Tente novamente.')
            time.sleep(1)
            self.coletar_pacotes()
        elif str(type(re.search(r'4\d\d\d\d\d\d\d\d\d\d',input_coletor)))!="<class 'NoneType'>" and self.FINALIZAR != 'FINALIZAR' and self.CANCELAR != 'CANCELAR':
             self.id_s += [re.search(r'4\d\d\d\d\d\d\d\d\d\d',input_coletor)[0]]

    def coletar_pacotes_com_status_divergentes(self) -> str:
        """Coleta status não convencional"""

        self.FINALIZAR = None
        self.CANCELAR = None

        while True:
            self.coletar_pacotes()
            if self.FINALIZAR == 'FINALIZAR':
                break
            if self.CANCELAR == 'CANCELAR':
                break
            self.status += [f"PACOTE DIVERGENTE - {input('Explique a divergência: ')}".upper()]                

    def consolidar_pacotes(self, nome, transportadora, operador, celular) -> None:
        """Consolidar pacotes divergentes com status"""

        ids_a_receber = pd.DataFrame({'ID do envio':self.id_s,'Status':self.status})
        ids_a_receber['Para'] = ''
        ids_a_receber['NOME COMPLETO DO MOTORISTA'] = nome
        ids_a_receber['TRANSPORTADORA'] = transportadora
        ids_a_receber['RESPONSÁVEL DHL'] = operador
        ids_a_receber['DATA DE ENTREGA'] = time.strftime('%d/%m/%Y %H:%M:%S')
        ids_a_receber['PACOTE DO DIA'] = '-'
        ids_a_receber['NÚMERO DE WHATSAPP DO MOTORISTA'] = celular

        return ids_a_receber

@dataclass
class interfaceDePrograma:
    """Classe para lidar com interface com usuário"""

    usuario: list[str] = field(default_factory=list)

    def escolher_usuario(self) -> None:
        """Escolher usuário para operar programa"""
        
        while True:
            try:
                os.system('cls')
                text_operadores = '''\nRESPONSÁVEIS DHL
                                        1 - LUANA MEDEIROS
                                        2 - RODRIGO SALDANHA
                                        3 - ULISSES
                                        4 - RAFAEL BARROS
                                        5 - RODRIGO LIMA
                                        5 - FERNANDO JUNIOR\n                                        
                                        '''
                print(text_operadores)
                operador_input = int(input('Digite o número correspondente do responsável DHL: '))
                if operador_input > 5 or operador_input < 0:continue
                lista_operadores = ['LUANA MEDEIROS','RODRIGO SALDANHA','ULISSES','RAFAEL BARROS','RODRIGO LIMA']
                self.usuario = lista_operadores[operador_input-1]
                break
            except:
                print('Opção invalida!')
                pass

    def menu_principal(self) -> None:
        """Função para mostrar menu principal"""

        text_menu = '''Assistente do insucesso\n
            1 - Salvar pacotes de insucesso do dia anterior.\n
            2 - Salvar pacotes de insucesso do dia\n
            3 - Salvar pacotes com divergência\n
            '''

        while True:
            os.system('cls')
            try:
                print(text_menu)
                funcao = int(input('\nDigite o numero da função e pressione enter para iniciar o processo: '))
                break
            except:
                print('Função incorreta.\n')
                time.sleep(1)
            
            # if funcao == 1: salvar_ids_insucesso_do_dia_anterior(operador)
            # if funcao == 2: salvar_ids_insucesso_do_dia(operador)
            # if funcao == 3: self.coletar_pacotes_com_status_divergentes()

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