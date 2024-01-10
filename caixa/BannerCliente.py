import re
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton
import requests
import json
import pyautogui
from datetime import datetime
import smtplib
import email.message

class BannerCliente(GridLayout):

    def Validar_Cupom(self):
        meu_aplicativo = App.get_running_app()

        if meu_aplicativo.Login_Cliente == True:
            Dic_Clientes = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes')
            Achei_Cupom = False
            tela = meu_aplicativo.root.ids["pagarvenda"]
            cpf = tela.ids["cpf_input"].text
            cupom = tela.ids["cupom_input"].text
            cupom = cupom.upper()
            tela.ids["cupom_input"].text = cupom

            try:
                for Cliente in Dic_Clientes:
                    if Dic_Clientes[Cliente]["CPF"] == cpf:
                        Dic_Lista_Cupons = Dic_Clientes[Cliente]["Cupons"]
                        for Cupom in Dic_Lista_Cupons:
                            if Dic_Lista_Cupons[Cupom]["Nome"] == cupom and Cupom == "BEMVINDO":
                                Achei_Cupom = True
                                meu_aplicativo.Desconto = int(Dic_Lista_Cupons[Cupom]["Desconto"])
                                meu_aplicativo.Cupom_Valido = True

                                tela = meu_aplicativo.root.ids["pagarvenda"]

                                Total = tela.ids["total_compra"].text
                                Total = re.findall(r'\d+|\.', Total)
                                Total = ''.join(Total)
                                Total = float(Total) - (float(Total) * (float(meu_aplicativo.Desconto)/100))

                                tela.ids["label_cupom"].text = f"                         DESCONTO DE {meu_aplicativo.Desconto}% APLICADO: R${Total: ,.2f}"
                                tela.ids["label_cupom"].color = (0, 0, 0, 1)
                            elif Dic_Lista_Cupons[Cupom]["Nome"] == cupom:
                                data_atual = datetime.now()
                                data_validade = datetime.strptime(Dic_Lista_Cupons[Cupom]["Data_Validade"], "%d/%m/%Y")
                                if data_validade > data_atual:
                                    Achei_Cupom = True
                                    meu_aplicativo.Desconto = int(Dic_Lista_Cupons[Cupom]["Desconto"])
                                    meu_aplicativo.Cupom_Valido = True

                                    tela = meu_aplicativo.root.ids["pagarvenda"]

                                    Total = tela.ids["total_compra"].text
                                    Total = re.findall(r'\d+|\.', Total)
                                    Total = ''.join(Total)
                                    Total = float(Total) - (float(Total) * (float(meu_aplicativo.Desconto) / 100))

                                    tela.ids[
                                        "label_cupom"].text = f"                         DESCONTO DE {meu_aplicativo.Desconto}% APLICADO: R${Total: ,.2f}"
                                    tela.ids["label_cupom"].color = (0, 0, 0, 1)
                                else:
                                    meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes/{Cliente}/Cupons/{Cupom}')
            except:
                pass

            if Achei_Cupom == False:
                tela = meu_aplicativo.root.ids["pagarvenda"]
                tela.ids["label_cupom"].text = "        CUPOM NÃO ENCONTRADO OU FORA DA VALIDADE"
                tela.ids["label_cupom"].color = (1, 0, 0, 1)

        else:
            tela = meu_aplicativo.root.ids["pagarvenda"]
            tela.ids["label_cupom"].text = "        CLIENTE NÃO CADASTRADO"
            tela.ids["label_cupom"].color = (1, 0, 0, 1)

    def enviar_email(self, Nome, Email):
        meu_aplicativo = App.get_running_app()

        email_empresa = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Email')
        senha_empresa = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Senha')
        Dic_Cupom = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Cupons/Padrao')
        titulo = f'{Dic_Cupom["Titulo"]}'
        corpo = f'{Dic_Cupom["Corpo"]}'


        corpo_email = f"""{corpo}"""

        msg = email.message.Message()
        msg['Subject'] = f"{titulo}"
        msg['From'] = f'{email_empresa}'
        msg['To'] = f'{Email}'
        password = f'{senha_empresa}'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    def Login(self):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["pagarvenda"]
        cpf = tela.ids["cpf_input"].text

        try:
            dic_Cliente = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes')
            for cliente in dic_Cliente:
                if cpf == dic_Cliente[cliente]["CPF"]:
                    tela = meu_aplicativo.root.ids["cadastrarcliente"]
                    tela.ids["nome_input"].text = dic_Cliente[cliente]["Nome"]
                    tela.ids["email_input"].text = dic_Cliente[cliente]["Email"]
                    tela.ids["cpf_input"].text = dic_Cliente[cliente]["CPF"]

                    tela = meu_aplicativo.root.ids["pagarvenda"]
                    tela.ids["label_cpf"].text = f'                           {dic_Cliente[cliente]["Nome"]}'
                    meu_aplicativo.Login_Cliente = True
        except:
            pass

    def Cadastrar_Cliente(self):
        meu_aplicativo = App.get_running_app()

        BannerCliente.Login(self)

        tela = meu_aplicativo.root.ids["cadastrarcliente"]
        Nome = tela.ids["nome_input"].text
        Email = tela.ids["email_input"].text
        CPF = tela.ids["cpf_input"].text

        if meu_aplicativo.Login_Cliente == False:
            Dic_Padrao = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Cupons/Padrao')

            Dic_Login = {'CPF':f'{CPF}', 'Nome':f'{Nome}', 'Email':f'{Email}', 'Cupons':{'BEMVINDO': {'Nome': f'{Dic_Padrao["Nome"]}', 'Desconto': f'{Dic_Padrao["Desconto"]}'}}}
            meu_aplicativo.Requisicao_Post(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes/', Dic_Login)
            BannerCliente.enviar_email(self, Nome, Email)

        tela = meu_aplicativo.root.ids["pagarvenda"]
        tela.ids["label_cpf"].text = f'                           {Nome}'
        meu_aplicativo.mudar_tela("pagarvenda")

        meu_aplicativo.Login_Cliente = True

    def Validar_CPF(self):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["pagarvenda"]
        cpf = tela.ids["cpf_input"].text

        #Deixar somente em número
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) == 11:
            digitos = list(map(int, cpf))
            soma1 = sum(x * y for x, y in zip(digitos[:9], range(10, 1, -1)))
            digito1 = (soma1 * 10) % 11 if (soma1 * 10) % 11 < 10 else 0

            soma2 = sum(x * y for x, y in zip(digitos[:10], range(11, 1, -1)))
            digito2 = (soma2 * 10) % 11 if (soma2 * 10) % 11 < 10 else 0

            if digito1 == digitos[9] and digito2 == digitos[10]:
                # Formatando como CPF
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

                tela.ids["cpf_input"].text = f'{cpf}'
                tela.ids["label_cpf"].text = '             CPF VALIDO'
                tela = meu_aplicativo.root.ids["cadastrarcliente"]
                tela.ids["cpf_input"].text = f'{cpf}'

                meu_aplicativo.CPF_Valido = True
                BannerCliente.Login(self)
            else:
                pyautogui.alert(F'03 - O CPF {cpf} É INVALIDO!')
        else:
            pyautogui.alert(F'02 - O CPF {cpf} É INVALIDO!')

    def __init__(self, **kwargs):
        meu_aplicativo = App.get_running_app()

        super().__init__()

        tela = meu_aplicativo.root.ids["cadastrarcliente"]
        Nome = tela.ids["nome_input"].text
        Email = tela.ids["email_input"].text
        CPF = tela.ids["cpf_input"].text
        if Nome != '' and Email != '' and CPF != '':
            padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if re.match(padrao, Email):
                if meu_aplicativo.CPF_Valido == True:
                    self.Cadastrar_Cliente()
                else:
                    tela = meu_aplicativo.root.ids["pagarvenda"]
                    tela.ids["cpf_input"].text = CPF
                    self.Validar_CPF()
                    if meu_aplicativo.CPF_Valido == True:
                        self.Cadastrar_Cliente()
            else:
                pyautogui.alert("EMAIL INCORRETO!")
        else:
            pyautogui.alert("PREENCHA TODOS OS CAMPOS!")