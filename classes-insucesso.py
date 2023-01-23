from dataclasses import dataclass
from dataclasses import field
import time
import os

@dataclass
class pacotesInsucesso:
    """Classe para lidar com informações de pacotes"""
    id: list[str] = field(default_factory=list)
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
    
    def consultar_motorista(self):
        """Realiza consulta de cadastros"""
        pass
    
    def realizar_cadastro(self):
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
        
        if self.celular == '':
            while True:
                self.celular = input('Insira o número de WhatsApp do motorista: ')
                if len(self.celular) == 11 and self.celular[:2] == '21':
                    break
                else:
                    print('Número inválido! Por favor, tente novamente')
                    time.sleep(1)
                    os.system('cls')
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



