from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import urllib
import time
import traceback
from google_api_functions import *
import os
import re
import json

def carregarParametros():
    with open("parametros.json", "r") as infile:
        parametros = json.load(infile)
    return parametros

def subir_informacoes_googlesheets_pulando_linha(tabela):
    last_row = str(int(ultima_linha('1U-BmZ9k6Jk6Jrpi1MhDQNfpndbydyB8Qy0n3zkFxCVQ','PLANILHA!A1:A')))
    for i in range(15):
        try:
            update_values('1U-BmZ9k6Jk6Jrpi1MhDQNfpndbydyB8Qy0n3zkFxCVQ',f'PLANILHA!A{last_row}:H','USER_ENTERED',tabela.values.tolist())
            print('\nPacotes salvos!')
            break
        except:
            if debug_mode: print(traceback.format_exc())

def validar_informacoes_motorista(numero_do_motorista):
    for i in range(15):
        try:
            cadastro_de_motoristas = get_values(carregarParametros()["idBaseDeCadastroDeMotoristasDoForms"],"'Respostas ao formulário 1'!A1:D")
            cadastro_de_motoristas2 = get_values(carregarParametros()["idPlanilhaBase"],"'CADASTRO DE MOTORISTAS 2'!A1:C")
            break
        except:
            if debug_mode: print(traceback.format_exc())
        # try:
        #     cadastro_de_motoristas2 = get_values(carregarParametros()["idPlanilhaBase"],"'CADASTRO DE MOTORISTAS 2'!A1:C")
        #     break
        # except:
        #     if debug_mode: print(traceback.format_exc())
    cadastro_de_motoristas = pd.DataFrame(cadastro_de_motoristas[1:],columns=cadastro_de_motoristas[0])
    cadastro_de_motoristas2 = pd.DataFrame(cadastro_de_motoristas2[1:],columns=cadastro_de_motoristas2[0])
    cadastro_de_motoristas['NÚMERO DE WHATSAPP DO MOTORISTA'] = cadastro_de_motoristas['NÚMERO DE WHATSAPP (EXEMPLO: 21988888888)'].astype('str')
    cadastro_de_motoristas = pd.concat([cadastro_de_motoristas,cadastro_de_motoristas2])

    return cadastro_de_motoristas.loc[cadastro_de_motoristas['NÚMERO DE WHATSAPP DO MOTORISTA']==numero_do_motorista]

def salvar_ids_insucesso_do_dia(operador):
    
    # Validar informações de insucesso
    os.system('cls')
    numero_do_motorista = input('\nDigite o número do whatsapp do motorista e pressione ENTER: ')
    print('\nConsultando número...')
    tabela_info_motorista = validar_informacoes_motorista(numero_do_motorista)
    if len(tabela_info_motorista) < 1:
        os.system('cls')
        print('\nInformações do motorista não encontradas.')
        text_transportadoras = '''\nTRANSPORTADORAS
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
        print(text_transportadoras)
        opcao_transportadora = int(input('\nDigite o número da transportadora do motorista: '))
        lista_transportadoras = ['DELUNA', 'DHL', 'HAWK TRANSPORTES', 'M.J. TRANSPORTES', 'MURICI',
        'ON TIME SERVIÇOS', 'PARCEIRO SPOT SOLUÇÕES', 'LOGISTICSEIRELI',
        'PRALOG', 'BEDENDO E VIANA', 'ME EXTRA', 'HELP', 'KANGU']
        transportadora = lista_transportadoras[opcao_transportadora-1]
        nome_do_motorista = input('Digite o nome completo do motorista: ').upper()

    else:
        transportadora = tabela_info_motorista['TRANSPORTADORA'].values[0]
        nome_do_motorista = tabela_info_motorista['NOME COMPLETO DO MOTORISTA'].values[0].upper()
        os.system('cls')
        print('\n',tabela_info_motorista)
        if input('\nDeseja seguir o processo com este motorista (s/n)? ').upper() != 'S':
            return True
    while True:
        tabela_insucesso = navegador.find_elements(By.CLASS_NAME,'andes-table__row')
        lista = [i.text for i in tabela_insucesso]
        if len(lista) < 1:
            if input('Nenhum ID na lista de recebimento. Deseja repetir a pesquisa (s/n)?').upper() == 'S':
                continue
            else:
                return True
        else:
            break

    # Tratar tabela de base de insucesso
    
    ids_a_receber = pd.DataFrame(lista[1:], columns=['ID do envio'])
    ids_a_receber['Status'] = ids_a_receber['ID do envio'].str[12:].str.split('Devolução').str[0].str.split('Classificação').str[0].str.strip()
    ids_a_receber['Para'] = ids_a_receber['ID do envio'].str[12:].str.split(' ').str[-1]
    ids_a_receber['ID do envio'] = ids_a_receber['ID do envio'].str[:12].str.strip()
    ids_a_receber['NOME COMPLETO DO MOTORISTA'] = nome_do_motorista
    ids_a_receber['TRANSPORTADORA'] = transportadora
    ids_a_receber['RESPONSÁVEL DHL'] = operador
    ids_a_receber['DATA DE ENTREGA'] = time.strftime('%d/%m/%Y %H:%M:%S')
    ids_a_receber['PACOTE DO DIA'] = 'SIM'
    ids_a_receber['NÚMERO DE WHATSAPP DO MOTORISTA'] = numero_do_motorista
    ids_a_receber = ids_a_receber.loc[ids_a_receber['Status'].str.strip() != 'O pacote foi perdido Solução de problemas']

    os.system('cls')
    print('\n',ids_a_receber)
    print(f'\nNome do motorista: {nome_do_motorista}')
    print(f'\nResponsável DHL: {operador}')
    
    # Armazenar informações de insucesso

    if input('Deseja armazenar esses pacotes na base do insucesso e enviar comprovante por whatsapp(s/n)? ').upper() == 'S':
        print('Armazenando pacotes na base do insucesso...')
        subir_informacoes_googlesheets_pulando_linha(ids_a_receber[['DATA DE ENTREGA','ID do envio','NOME COMPLETO DO MOTORISTA','TRANSPORTADORA','PACOTE DO DIA','Status','RESPONSÁVEL DHL','NÚMERO DE WHATSAPP DO MOTORISTA']])
        enviar_comprovante_whatsapp(nome_do_motorista,transportadora,operador,numero_do_motorista,ids_a_receber['ID do envio'])
        input('Pressione ENTER para continuar.')
    else:
        os.system('cls')
        return True

def salvar_ids_insucesso_do_dia_anterior(operador):
    os.system('cls')
    numero_do_motorista = input('\nDigite o número do whatsapp do motorista e pressione ENTER: ')
    print('\nConsultando número...')
    tabela_info_motorista = validar_informacoes_motorista(numero_do_motorista)
    if len(tabela_info_motorista) < 1:
        print('\nInformações do motorista não encontradas.')
        text_transportadoras = '''\nTRANSPORTADORAS
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
        print(text_transportadoras)
        opcao_transportadora = int(input('\nDigite o número da transportadora do motorista: '))
        lista_transportadoras = ['DELUNA', 'DHL', 'HAWK TRANSPORTES', 'M.J. TRANSPORTES', 'MURICI',
        'ON TIME SERVIÇOS', 'PARCEIRO SPOT SOLUÇÕES', 'LOGISTICSEIRELI',
        'PRALOG', 'BEDENDO E VIANA', 'ME EXTRA', 'HELP', 'KANGU']
        transportadora = lista_transportadoras[opcao_transportadora-1]
        nome_do_motorista = input('Digite o nome completo do motorista: ').upper()

    else:
        transportadora = tabela_info_motorista['TRANSPORTADORA'].values[0]
        nome_do_motorista = tabela_info_motorista['NOME COMPLETO DO MOTORISTA'].values[0].upper()
    lista_de_ids_do_dia_anterior = []
    while True:
        try:
            os.system('cls')
            try:
                if len(lista_de_ids_do_dia_anterior) > 0: print('\nIDs coletados:\n','\n'.join(lista_de_ids_do_dia_anterior))
            except:
                pass
            id_coletor = input('\nBipe o ID do pacote ou digite s e aperte ENTER para sair: ')
            if id_coletor.upper() == 'S':
                if input('\nTem certeza que deseja sair par ao menu principal(s/n)?: ').upper() == 'S': return True
                pass
            if id_coletor == '':
                if input('\nDeseja finalizar a coleta de IDs(s/n)?: ').upper() == 'S': break
            id_coletor = re.search(r'4\d\d\d\d\d\d\d\d\d\d',id_coletor)[0]
            navegador.get('https://envios.mercadolivre.com.br/logistics/management-packages/package/' + str(id_coletor))
            if input('\nPara atrelar o status ao ID digite ENTER. Caso contrário digite s e pressione ENTER. ') == '':
                for i in range(15):
                    status_virado = navegador.find_elements(By.CLASS_NAME,'andes-dropdown__display-values')
                    if len(status_virado) > 0:
                        status_virado = navegador.find_elements(By.CLASS_NAME,'andes-dropdown__display-values')[0].text.strip()
                        break
                lista_de_ids_do_dia_anterior.append([id_coletor,status_virado])
        except:
            if debug_mode:
                print(traceback.format_exc())
            print('ID/função invalida!')
            time.sleep(1)
    
    ids_a_receber = pd.DataFrame(lista_de_ids_do_dia_anterior, columns=['ID do envio','Status'])
    # ids_a_receber['Status'] = ''
    ids_a_receber['Para'] = ''
    ids_a_receber['NOME COMPLETO DO MOTORISTA'] = nome_do_motorista
    ids_a_receber['TRANSPORTADORA'] = transportadora
    ids_a_receber['RESPONSÁVEL DHL'] = operador
    ids_a_receber['DATA DE ENTREGA'] = time.strftime('%d/%m/%Y %H:%M:%S')
    ids_a_receber['PACOTE DO DIA'] = 'NÃO'
    ids_a_receber['NÚMERO DE WHATSAPP DO MOTORISTA'] = numero_do_motorista

    
    print('\n',ids_a_receber)
    print(f'\nNome do motorista: {nome_do_motorista}')
    print(f'\nResponsável DHL: {operador}')
    print(f'\nTransportadora: {transportadora}')
    input('Pressione ENTER para continuar.')

    if input('Deseja armazenar esses pacotes na base do insucesso e enviar comprovante por whatsapp(s/n)? ').upper() == 'S':
        print('Armazenando pacotes na base do insucesso...')
        subir_informacoes_googlesheets_pulando_linha(ids_a_receber[['DATA DE ENTREGA','ID do envio','NOME COMPLETO DO MOTORISTA','TRANSPORTADORA','PACOTE DO DIA','Status','RESPONSÁVEL DHL','NÚMERO DE WHATSAPP DO MOTORISTA']])
        enviar_comprovante_whatsapp(nome_do_motorista,transportadora,operador,numero_do_motorista,ids_a_receber['ID do envio'])
        input('Pressione ENTER para continuar.')
    else:
        os.system('cls')
        return True

def escolher_funcao(operador):
    text_menu = '''Assistente do insucesso\n
    1 - Salvar pacotes de insucesso do dia anterior.\n
    2 - Salvar pacotes de insucesso do dia\n
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
    
    if funcao == 1: salvar_ids_insucesso_do_dia_anterior(operador)
    if funcao == 2: salvar_ids_insucesso_do_dia(operador)

def enviar_comprovante_whatsapp(motorista,transportadora,responsavel_dhl,numero_whatsapp_motorista,listadeids):
    while True:
        try:
            # Tratar os dados
            
            data_ = time.strftime('%d/%m/%Y')
            quantidade_de_pacotes = len(listadeids)
            ids = '\n'.join(listadeids.tolist())
            if str(numero_whatsapp_motorista)[0] == '2':
                numero = f'55{numero_whatsapp_motorista}'
            else:
                numero = str(numero_whatsapp_motorista)
            mensagem = f'''Olá, {motorista}! Segue a relação de ids que você entregou ao insucesso no dia {data_}:\n\nQuantidade: {quantidade_de_pacotes}\n\nTransportadora: {transportadora}\n\nResponsável DHL: {responsavel_dhl}\n\n{ids}'''
            texto = urllib.parse.quote(f"{mensagem}")
            link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
            data_hora = time.strftime('%d/%m/%Y %H:%M')
            last_row_logwhatsapp = str(int(ultima_linha(carregarParametros()["idPlanilhaBase"],"'LOG WHATSAPP'!A1:C")))
            tabela_log_whatsapp_upload = pd.DataFrame({'DATA':[data_hora]*(len(ids.split('\n'))),
            'ID': ids.split('\n'),
            'NÚMERO DE WHATSAPP MOTORISTA':[numero]*(len(ids.split('\n'))),
            'STATUS DE ENVIO WHATSAPP':[f'IDs enviados em {data_hora}']*(len(ids.split('\n')))
            })
            navegador.switch_to.window(navegador.window_handles[1])
            navegador.get(link)
            if len(listadeids) > 0:

                while len(navegador.find_elements(By.ID,"side")) < 1:
                    time.sleep(1)

                if debug_mode:
                    print(link)
                navegador.get(link)
                for i in range(20):
                    time.sleep(1)
                    try:
                        if debug_mode:
                            print("Procurando erro...")
                        if len(navegador.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]")) != 0:
                            break
                        else:
                            numero_n_encontrado = [i for i in navegador.find_elements(By.TAG_NAME,'div') if i.text == 'Phone number shared via url is invalid.' or i.text == 'O número de telefone compartilhado através de url é inválido.'][0]
                            print(numero_n_encontrado.text)
                            break
                    except:
                        pass
                try:
                    if numero_n_encontrado.text == 'Phone number shared via url is invalid.' or numero_n_encontrado.text == 'O número de telefone compartilhado através de url é inválido.':
                        
                        continue
                except:
                    if debug_mode:
                        print("Enviando mensagem para motorista...")
                    pass

                while len(navegador.find_elements(By.ID,"side")) < 1:
                    time.sleep(1)
                while len(navegador.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]")) < 1:
                    time.sleep(1)
                for i in range(10):
                    time.sleep(1)
                    try:
                        [i for i in navegador.find_elements(By.TAG_NAME,'button') if i.get_attribute('aria-label') == "Send" or i.get_attribute('aria-label') == "Enviar"][0].click()
                        break
                    except:
                        pass
                # grava o log de envio no google sheets
                for i in range(20):
                    try:
                        update_values('1U-BmZ9k6Jk6Jrpi1MhDQNfpndbydyB8Qy0n3zkFxCVQ',f"'LOG WHATSAPP'!A{last_row_logwhatsapp}:D",'USER_ENTERED',tabela_log_whatsapp_upload.values.tolist())
                        break
                    except:
                        pass
                time.sleep(5)
            else:
                print('Nenhum ID para enviar para o motorista.') 
                break
            navegador.switch_to.window(navegador.window_handles[0])
            break
        except:
            if debug_mode:
                print(traceback.format_exc())
                input()
            pass

profile_path = carregarParametros()['perfilFirefox']
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)
options.binary_location = carregarParametros()['caminhoFirefox']

navegador = webdriver.Firefox(options=options)
navegador.get("https://envios.mercadolivre.com.br/logistics/service-center/return-to-station")
navegador.execute_script("window.open('');")
navegador.switch_to.window(navegador.window_handles[1])
navegador.get('https://web.whatsapp.com/')
navegador.switch_to.window(navegador.window_handles[0])
debug_mode = True

while True:
    try:
        os.system('cls')
        text_operadores = '''\nRESPONSÁVEIS DHL
                                1 - LUANA MEDEIROS
                                2 - RODRIGO SALDANHA
                                3 - ULISSES
                                4 - RAFAEL BARROS
                                5 - RODRIGO LIMA\n
                                '''
        print(text_operadores)
        operador_input = int(input('Digite o número correspondente do responsável DHL: '))
        if operador_input > 5 or operador_input < 0:continue
        lista_operadores = ['LUANA MEDEIROS','RODRIGO SALDANHA','ULISSES','RAFAEL BARROS','RODRIGO LIMA']
        operador = lista_operadores[operador_input-1]
        break
    except:
        print('Opção invalida!')
        pass

while True:
    try:
        os.system('cls')
        escolher_funcao(operador)
    except:
        if debug_mode:
            print(traceback.format_exc())
            input()
        pass