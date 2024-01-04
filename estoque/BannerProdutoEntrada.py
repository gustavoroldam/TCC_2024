import pyautogui
from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton
from pyautogui import alert

class BannerProdutosEntrada(GridLayout):

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_produtos"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def Filtrar(self):
        meu_aplicativo = App.get_running_app()

        BannerProdutosEntrada.limpar_lista_produtos(self, "entrada")

        requisicao_dic = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        Tela_vendas = meu_aplicativo.root.ids["entrada"]
        vendas = Tela_vendas.ids["lista_produtos"]

        requisicao_dic = [(chave, valor) for chave, valor in requisicao_dic.items() if chave != 'Proximo_Id' and 'Quantidade' in valor]
        requisicao_dic = sorted(requisicao_dic, key=lambda x: int(x[1]['Quantidade']))

        for chave, valor in requisicao_dic:
            Nome = valor["Nome"]
            Quantidade = valor["Quantidade"]
            Valor = float(valor["Valor"])

            texto = f"Nome: {Nome} \nQuantidade: {Quantidade} \nValor: R$ {Valor: ,.2f}"

            item = LabelButton(
                text=texto,
                markup=True,
                halign='center',
                valign='middle',
                size_hint=(1, 0.2),
                pos_hint={"right": 1, "top": 0.2},
                color=(0, 0, 0, 1),
                on_release=partial(meu_aplicativo.Entrada_Selecionar, Nome)
            )
            vendas.add_widget(item)

    def GravarEntrada(self, fazer):
        meu_aplicativo = App.get_running_app()

        Nome = meu_aplicativo.Entrada_Nome

        if Nome != None:
            tela = meu_aplicativo.root.ids["entrada"]
            Quantidade = int(tela.ids["quantidade"].text)

            Dic_Produtos = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')
            for Produto in Dic_Produtos:
                if Produto != "Proximo_Id":
                    if Dic_Produtos[Produto]["Nome"] == Nome:
                        Antiga_Qtde = int(Dic_Produtos[Produto]["Quantidade"])
                        data_atual = datetime.now()
                        data_atual = data_atual.strftime("%d/%m/%Y")
                        if fazer == True:
                            Nova_Qtde = Antiga_Qtde + Quantidade
                            Dic_Relatorio = {"Funcionario": meu_aplicativo.nome_Estoque, "Produto": Nome, "Quantidade": Quantidade, "Alteracao": "Entrada", "Data": data_atual}
                            requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Movimentacao', Dic_Relatorio)
                        else:
                            Nova_Qtde = Antiga_Qtde - Quantidade
                            Dic_Relatorio = {"Funcionario": meu_aplicativo.nome_Estoque, "Produto": Nome, "Quantidade": Quantidade, "Alteracao": "Saida", "Data": data_atual}
                            requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Movimentacao', Dic_Relatorio)
                        Dic_Nova_Quantidade = {"Quantidade": Nova_Qtde}
                        requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{Produto}',Dic_Nova_Quantidade)
            alert('Alteração Feita!')
            meu_aplicativo.mudar_tela("homepage")
        else:
            alert('Selecione um PRODUTO primeiro!')

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("entrada")
        except:
            pass

        requisicao_dic = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        Tela_vendas = meu_aplicativo.root.ids["entrada"]
        vendas = Tela_vendas.ids["lista_produtos"]

        for id in requisicao_dic:
            if id != 'Proximo_Id':
                Nome = requisicao_dic[id]["Nome"]
                Quantidade = requisicao_dic[id]["Quantidade"]
                Valor = float(requisicao_dic[id]["Valor"])

                texto = f"Nome: {Nome} \nQuantidade: {Quantidade} \nValor: R$ {Valor: ,.2f}"

                item = LabelButton(
                    text=texto,
                    markup=True,
                    halign='center',
                    valign='middle',
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(meu_aplicativo.Entrada_Selecionar, Nome)
                )
                vendas.add_widget(item)