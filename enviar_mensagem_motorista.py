from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import urllib
import time
import datetime
import traceback
from google_api_functions import *

profile_path = r'C:\Users\vdiassob\AppData\Roaming\Mozilla\Firefox\Profiles\eituekku.robo'
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)
options.binary_location = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'

navegador = webdriver.Firefox(options=options)
navegador.get("https://web.whatsapp.com/")
debug_mode = True

while True:
    try:
        time.sleep(20)
        # input('Digite ENTER para enviar a mensagem!')
        # carregar pacotes recebidos
        pacotes_recebidos_insucesso = get_values('1U-BmZ9k6Jk6Jrpi1MhDQNfpndbydyB8Qy0n3zkFxCVQ','PLANILHA!A1:H')
        pacotes_recebidos_insucesso = pd.DataFrame(pacotes_recebidos_insucesso[1:],columns=pacotes_recebidos_insucesso[0])
        pacotes_recebidos_insucesso.loc[pacotes_recebidos_insucesso['NÚMERO DE WHATSAPP DO MOTORISTA'].str[:1] == '2', 'NÚMERO DE WHATSAPP DO MOTORISTA'] = '55' + pacotes_recebidos_insucesso['NÚMERO DE WHATSAPP DO MOTORISTA'].astype('str')
        limiteInferiorDataMonitoramento = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,00,00,00)
        limiteSuperiorDataMonitoramento = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,23,59,59) + datetime.timedelta(days=1)

        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.loc[(pd.to_datetime(pacotes_recebidos_insucesso['DATA E HORA'],format="%d/%m/%Y %H:%M:%S") >= limiteInferiorDataMonitoramento)
            & (pd.to_datetime(pacotes_recebidos_insucesso['DATA E HORA'],format="%d/%m/%Y %H:%M:%S") <= limiteSuperiorDataMonitoramento)]
        # carregar cadastro de motoristas
        cadastro_de_motoristas = get_values('1VLgkDoCc8i3MGPaWH8NBRATt9iXtwHo5ZZwmVKhoSsc',"'Respostas ao formulário 1'!A1:D")
        cadastro_de_motoristas = pd.DataFrame(cadastro_de_motoristas[1:],columns=cadastro_de_motoristas[0])
        cadastro_de_motoristas['NÚMERO DE WHATSAPP DO MOTORISTA'] = cadastro_de_motoristas['NÚMERO DE WHATSAPP (EXEMPLO: 21988888888)']
        cadastro_de_motoristas.loc[cadastro_de_motoristas['NÚMERO DE WHATSAPP DO MOTORISTA'].str[:1] == '2', 'NÚMERO DE WHATSAPP DO MOTORISTA'] = '55' + cadastro_de_motoristas['NÚMERO DE WHATSAPP DO MOTORISTA'].astype('str')
        # carregar log de whatsapp
        log_whatsapp = get_values('1U-BmZ9k6Jk6Jrpi1MhDQNfpndbydyB8Qy0n3zkFxCVQ',"'LOG WHATSAPP'!A1:D")
        log_whatsapp = pd.DataFrame(log_whatsapp[1:],columns=log_whatsapp[0])            
        log_whatsapp = log_whatsapp.loc[(pd.to_datetime(log_whatsapp['DATA'],format="%d/%m/%Y %H:%M:%S") >= limiteInferiorDataMonitoramento)
            & (pd.to_datetime(log_whatsapp['DATA'],format="%d/%m/%Y %H:%M:%S") <= limiteSuperiorDataMonitoramento)]
        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.merge(cadastro_de_motoristas.copy(), how='left', on='NÚMERO DE WHATSAPP DO MOTORISTA')
        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.merge(log_whatsapp.copy(), how='left', on='ID')
        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.loc[(pacotes_recebidos_insucesso['STATUS DE ENVIO WHATSAPP'].isna()==True)]
        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.loc[(pd.to_numeric(pacotes_recebidos_insucesso['NÚMERO DE WHATSAPP DO MOTORISTA'], errors='coerce').isna()==False)]
        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.loc[pacotes_recebidos_insucesso['STATUS'] != 'O pacote foi perdido']
        pacotes_recebidos_insucesso = pacotes_recebidos_insucesso.drop_duplicates(subset='ID')
        # print(pacotes_recebidos_insucesso)
        # print(log_whatsapp)
        # input()
        # continue
        if len(pacotes_recebidos_insucesso) < 1: print('Nenhum ID para enviar para o motorista.')

        for i in pacotes_recebidos_insucesso["NÚMERO DE WHATSAPP DO MOTORISTA"].unique():
            # Trata os dados
            data_ = time.strftime('%d/%m/%Y')
            quantidade_de_pacotes = len(pacotes_recebidos_insucesso['ID'].astype('str').loc[pacotes_recebidos_insucesso["NÚMERO DE WHATSAPP DO MOTORISTA"]==i].tolist())
            ids = '\n'.join(pacotes_recebidos_insucesso['ID'].astype('str').loc[pacotes_recebidos_insucesso["NÚMERO DE WHATSAPP DO MOTORISTA"]==i].tolist())
            motorista = pacotes_recebidos_insucesso['NOME COMPLETO DO MOTORISTA'].loc[pacotes_recebidos_insucesso["NÚMERO DE WHATSAPP DO MOTORISTA"]==i].tolist()[0]
            mensagem = f'''Olá, {motorista}! Segue a relação de ids que você entregou ao insucesso no dia {data_}:\n\nQuantidade: {quantidade_de_pacotes}\n\nTransportadora: {transportadora}\n\n{ids}'''
            transportadora = pacotes_recebidos_insucesso['TRANSPORTADORA'].loc[pacotes_recebidos_insucesso["NÚMERO DE WHATSAPP DO MOTORISTA"]==i].tolist()[0]
            numero = str(i)
            texto = urllib.parse.quote(f"{mensagem}")
            link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
            data_hora = time.strftime('%d/%m/%Y %H:%M')
            last_row_logwhatsapp = str(int(ultima_linha('1U-BmZ9k6Jk6Jrpi1MhDQNfpndbydyB8Qy0n3zkFxCVQ',"'LOG WHATSAPP'!A1:C")))
            tabela_log_whatsapp_upload = pd.DataFrame({'DATA':[data_hora]*(len(ids.split('\n'))),
            'ID': ids.split('\n'),
            'NÚMERO DE WHATSAPP MOTORISTA':[numero]*(len(ids.split('\n'))),
            'STATUS DE ENVIO WHATSAPP':[f'IDs enviados em {data_hora}']*(len(ids.split('\n')))
            })

            if len(pacotes_recebidos_insucesso) > 0:

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
                    if numero_n_encontrado.text == 'Phone number shared via url is invalid.' or numero_n_encontrado.text == 'O número de telefone compartilhado através de url é inválido.': continue
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
    except:
        if debug_mode:
            print(traceback.format_exc())
        pass