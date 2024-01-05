from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton
from pyautogui import alert

class BannerVendedores(GridLayout):

    def GravarComissao(self):
        meu_aplicativo = App.get_running_app()

        tela = meu_aplicativo.root.ids["gerenciarvendedores"]
        comissao = tela.ids["comissao_input"].text
        Dic_Comissao = {"Comissao": comissao}
        requisicao = meu_aplicativo.Requisicao_Patch('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Financeiro/Vendedor', Dic_Comissao)
        alert('Alteração realizadas para futuras vendas!')

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_vendas_vendedores"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def Lista_Filtrada(self):
        meu_aplicativo = App.get_running_app()

        Tela_vendas = meu_aplicativo.root.ids["gerenciarvendedores"]
        vendas = Tela_vendas.ids["lista_vendas_vendedores"]

        Dic_Produtos = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        data_atual = datetime.now()
        data_atual = data_atual.strftime("%d/%m/%Y")
        dia, mes_atual, ano_atual = map(int, data_atual.split('/'))

        Dic_Vendedor = meu_aplicativo.Requisicao_Get(
            "https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor")

        for id in Dic_Vendedor:

            Nome = Dic_Vendedor[id]["Nome"]

            texto = f"{Nome}"

            Comissao = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Financeiro/Vendedor/Comissao')
            Comissao_Total = float(Dic_Vendedor[id]["Comissao"])

            Dic_Vendas = meu_aplicativo.Requisicao_Get(
                "https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Fechadas")
            Total_Venda = 0.0
            for venda in Dic_Vendas:
                if Dic_Vendas[venda]["Vendedor"] == id:
                    data_venda = Dic_Vendas[venda]["Data"]
                    dia, mes_venda, ano_venda = map(int, data_venda.split('/'))
                    if mes_atual == mes_venda and ano_atual == ano_venda:
                        Total_Venda += float(Dic_Vendas[venda]["Total"])
                    else:
                        Comissao_Total -= float(Dic_Vendas[venda]["Total"]) * (float(Comissao)/100)

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
                text=f"{Total_Venda: ,.2f}",
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
            )
            vendas.add_widget(item)

            item = LabelButton(
                text=f'{Comissao_Total: ,.2f}',
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
            )
            vendas.add_widget(item)

    def Filtrar(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["gerenciarvendedores"]
        fazer = pagina_carrinho.ids["filtro"].text

        if fazer == "ESSE MÊS":
            pagina_carrinho.ids["filtro"].text = "TUDO"
            BannerVendedores.limpar_lista_produtos(self, "gerenciarvendedores")
            BannerVendedores.Lista_Filtrada(self)
        else:
            meu_aplicativo.Opcoes("gvendedores")

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("gerenciarvendedores")
        except:
            pass

        Tela_vendas = meu_aplicativo.root.ids["gerenciarvendedores"]
        vendas = Tela_vendas.ids["lista_vendas_vendedores"]

        Comissao = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Financeiro/Vendedor/Comissao')
        Dic_Vendedor = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor")

        Tela_vendas.ids["comissao_input"].text = f"{Comissao}"

        for id in Dic_Vendedor:

            Nome = Dic_Vendedor[id]["Nome"]

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
            for venda in Dic_Vendas:
                if Dic_Vendas[venda]["Vendedor"] == id:
                    Total_Venda += float(Dic_Vendas[venda]["Total"])
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

            Comissao = float(Dic_Vendedor[id]["Comissao"])
            item = LabelButton(
                text=f'{Comissao: ,.2f}',
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
            )
            vendas.add_widget(item)