from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC_2023.gerente.botoes import LabelButton
from pyautogui import alert
import re

class BannerFuncionario(GridLayout):

    def deletar(self, id, cargo):
        meu_aplicativo = App.get_running_app()

        if cargo != "ADM":
            requisicao = meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/{cargo}/{id}')
        else:
            requisicao = meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios/{id}')

        alert('Exclusão concluida!')
        meu_aplicativo.Opcoes("gfuncionarios")

    def editar(self, id, cargo):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["editarfuncionario"]

        login = tela.ids["login_input"].text
        senha = tela.ids["senha_input"].text

        Dic_Mudanca = {"Nome": f"{login}", "Senha": f"{senha}"}

        if cargo != "ADM":
            Dic_Vendedor = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/{cargo}')
            Pode = True
            for vendedor in Dic_Vendedor:
                if Dic_Vendedor[vendedor]["Nome"] == login:
                    Pode = False
            if Pode == True:
                requisicao = meu_aplicativo.Requisicao_Patch(
                    f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/{cargo}/{id}', Dic_Mudanca)
                alert('Alteração feita!')
                meu_aplicativo.Opcoes("gfuncionarios")
            else:
                alert('Login Existente!')
        else:
            Dic_ADM = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios')
            Pode = True
            for vendedor in Dic_ADM:
                if Dic_ADM[vendedor]["Nome"] == login:
                    Pode = False
            if Pode == True:
                requisicao = meu_aplicativo.Requisicao_Patch(
                    f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios/{id}', Dic_Mudanca)
                alert('Alteração feita!')
                meu_aplicativo.Opcoes("gfuncionarios")

    def ler_funcionario(self, cargo, id, *args):
        meu_aplicativo = App.get_running_app()

        meu_aplicativo.Link_Funcionario = id
        meu_aplicativo.Cargo_Funcionario_Editar = cargo

        tela = meu_aplicativo.root.ids["editarfuncionario"]

        if cargo != "ADM":
            Dic_Funcionario = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/{cargo}/{id}')
        else:
            Dic_Funcionario = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios/{id}')

        tela.ids["nome_completo"].text = f"{Dic_Funcionario['Usuario']}"
        tela.ids["login_input"].text = f"{Dic_Funcionario['Nome']}"
        tela.ids["senha_input"].text = f"{Dic_Funcionario['Senha']}"
        tela.ids["cpf"].text = f"{Dic_Funcionario['CPF']}"

        meu_aplicativo.mudar_tela("editarfuncionario")

    def add_conta(self):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["adicionarfuncionario"]

        nome = tela.ids["nome_input"].text
        if nome != "":
            login = tela.ids["login_input"].text
            if login != "":
                senha = tela.ids["senha_input"].text
                if senha != "":
                    cpf = tela.ids["cpf_input"].text
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
                            Cargo = meu_aplicativo.Cargo_Funcionario
                            if Cargo != None:
                                if Cargo == "Vendedor":
                                    Dic_Funcionario = {"CPF": f"{cpf}", "Nome": f"{login}", "Senha": f"{senha}", "Usuario": f"{nome}", "Comissao": "0"}
                                    Dic_Vendedor = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor')
                                    Pode = True
                                    for vendedor in Dic_Vendedor:
                                        if Dic_Vendedor[vendedor]["Nome"] == login or Dic_Vendedor[vendedor]["Usuario"] == nome:
                                            Pode = False
                                    if Pode == True:
                                        requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor',Dic_Funcionario)
                                        Dic_Vendedor = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor')
                                        for vendedor in Dic_Vendedor:
                                            if Dic_Vendedor[vendedor]["Nome"] == login:
                                                Dic_Lista = {f"{vendedor}": {"Total": 0}}
                                                requisicao = meu_aplicativo.Requisicao_Patch(
                                                    f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{vendedor}/Lista_Venda',Dic_Lista)
                                        alert("Login criado com sucesso!")
                                        meu_aplicativo.Opcoes("gfuncionarios")
                                    else:
                                        alert("Login já existente!")
                                elif Cargo == "Estoque":
                                    Dic_Funcionario = {"CPF": f"{cpf}", "Nome": f"{login}", "Senha": f"{senha}", "Usuario": f"{nome}"}
                                    Dic_Estoque = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Estoque')
                                    Pode = True
                                    for vendedor in Dic_Estoque:
                                        if Dic_Estoque[vendedor]["Nome"] == login or Dic_Estoque[vendedor]["Usuario"] == nome:
                                            Pode = False
                                    if Pode == True:
                                        requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Estoque', Dic_Funcionario)
                                        alert("Login criado com sucesso!")
                                        meu_aplicativo.Opcoes("gfuncionarios")
                                    else:
                                        alert("Login já existente!")
                                elif Cargo == "Caixa":
                                    Dic_Funcionario = {"CPF": f"{cpf}", "Nome": f"{login}", "Senha": f"{senha}", "Usuario": f"{nome}", "Vendas": "0"}
                                    Dic_Caixa = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Caixa')
                                    Pode = True
                                    for vendedor in Dic_Caixa:
                                        if Dic_Caixa[vendedor]["Nome"] == login or Dic_Caixa[vendedor]["Usuario"] == nome:
                                            Pode = False
                                    if Pode == True:
                                        requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Caixa', Dic_Funcionario)
                                        alert("Login criado com sucesso!")
                                        meu_aplicativo.Opcoes("gfuncionarios")
                                    else:
                                        alert("Login já existente!")
                                elif Cargo == "ADM":
                                    Dic_Funcionario = {"CPF": f"{cpf}", "Nome": f"{login}", "Senha": f"{senha}", "Usuario": f"{nome}"}
                                    Dic_ADM = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios')
                                    Pode = True
                                    for vendedor in Dic_ADM:
                                        if Dic_ADM[vendedor]["Nome"] == login or Dic_ADM[vendedor]["Usuario"] == nome:
                                            Pode = False
                                    if Pode == True:
                                        requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios', Dic_Funcionario)
                                        alert("Login criado com sucesso!")
                                        meu_aplicativo.Opcoes("gfuncionarios")
                                    else:
                                        alert("Login já existente!")
                            else:
                                alert("Escolha um CARGO para continuar!")
                        else:
                            alert(F'03 - O CPF {cpf} É INVALIDO!')
                    else:
                        alert(F'02 - O CPF {cpf} É INVALIDO!')
                else:
                    alert("Campo SENHA vazio!")
            else:
                alert("Campo LOGIN vazio!")
        else:
            alert("Campo NOME COMPLETO vazio!")

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_funcionario"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("listarfuncionarios")
        except:
            pass

        Tela_vendas = meu_aplicativo.root.ids["listarfuncionarios"]
        vendas = Tela_vendas.ids["lista_funcionario"]

        Dic_Funcionarios = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios")

        Dic_Caixa = Dic_Funcionarios["Caixa"]
        Dic_Vendedor = Dic_Funcionarios["Vendedor"]
        Dic_Estoque = Dic_Funcionarios["Estoque"]
        Dic_Adm = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios')

        for id in Dic_Caixa:
            Nome = Dic_Caixa[id]["Usuario"]

            texto = f"{Nome}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Caixa", id)
            )
            vendas.add_widget(item)

            Login = Dic_Caixa[id]["Nome"]

            texto = f"{Login}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Caixa", id)
            )
            vendas.add_widget(item)

            Senha = Dic_Caixa[id]["Senha"]

            texto = f"{Senha}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Caixa", id)
            )
            vendas.add_widget(item)

            cpf = Dic_Caixa[id]["CPF"]

            texto = f"{cpf}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Caixa", id)
            )
            vendas.add_widget(item)

            texto = f"Caixa"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Caixa", id)
            )
            vendas.add_widget(item)

        for id in Dic_Vendedor:
            Nome = Dic_Vendedor[id]["Usuario"]

            texto = f"{Nome}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Vendedor", id)
            )
            vendas.add_widget(item)

            Login = Dic_Vendedor[id]["Nome"]

            texto = f"{Login}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Vendedor", id)
            )
            vendas.add_widget(item)

            Senha = Dic_Vendedor[id]["Senha"]

            texto = f"{Senha}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Vendedor", id)
            )
            vendas.add_widget(item)

            cpf = Dic_Vendedor[id]["CPF"]

            texto = f"{cpf}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Vendedor", id)
            )
            vendas.add_widget(item)

            texto = f"Vendedor"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Vendedor", id)
            )
            vendas.add_widget(item)

        for id in Dic_Estoque:
            Nome = Dic_Estoque[id]["Usuario"]

            texto = f"{Nome}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Estoque", id)
            )
            vendas.add_widget(item)

            Login = Dic_Estoque[id]["Nome"]

            texto = f"{Login}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Estoque", id)
            )
            vendas.add_widget(item)

            Senha = Dic_Estoque[id]["Senha"]

            texto = f"{Senha}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Estoque", id)
            )
            vendas.add_widget(item)

            cpf = Dic_Estoque[id]["CPF"]

            texto = f"{cpf}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Estoque", id)
            )
            vendas.add_widget(item)

            texto = f"Estoque"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "Estoque", id)
            )
            vendas.add_widget(item)

        for id in Dic_Adm:
            Nome = Dic_Adm[id]["Usuario"]

            texto = f"{Nome}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "ADM", id)
            )
            vendas.add_widget(item)

            Login = Dic_Adm[id]["Nome"]

            texto = f"{Login}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "ADM", id)
            )
            vendas.add_widget(item)

            Senha = Dic_Adm[id]["Senha"]

            texto = f"{Senha}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "ADM", id)
            )
            vendas.add_widget(item)

            cpf = Dic_Adm[id]["CPF"]

            texto = f"{cpf}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "ADM", id)
            )
            vendas.add_widget(item)

            texto = f"Administrador"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(self.ler_funcionario, "ADM", id)
            )
            vendas.add_widget(item)