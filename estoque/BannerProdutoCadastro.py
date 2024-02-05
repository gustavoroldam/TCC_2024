from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC_2023.estoque.botoes import LabelButton
from pyautogui import alert

class BannerProdutoCadastro(GridLayout):

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        tela = meu_aplicativo.root.ids["cadastrar"]

        Nome = tela.ids["nome_input"].text

        if Nome != '':
            Valor = tela.ids["valor_input"].text
            try:
                Valor = float(Valor)
            except:
                try:
                    Valor = Valor.replace(',', '.')
                except:
                    Valor = ''
            if Valor != '':
                Quantidade = tela.ids["qtde_input"].text
                try:
                    Quantidade = int(Quantidade)
                except:
                    Quantidade = ''
                if Quantidade != '':
                    Dic_Cadastro = {"Nome": Nome, "Quantidade": Quantidade, "Valor": Valor}
                    Proximo_Id = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/Proximo_Id')
                    requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{Proximo_Id}', Dic_Cadastro)
                    Proximo_Id += 1
                    Dic_Proximo_Id = {"Proximo_Id": Proximo_Id}
                    requisicao = meu_aplicativo.Requisicao_Patch('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos', Dic_Proximo_Id)
                    alert('Produto gravado com SUCESSO!')
                    meu_aplicativo.bannerprodutos('atualizar')
                else:
                    alert('Campo QUANTIDADE vazio ou incorreto')
            else:
                alert('Campo VALOR vazio ou incorreto!')
        else:
            alert('Campo NOME vazio!')