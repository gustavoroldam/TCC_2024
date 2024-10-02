import json

import requests
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from functools import partial

from vendedor.botoes import LabelButton


class BannerCarrinho(GridLayout):
    Produto_Carrinho = None
    Quantidade_Carrinho = None
    Valor_Carrinho = None
    id_vendedor = None

    def Limpar_Carrinho(self, id_vendedor):
        meu_aplicativo = App.get_running_app()

        requisicao = requests.get(
            f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda.json")
        requisicao_dic = requisicao.json()

        for id in requisicao_dic:
            if id != id_vendedor:
                requisicao = requests.delete(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda/{id}.json")
            else:
                Total = 0
                Dic_Total = {"Total": f'{Total: ,.2f}'}
                requisicao = requests.patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda/{id_vendedor}/.json",
                        data=json.dumps(Dic_Total))
                pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
                pagina_carrinho.ids["total_venda"].text = f"Total: {Total: ,.2f}"

    def Deletar_Item(self, id_vendedor):

        meu_aplicativo = App.get_running_app()

        tela_mudanca = meu_aplicativo.root.ids["mudarpedido"]
        Produto = tela_mudanca.ids["id_Produto"].text

        requisicao = requests.get(
            f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}.json")
        requisicao_dic = requisicao.json()

        try:
            Total = float(requisicao_dic['Total'])
        except:
            Total = requisicao_dic['Total'].replace(',', '')
            Total = float(Total)

        requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda.json")
        requisicao_dic = requisicao.json()

        for id in requisicao_dic:
            if id != id_vendedor:
                if requisicao_dic[id]["Produto"] == Produto:

                    try:
                        Total -= float(requisicao_dic[id]["Valor"])
                    except:
                        Calculo = requisicao_dic[id]["Valor"].replace(',', '')
                        Total -= float(Calculo)
                    Dic_Total = {'Total':f'{Total: ,.2f}'}
                    requisicao = requests.patch(
                        f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}/.json",
                        data=json.dumps(Dic_Total))

                    requisicao = requests.delete(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda/{id}.json")
                    meu_aplicativo.Carrinho("Carregar")

        requisicao = requests.get(
            f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}.json")
        requisicao_dic = requisicao.json()
        pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
        try:
            Total = float(requisicao_dic['Total'])
        except:
            Total = requisicao_dic['Total'].replace(',', '')
            Total = float(Total)
        pagina_carrinho.ids["total_venda"].text = f"Total: {Total: ,.2f}"

    def Salvar_Alteracao(self, id_vendedor):

        meu_aplicativo = App.get_running_app()

        tela_mudanca = meu_aplicativo.root.ids["mudarpedido"]
        Produto = tela_mudanca.ids["id_Produto"].text
        Quantidade = tela_mudanca.ids["quantidade"].text
        Valor = meu_aplicativo.Novo_valor_produto

        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
        Produto_Dic = requisicao.json()
        for id in Produto_Dic:
            if id != "Proximo_Id" and Produto_Dic[id]["Nome"] == Produto:
                Nova_Qtde = int(Produto_Dic[id]["Quantidade"]) - int(Quantidade)
                if Nova_Qtde > 0:

                    tela = meu_aplicativo.root.ids["mudarpedido"]
                    tela.ids["salvar_sair"].text = "Salvar e Sair"
                    tela.ids["salvar_sair"].color = (1, 1, 1, 1)

                    requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}.json")
                    requisicao_dic = requisicao.json()

                    try:
                        Total = float(requisicao_dic['Total'])
                    except:
                        Total = requisicao_dic['Total'].replace(',', '')
                        Total = float(Total)

                    requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda.json")
                    requisicao_dic = requisicao.json()

                    for id in requisicao_dic:
                        if id != id_vendedor:
                            if requisicao_dic[id]["Produto"] == Produto:

                                try:
                                    Total -= float(requisicao_dic[id]["Valor"])
                                except:
                                    Calculo = requisicao_dic[id]["Valor"].replace(',', '')
                                    Total -= float(Calculo)

                                try:
                                    Total += float(Valor)
                                except:
                                    try:
                                        Calculo = Valor.replace(',', '')
                                        Total += float(Valor)
                                    except:
                                        pass

                                Dic_Total = {'Total':f'{Total: ,.2f}'}
                                requisicao = requests.patch(
                                    f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}/.json",
                                    data=json.dumps(Dic_Total))
                                pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
                                pagina_carrinho.ids["total_venda"].text = f"Total: {Total: ,.2f}"

                                dados = {'Quantidade': Quantidade, 'Valor': Valor}
                                requisicao = requests.patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda/{id}.json", data=json.dumps(dados))
                                meu_aplicativo.Carrinho("Carregar")
                else:
                    tela = meu_aplicativo.root.ids["mudarpedido"]
                    tela.ids["salvar_sair"].text = "Falta de Estoque"
                    tela.ids["salvar_sair"].color = (1, 0, 0, 1)

    def ModificarQuantidade_Carrinho(self, fazer):

        meu_aplicativo = App.get_running_app()

        produto = meu_aplicativo.root.ids["mudarpedido"]
        Produto_Carrinho = produto.ids["id_Produto"].text

        if fazer == 1:
            novo_valor = meu_aplicativo.root.ids["mudarpedido"]
            valor = int(novo_valor.ids["quantidade"].text)
            valor = valor + 1
            novo_valor.ids["quantidade"].text = f"{valor}"
        elif fazer == -1:
            novo_valor = meu_aplicativo.root.ids["mudarpedido"]
            valor = int(novo_valor.ids["quantidade"].text)
            if valor > 1:
                valor = valor - 1
            novo_valor.ids["quantidade"].text = f"{valor}"

        novo_valor = meu_aplicativo.root.ids["mudarpedido"]
        quantidade = int(novo_valor.ids["quantidade"].text)

        requisicao = requests.get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json")
        requisicao_dic = requisicao.json()
        valor = None
        for produto in requisicao_dic:
            if produto != "Proximo_Id" and Produto_Carrinho == requisicao_dic[produto]["Nome"]:
                valor = int(requisicao_dic[produto]["Valor"])

        Valor_Carrinho = valor * quantidade
        meu_aplicativo.Novo_valor_produto = Valor_Carrinho
        novo_valor.ids["id_Valor"].text = f"R$ {Valor_Carrinho: ,.2f}"

    def selecionar_item_carrinho(self, nome_produto, quantidade_produto, valor_produto, *args):

        meu_aplicativo = App.get_running_app()

        self.Produto_Carrinho = nome_produto
        self.Valor_Carrinho = valor_produto
        self.Quantidade_Carrinho = quantidade_produto
        # pintar de branco todos os outros caras
        pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
        carrinho = pagina_carrinho.ids["lista_compra"]
        for item in list(carrinho.children):
            try:
                texto = item.text
                if nome_produto in texto:
                    pagina_mudanca = meu_aplicativo.root.ids["mudarpedido"]
                    pagina_mudanca.ids["id_Produto"].text = f"{self.Produto_Carrinho}"
                    pagina_mudanca.ids["id_Quantidade"].text = f"Quantidade: {self.Quantidade_Carrinho}"
                    pagina_mudanca.ids["id_Valor"].text = f"R$ {self.Valor_Carrinho: ,.2f}"
                    pagina_mudanca.ids["quantidade"].text = f"{self.Quantidade_Carrinho}"
                    meu_aplicativo.mudar_tela("mudarpedido")
            except:
                pass

    def limpar_carrinho(self):

        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
        carrinho = pagina_carrinho.ids["lista_compra"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def __init__(self, **kwargs):
        self.id_vendedor = kwargs["id_vendedor"]

        meu_aplicativo = App.get_running_app()

        self.cols = 1
        super().__init__()

        try:
            self.limpar_carrinho()
            requisicao = requests.get(
                f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{self.id_vendedor}/Lista_Venda.json")
            requisicao_dic = requisicao.json()
            pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
            carrinho = pagina_carrinho.ids["lista_compra"]
            for id_Item in requisicao_dic:
                if id_Item != self.id_vendedor:
                    Produto_Carrinho = requisicao_dic[id_Item]["Produto"]
                    Quantidade_Carrinho = requisicao_dic[id_Item]["Quantidade"]
                    try:
                        Valor_Carrinho = float(requisicao_dic[id_Item]["Valor"])
                    except:
                        Valor_Carrinho = requisicao_dic[id_Item]["Valor"].replace(',', '')
                        Valor_Carrinho = float(Valor_Carrinho)

                    item = LabelButton(
                        text=f"{Produto_Carrinho} \n Quantidade: {Quantidade_Carrinho} \n R$ {Valor_Carrinho: ,.2f}",
                        size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                        on_release=partial(self.selecionar_item_carrinho, Produto_Carrinho, Quantidade_Carrinho,
                                           Valor_Carrinho))
                    carrinho.add_widget(item)

            requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{self.id_vendedor}/Lista_Venda/{self.id_vendedor}.json")
            requisicao_dic = requisicao.json()
            pagina_carrinho = meu_aplicativo.root.ids["carrinho"]
            try:
                Total = float(requisicao_dic['Total'])
            except:
                Total = requisicao_dic['Total'].replace(',', '')
                Total = float(Total)

            pagina_carrinho.ids["total_venda"].text = f"Total: {Total: ,.2f}"
        except:
            pass

        meu_aplicativo.mudar_tela("carrinho")