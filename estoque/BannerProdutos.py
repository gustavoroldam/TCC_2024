import pyautogui
from datetime import datetime
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC_2023.estoque.botoes import LabelButton
from pyautogui import alert

class BannerProdutosDevolucao(GridLayout):

    def Devolver(self):
        meu_aplicativo = App.get_running_app()

        Nome = meu_aplicativo.Devolucao_Nome

        if Nome != None:
            tela = meu_aplicativo.root.ids["devolucao"]
            Texto = tela.ids["motivo_input"].text

            if Texto != '':
                Quantidade = int(tela.ids["quantidade"].text)
                Reutilizar = tela.ids["switch"].active

                data_atual = datetime.now()
                data_atual = data_atual.strftime("%d/%m/%Y")

                Dic_Devolucao = {"Produto": Nome, "Motivo": Texto, "Quantidade": Quantidade, "Reutilizado": Reutilizar, "Data": data_atual}

                requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Devolucoes', Dic_Devolucao)

                if Reutilizar == True:
                    Dic_Produtos = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')
                    for Produto in Dic_Produtos:
                        if Produto != "Proximo_Id":
                            if Dic_Produtos[Produto]["Nome"] == Nome:
                                Antiga_Qtde = int(Dic_Produtos[Produto]["Quantidade"])
                                Nova_Qtde = Antiga_Qtde + Quantidade
                                Dic_Nova_Quantidade = {"Quantidade": Nova_Qtde}
                                requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{Produto}', Dic_Nova_Quantidade)
                alert('Devolução Feita!')
                meu_aplicativo.mudar_tela("homepage")
            else:
                alert('Insira um motivo para a DEVOLUÇÃO!')
        else:
            alert('Nenhum produto SELECIONADO!')

    def limpar_lista_produtos(self, tela):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids[tela]
        carrinho = pagina_carrinho.ids["lista_produtos"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def Devolucao_Listar(self):
        meu_aplicativo = App.get_running_app()

        BannerProdutosDevolucao.limpar_lista_produtos(self, "devolucao")

        requisicao_dic = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        Tela_vendas = meu_aplicativo.root.ids["devolucao"]
        vendas = Tela_vendas.ids["lista_produtos"]

        for id in requisicao_dic:
            if id != 'Proximo_Id':
                Nome = requisicao_dic[id]["Nome"]
                Quantidade = requisicao_dic[id]["Quantidade"]
                Valor = float(requisicao_dic[id]["Valor"])

                texto = f"Nome: {Nome} \nQuantidade: {Quantidade} \nValor: R$ {Valor: ,.2f}"

                item = LabelButton(
                    text=texto,
                    halign='center',
                    valign='middle',
                    markup=True,
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(meu_aplicativo.Devolucao_Selecionar, Nome)
                )
                vendas.add_widget(item)

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos("homepage")
        except:
            pass

        requisicao_dic = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos")

        Tela_vendas = meu_aplicativo.root.ids["homepage"]
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
                )
                vendas.add_widget(item)