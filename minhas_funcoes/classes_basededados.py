from google_api_functions import get_values, update_values
from dataclasses import dataclass
import pandas as pd

@dataclass
class baseDeDadosGoogle:
    """Classe para lidar com bases de dados"""

    baseDeMotoristas: object = ''
    baseDeInsucesso: object = ''

    def baixar_motoristas(self, idBaseDeCadastroDeMotoristasDoForms,idPlanilhaBaseInsucesso) -> object:
        """Baixa e consolida as bases de cadastro de motorista"""

        for _ in range(15):
            try:
                cadastro_de_motoristas = get_values(idBaseDeCadastroDeMotoristasDoForms,"'Respostas ao formulário 1'!A1:D")
                insucesso = get_values(idPlanilhaBaseInsucesso,"PLANILHA!A1:H")
                break
            except:
                pass

        cadastro_de_motoristas_base_insucesso = pd.DataFrame(insucesso[1:],columns=insucesso[0])
        cadastro_de_motoristas = pd.DataFrame(cadastro_de_motoristas[1:],columns=cadastro_de_motoristas[0])
        cadastro_de_motoristas_base_insucesso['DATA E HORA'] = pd.to_datetime(cadastro_de_motoristas_base_insucesso['DATA E HORA'],yearfirst=False,dayfirst=True)
        cadastro_de_motoristas['DATA E HORA'] = pd.to_datetime(cadastro_de_motoristas['Carimbo de data/hora'],yearfirst=False,dayfirst=True)
        cadastro_de_motoristas['NÚMERO DE WHATSAPP DO MOTORISTA'] = cadastro_de_motoristas['NÚMERO DE WHATSAPP (EXEMPLO: 21988888888)'].astype('str')
        cadastro_de_motoristas = cadastro_de_motoristas[['DATA E HORA','NÚMERO DE WHATSAPP DO MOTORISTA','TRANSPORTADORA','NOME COMPLETO DO MOTORISTA']]
        cadastro_de_motoristas_base_insucesso = cadastro_de_motoristas_base_insucesso[['DATA E HORA','NÚMERO DE WHATSAPP DO MOTORISTA','TRANSPORTADORA','NOME COMPLETO DO MOTORISTA']]
        
        cadastro_de_motoristas_consolidado = pd.concat([cadastro_de_motoristas, cadastro_de_motoristas_base_insucesso])
        cadastro_de_motoristas_consolidado = cadastro_de_motoristas_consolidado.sort_values(by='DATA E HORA',ascending=False)
        cadastro_de_motoristas_consolidado = cadastro_de_motoristas_consolidado.drop_duplicates(subset='NÚMERO DE WHATSAPP DO MOTORISTA')

        self.baseDeMotoristas = cadastro_de_motoristas_consolidado
        
        return self.baseDeMotoristas

    def baixar_insucesso(self, idPlanilhaBaseInsucesso) -> object:
        """Baixa a base de insucesso"""

        for _ in range(15):
            try:
                insucesso = get_values(idPlanilhaBaseInsucesso,"PLANILHA!A1:H")
                break
            except:
                pass

        insucesso = pd.DataFrame(insucesso[1:],columns=insucesso[0])
        self.baseDeInsucesso = insucesso
        
        return self.baseDeInsucesso