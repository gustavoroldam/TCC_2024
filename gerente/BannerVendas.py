from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from gerente.botoes import LabelButton
from pyautogui import alert

class BannerVendas(GridLayout):

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_vendas"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def Lista_Filtrada(self):
        meu_aplicativo = App.get_running_app()

        Tela_vendas = meu_aplicativo.root.ids["gerenciarvendas"]
        vendas = Tela_vendas.ids["lista_vendas"]

        Dic_Produtos = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        data_atual = datetime.now()
        data_atual = data_atual.strftime("%d/%m/%Y")
        dia, mes_atual, ano_atual = map(int, data_atual.split('/'))

        for id in Dic_Produtos:
            if id != "Proximo_Id":

                Nome = Dic_Produtos[id]["Nome"]

                texto = f"{Nome}"

                Dic_Vendas = meu_aplicativo.Requisicao_Get(
                    "https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Fechadas")
                Total_Venda = 0.0
                Qtde_Venda = 0
                for venda in Dic_Vendas:
                    for produto in Dic_Vendas[venda]["Produtos"]:
                        try:
                            if produto["Produto"] == Nome:
                                Data_Venda = Dic_Vendas[venda]["Data"]
                                dia, mes_venda, ano_venda = map(int, Data_Venda.split('/'))
                                Qtde_Venda += int(produto["Quantidade"])
                                Total_Venda += float(Dic_Vendas[venda]["Total"])
                        except:
                            pass
                try:
                    if mes_atual == mes_venda and ano_atual == ano_venda and Qtde_Venda != 0:
                        item = LabelButton(
                            text=texto,
                            markup=True,
                            halign='center',
                            valign='middle',
                            size_hint=(1, 0.2),
                            pos_hint={"right": 1, "top": 0.2},
                            color=(0, 0, 0, 1),
                        )
                        vendas.add_widget(item)

                        item = LabelButton(
                            text=f"{Qtde_Venda}",
                            markup=True,
                            halign='center',
                            valign='middle',
                            size_hint=(1, 0.2),
                            pos_hint={"right": 1, "top": 0.2},
                            color=(0, 0, 0, 1),
                        )
                        vendas.add_widget(item)

                        item = LabelButton(
                            text=f"{Total_Venda: ,.2f}",
                            markup=True,
                            halign='center',
                            valign='middle',
                            size_hint=(1, 0.2),
                            pos_hint={"right": 1, "top": 0.2},
                            color=(0, 0, 0, 1),
                        )
                        vendas.add_widget(item)
                except:
                    pass

    def Filtrar(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["gerenciarvendas"]
        fazer = pagina_carrinho.ids["filtro"].text

        if fazer == "ESSE MÊS":
            pagina_carrinho.ids["filtro"].text = "TUDO"
            BannerVendas.limpar_lista_produtos(self, "gerenciarvendas")
            BannerVendas.Lista_Filtrada(self)
        else:
            meu_aplicativo.Opcoes("gvendas")

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("gerenciarvendas")
        except:
            pass

        Tela_vendas = meu_aplicativo.root.ids["gerenciarvendas"]
        vendas = Tela_vendas.ids["lista_vendas"]

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
                )
                vendas.add_widget(item)

                Dic_Vendas = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Fechadas")
                Total_Venda = 0.0
                Qtde_Venda = 0
                for venda in Dic_Vendas:
                    for produto in Dic_Vendas[venda]["Produtos"]:
                        try:
                            if produto["Produto"] == Nome:
                                Qtde_Venda += int(produto["Quantidade"])
                                Total_Venda += float(Dic_Vendas[venda]["Total"])
                        except:
                            pass

                item = LabelButton(
                    text=f"{Qtde_Venda}",
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                )
                vendas.add_widget(item)

                item = LabelButton(
                    text=f"{Total_Venda: ,.2f}",
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                )
                vendas.add_widget(item)