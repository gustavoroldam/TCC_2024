import pyautogui
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton

class BannerProdutos(GridLayout):

    def limpar_lista_produtos(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["homepage"]
        carrinho = pagina_carrinho.ids["lista_produtos"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_lista_produtos()
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
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                )
                vendas.add_widget(item)