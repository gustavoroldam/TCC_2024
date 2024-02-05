import re
from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC_2023.gerente.botoes import LabelButton
from pyautogui import alert
import smtplib
import email.message

class BannerCupons(GridLayout):

    def validar_nome_cupom(self, nome_cupom):
        meu_aplicativo = App.get_running_app()

        Dic_cupons = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Cupons')

        pode = True

        for cupom in Dic_cupons:
            if nome_cupom == Dic_cupons[cupom]["Nome"]:
                pode = False

        return pode

    def salvar_cupom_padrao(self):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["emailpadrao"]
        titulo = tela.ids["titulo_input"].text

        if titulo != '':
            corpo = tela.ids["corpo_input"].text
            if corpo != '':
                nome_cupom = tela.ids["cupom_input"].text
                if nome_cupom != '':
                    nome_cupom = nome_cupom.upper()
                    desconto = tela.ids["desconto_input"].text
                    if desconto != '':
                        try:
                            desconto = int(desconto)
                            valido = BannerCupons.validar_nome_cupom(self, nome_cupom)
                            if valido == True:
                                Dic_Cupom = {"Nome": f'{nome_cupom}', "Desconto": f'{desconto}', "Corpo": f'{corpo}', "Titulo": f'{titulo}'}
                                requisicao = meu_aplicativo.Requisicao_Patch('https://tcc2023-9212b-default-rtdb.firebaseio.com/Cupons/Padrao', Dic_Cupom)
                                alert('Alteração concluida!')
                                meu_aplicativo.Opcoes("cupom")
                            else:
                                alert('Nome do Cupom já existe!')
                        except:
                            alert('Campo DESCONTO (%) incorreto')
                    else:
                        alert('Campo DESCONTO (%) vazio!')
                else:
                    alert('Campo NOME DO CUPOM vazio!')
            else:
                alert('Campo CORPO DO EMAIL vazio!')
        else:
            alert('Campo TÍTULO DO EMAIL vazio!')

    def cupom_padrao(self):
        meu_aplicativo = App.get_running_app()

        Dic_Cupom = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Cupons/Padrao')

        tela = meu_aplicativo.root.ids["emailpadrao"]

        tela.ids["titulo_input"].text = f'{Dic_Cupom["Titulo"]}'
        tela.ids["corpo_input"].text = f'{Dic_Cupom["Corpo"]}'
        tela.ids["cupom_input"].text = f'{Dic_Cupom["Nome"]}'
        tela.ids["desconto_input"].text = f'{Dic_Cupom["Desconto"]}'

        meu_aplicativo.mudar_tela('emailpadrao')

    def Enviar_Cupom_Novo(self, titulo, corpo, nome_cupom, desconto, data):
        meu_aplicativo = App.get_running_app()

        #Guardar no BD
        Dic_Cupom = {"Nome": f"{nome_cupom}", "Corpo": f"{corpo}", "Desconto": f"{desconto}", "Data_Validade": f"{data}", "Titulo": f"{titulo}"}
        requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Cupons', Dic_Cupom)

        email_empresa = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Email')
        senha_empreso = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Senha')

        Dic_Clientes = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes')

        for cliente in Dic_Clientes:

            requisicao = meu_aplicativo.Requisicao_Post(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes/{cliente}/Cupons', Dic_Cupom)

            Email = Dic_Clientes[cliente]["Email"]

            corpo_email = corpo

            msg = email.message.Message()
            msg['Subject'] = f"{titulo}"
            msg['From'] = f'{email_empresa}'
            msg['To'] = f'{Email}'
            password = f'{senha_empreso}'
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()

            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        alert("Cupons enviados!")
        meu_aplicativo.mudar_tela("homepage")

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        tela = meu_aplicativo.root.ids["email"]
        titulo = tela.ids["titulo_input"].text

        if titulo != '':
            corpo = tela.ids["corpo_input"].text
            if corpo != '':
                nome_cupom = tela.ids["cupom_input"].text
                if nome_cupom != '':
                    nome_cupom = nome_cupom.upper()
                    desconto = tela.ids["desconto_input"].text
                    if desconto != '':
                        try:
                            desconto = int(desconto)
                            data = tela.ids["data_input"].text
                            if data != '':
                                # Expressão regular para validar o formato da data
                                pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
                                if not pattern.match(data):
                                    alert('Campo DATA DE VALIDADE incorreto!') # Formato inválido
                                else:
                                    # Verifica se a data é válida
                                    try:
                                        datetime.strptime(data, '%d/%m/%Y')
                                        valido = self.validar_nome_cupom(nome_cupom)
                                        if valido == True:
                                            self.Enviar_Cupom_Novo(titulo, corpo, nome_cupom, desconto, data)
                                        else:
                                            alert('Nome do Cupom já existe!')
                                    except ValueError:
                                        alert('Invalida')  # Data inválida
                            else:
                                alert('Campo DATA DE VALIDADE vazio!')
                        except:
                            alert('Campo DESCONTO (%) incorreto')
                    else:
                        alert('Campo DESCONTO (%) vazio!')
                else:
                    alert('Campo NOME DO CUPOM vazio!')
            else:
                alert('Campo CORPO DO EMAIL vazio!')
        else:
            alert('Campo TÍTULO DO EMAIL vazio!')