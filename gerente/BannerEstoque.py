from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton
from pyautogui import alert

class BannerEstoque(GridLayout):

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_vendas"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def Listar_Motivos(self):
        meu_aplicativo = App.get_running_app()

        BannerEstoque.limpar_lista_produtos(self, "motivos")

        tela = meu_aplicativo.root.ids["motivos"]
        lista = tela.ids["lista_vendas"]

        tela.ids["filtro"].text = "ESSE MÊS"

        Dic_Motivos = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Devolucoes')

        for devolucao in Dic_Motivos:
            if Dic_Motivos[devolucao]["Produto"] == meu_aplicativo.Nome_Motivo:
                texto = f"{Dic_Motivos[devolucao]['Data']}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                )
                lista.add_widget(item)

                texto = f"{Dic_Motivos[devolucao]['Motivo']}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                )
                lista.add_widget(item)

                texto = f"{Dic_Motivos[devolucao]['Quantidade']}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                )
                lista.add_widget(item)

                if Dic_Motivos[devolucao]['Reutilizado'] == False:
                    item = LabelButton(
                        text="Não",
                        markup=True,
                        halign='center',
                        valign='middle',
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                    )
                    lista.add_widget(item)
                else:
                    item = LabelButton(
                        text="Sim",
                        markup=True,
                        halign='center',
                        valign='middle',
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                    )
                    lista.add_widget(item)

        meu_aplicativo.mudar_tela("motivos")

    def Filtrar_Motivo(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["motivos"]
        fazer = pagina_carrinho.ids["filtro"].text

        if fazer == "ESSE MÊS":
            pagina_carrinho.ids["filtro"].text = "TUDO"
            BannerEstoque.limpar_lista_produtos(self, "motivos")
            BannerEstoque.Lista_Motivos_Filtrada(self)
        else:
            BannerEstoque.Listar_Motivos(self)

    def Lista_Motivos_Filtrada(self):
        meu_aplicativo = App.get_running_app()

        data_atual = datetime.now()
        data_atual = data_atual.strftime("%d/%m/%Y")
        dia, mes_atual, ano_atual = map(int, data_atual.split('/'))

        tela = meu_aplicativo.root.ids["motivos"]
        lista = tela.ids["lista_vendas"]

        Dic_Motivos = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Devolucoes')

        for devolucao in Dic_Motivos:
            if Dic_Motivos[devolucao]["Produto"] == meu_aplicativo.Nome_Motivo:

                data_motivo = Dic_Motivos[devolucao]['Data']
                dia, mes_motivo, ano_motivo = map(int, data_motivo.split('/'))

                if mes_atual == mes_motivo and ano_atual == ano_motivo:
                    texto = f"{Dic_Motivos[devolucao]['Data']}"

                    item = LabelButton(
                        text=texto,
                        markup=True,
                        halign='center',
                        valign='middle',
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                    )
                    lista.add_widget(item)

                    texto = f"{Dic_Motivos[devolucao]['Motivo']}"

                    item = LabelButton(
                        text=texto,
                        markup=True,
                        halign='center',
                        valign='middle',
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                    )
                    lista.add_widget(item)

                    texto = f"{Dic_Motivos[devolucao]['Quantidade']}"

                    item = LabelButton(
                        text=texto,
                        markup=True,
                        halign='center',
                        valign='middle',
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                    )
                    lista.add_widget(item)

                    if Dic_Motivos[devolucao]['Reutilizado'] == False:
                        item = LabelButton(
                            text="Não",
                            markup=True,
                            halign='center',
                            valign='middle',
                            size_hint=(1, 0.2),
                            pos_hint={"right": 1, "top": 0.2},
                            color=(0, 0, 0, 1),
                        )
                        lista.add_widget(item)
                    else:
                        item = LabelButton(
                            text="Sim",
                            markup=True,
                            halign='center',
                            valign='middle',
                            size_hint=(1, 0.2),
                            pos_hint={"right": 1, "top": 0.2},
                            color=(0, 0, 0, 1),
                        )
                        lista.add_widget(item)

    def Lista_Filtrada(self):
        meu_aplicativo = App.get_running_app()

        data_atual = datetime.now()
        data_atual = data_atual.strftime("%d/%m/%Y")
        dia, mes_atual, ano_atual = map(int, data_atual.split('/'))

        Tela_vendas = meu_aplicativo.root.ids["gerenciarestoque"]
        vendas = Tela_vendas.ids["lista_vendas"]

        Dic_Produtos = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        for id in Dic_Produtos:
            if id != "Proximo_Id":

                Nome = Dic_Produtos[id]["Nome"]

                texto = f"{Nome}"

                Dic_Movimentacoes = meu_aplicativo.Requisicao_Get(
                    "https://tcc2023-9212b-default-rtdb.firebaseio.com/Movimentacao")
                Qtde_Saida = 0
                Qtde_Entrada = 0
                for movimentacao in Dic_Movimentacoes:
                    if Dic_Movimentacoes[movimentacao]["Produto"] == Nome:
                        if Dic_Movimentacoes[movimentacao]["Alteracao"] == "Entrada":
                            Qtde_Entrada += int(Dic_Movimentacoes[movimentacao]["Quantidade"])
                        else:
                            Qtde_Saida += int(Dic_Movimentacoes[movimentacao]["Quantidade"])

                        data_movimentacao = Dic_Movimentacoes[movimentacao]["Data"]
                        dia, mes_venda, ano_venda = map(int, data_movimentacao.split('/'))

                        if mes_atual == mes_venda and ano_atual == ano_venda:
                            item = LabelButton(
                                text=texto,
                                markup=True,
                                halign='center',
                                valign='middle',
                                size_hint=(1, 0.2),
                                pos_hint={"right": 1, "top": 0.2},
                                color=(0, 0, 0, 1),
                                on_release=partial(meu_aplicativo.Motivo, Nome)
                            )
                            vendas.add_widget(item)

                            item = LabelButton(
                                text=f"{Qtde_Entrada}",
                                markup=True,
                                halign='center',
                                valign='middle',
                                size_hint=(1, 0.2),
                                pos_hint={"right": 1, "top": 0.2},
                                color=(0, 0, 0, 1),
                                on_release=partial(meu_aplicativo.Motivo, Nome)
                            )
                            vendas.add_widget(item)

                            item = LabelButton(
                                text=f"{Qtde_Saida}",
                                markup=True,
                                halign='center',
                                valign='middle',
                                size_hint=(1, 0.2),
                                pos_hint={"right": 1, "top": 0.2},
                                color=(0, 0, 0, 1),
                                on_release=partial(meu_aplicativo.Motivo, Nome)
                            )
                            vendas.add_widget(item)

                            Dic_Devolucoes = meu_aplicativo.Requisicao_Get(
                                "https://tcc2023-9212b-default-rtdb.firebaseio.com/Devolucoes")
                            Qtde = 0
                            for devolucao in Dic_Devolucoes:
                                if Dic_Devolucoes[devolucao]["Produto"] == Nome:
                                    Qtde += int(Dic_Devolucoes[devolucao]["Quantidade"])

                            item = LabelButton(
                                text=f"{Qtde}",
                                markup=True,
                                halign='center',
                                valign='middle',
                                size_hint=(1, 0.2),
                                pos_hint={"right": 1, "top": 0.2},
                                color=(0, 0, 0, 1),
                                on_release=partial(meu_aplicativo.Motivo, Nome)
                            )
                            vendas.add_widget(item)

    def Filtrar(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["gerenciarestoque"]
        fazer = pagina_carrinho.ids["filtro"].text

        if fazer == "ESSE MÊS":
            pagina_carrinho.ids["filtro"].text = "TUDO"
            BannerEstoque.limpar_lista_produtos(self, "gerenciarestoque")
            BannerEstoque.Lista_Filtrada(self)
        else:
            meu_aplicativo.Opcoes("gestoque")

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("gerenciarestoque")
        except:
            pass

        Tela_vendas = meu_aplicativo.root.ids["gerenciarestoque"]
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
                    on_release=partial(meu_aplicativo.Motivo, Nome)
                )
                vendas.add_widget(item)

                Dic_Movimentacoes = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Movimentacao")
                Qtde_Saida = 0
                Qtde_Entrada = 0
                for movimentacao in Dic_Movimentacoes:
                    if Dic_Movimentacoes[movimentacao]["Produto"] == Nome:
                        if Dic_Movimentacoes[movimentacao]["Alteracao"] == "Entrada":
                            Qtde_Entrada += int(Dic_Movimentacoes[movimentacao]["Quantidade"])
                        else:
                            Qtde_Saida += int(Dic_Movimentacoes[movimentacao]["Quantidade"])

                item = LabelButton(
                    text=f"{Qtde_Entrada}",
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(meu_aplicativo.Motivo, Nome)
                )
                vendas.add_widget(item)

                item = LabelButton(
                    text=f"{Qtde_Saida}",
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(meu_aplicativo.Motivo, Nome)
                )
                vendas.add_widget(item)

                Dic_Devolucoes = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Devolucoes")
                Qtde = 0
                for devolucao in Dic_Devolucoes:
                    if Dic_Devolucoes[devolucao]["Produto"] == Nome:
                        Qtde += int(Dic_Devolucoes[devolucao]["Quantidade"])

                item = LabelButton(
                    text=f"{Qtde}",
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(meu_aplicativo.Motivo, Nome)
                )
                vendas.add_widget(item)