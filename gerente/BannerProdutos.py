from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton
from pyautogui import alert
import re

class BannerProdutos(GridLayout):

    def editar(self, id, cargo):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["listarprodutos"]

        login = tela.ids["login_input"].text
        senha = tela.ids["senha_input"].text

        Dic_Mudanca = {"Nome": f"{login}", "Senha": f"{senha}"}

        if cargo != "ADM":
            requisicao = meu_aplicativo.Requisicao_Patch(
                f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/{cargo}/{id}', Dic_Mudanca)
        else:
            requisicao = meu_aplicativo.Requisicao_Patch(
                f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios/{id}', Dic_Mudanca)

        alert('Alteração feita!')
        meu_aplicativo.Opcoes("gfuncionarios")

    def ler_produto(self, cargo, id, *args):
        meu_aplicativo = App.get_running_app()

        meu_aplicativo.Link_Funcionario = id
        meu_aplicativo.Cargo_Funcionario_Editar = cargo

        tela = meu_aplicativo.root.ids["listarprodutos"]

        if cargo != "ADM":
            Dic_Funcionario = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/{cargo}/{id}')
        else:
            Dic_Funcionario = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios/{id}')

        tela.ids["nome_completo"].text = f"{Dic_Funcionario['Usuario']}"
        tela.ids["login_input"].text = f"{Dic_Funcionario['Nome']}"
        tela.ids["senha_input"].text = f"{Dic_Funcionario['Senha']}"
        tela.ids["cpf"].text = f"{Dic_Funcionario['CPF']}"

        meu_aplicativo.mudar_tela("editarfuncionario")

    def add_produto(self):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["adicionarproduto"]

        nome = tela.ids["nome_input"].text
        if nome != "":
            qtde = tela.ids["qtde_input"].text
            try:
                qtde = int(qtde)
            except:
                qtde = ""
            if qtde != "":
                valor = tela.ids["valor_input"].text
                try:
                    valor = float(valor)
                except:
                    try:
                        valor = valor.replace(',', '.')
                        valor = float(valor)
                    except:
                        valor = ''
                if valor != "":
                    Dic_Cadastro = {"Nome": nome, "Quantidade": qtde, "Valor": valor}
                    Proximo_Id = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/Proximo_Id')
                    requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{Proximo_Id}', Dic_Cadastro)
                    Proximo_Id += 1
                    Dic_Proximo_Id = {"Proximo_Id": Proximo_Id}
                    requisicao = meu_aplicativo.Requisicao_Patch('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos', Dic_Proximo_Id)
                    alert('Produto gravado com SUCESSO!')
                    meu_aplicativo.Opcoes("gprodutos")
                else:
                    alert("Campo VALOR vazio ou incorreto!")
            else:
                alert("Campo QUANTIDADE vazio ou incorreto!")
        else:
            alert("Campo NOME vazio!")

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_produto"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("listarprodutos")
        except:
            pass

        Tela_vendas = meu_aplicativo.root.ids["listarprodutos"]
        vendas = Tela_vendas.ids["lista_produto"]

        Dic_Produtos = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        for id in Dic_Produtos:
            if id != "Proximo_Id":
                Nome = Dic_Produtos[id]["Nome"]

                texto = f"{Nome}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(self.ler_produto, "Caixa", id)
                )
                vendas.add_widget(item)

                Qtde = Dic_Produtos[id]["Quantidade"]

                texto = f"{Qtde}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(self.ler_produto, "Caixa", id)
                )
                vendas.add_widget(item)

                Valor = float(Dic_Produtos[id]["Valor"])

                texto = f"{Valor: ,.2f}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(self.ler_produto, "Caixa", id)
                )
                vendas.add_widget(item)