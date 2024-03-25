from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC_2023.vendedor.botoes import LabelButton
import requests
import json


class BannerProdutos(GridLayout):

    def ModificarQuantidade(self, fazer):

        meu_aplicativo = App.get_running_app()

        if fazer == 1:
            novo_valor = meu_aplicativo.root.ids["homepage"]
            valor = int(novo_valor.ids["quantidade"].text)
            valor = valor + 1
            novo_valor.ids["quantidade"].text = f"{valor}"
        elif fazer == -1:
            novo_valor = meu_aplicativo.root.ids["homepage"]
            valor = int(novo_valor.ids["quantidade"].text)
            if valor > 0:
                valor = valor - 1
            novo_valor.ids["quantidade"].text = f"{valor}"

    # Carregar Infos do Carrinho
    def adicionar_carrinho(self):

        meu_aplicativo = App.get_running_app()

        if self.nome_produto != None:
            pagina_home = meu_aplicativo.root.ids["homepage"]
            lista_produtos = pagina_home.ids["lista_produtos"]
            for item in list(lista_produtos.children):
                item.color = (0, 0, 0, 1)

            requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda.json")
            requisicao_dic = requisicao.json()

            Produto = meu_aplicativo.nome_produto
            Valor = meu_aplicativo.valor_produto
            pagina_home = meu_aplicativo.root.ids["homepage"]
            Quantidade = pagina_home.ids["quantidade"]

            if requisicao_dic != None:
                aprovado = True
                for item in requisicao_dic:
                    Dic_Produto = requisicao_dic[item]
                    try:
                        if Produto in Dic_Produto["Produto"]:
                            aprovado = False
                            erro = meu_aplicativo.root.ids["homepage"]
                            erro.ids["id_nome_vendedor"].text = "Produto já está na lista!"
                            erro.ids["id_nome_vendedor"].color = (1, 0, 0, 1)
                    except:
                        pass
                if aprovado == True:
                    requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
                    Produto_Dic = requisicao.json()
                    for id in Produto_Dic:
                        if id != "Proximo_Id" and Produto_Dic[id]["Nome"] == Produto:
                            Nova_Qtde = int(Produto_Dic[id]["Quantidade"]) - int(Quantidade.text)
                            if Nova_Qtde > 0:
                                Valor = Valor * (float(Quantidade.text))
                                dados = {'Produto': f'{Produto}', 'Valor': f'{Valor: ,.2f}', 'Quantidade': f'{Quantidade.text}'}
                                requisicao = requests.post(
                                    f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/.json",
                                    data=json.dumps(dados))
                                if requisicao.ok:

                                    requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}.json")
                                    requisicao_dic = requisicao.json()

                                    try:
                                        Valor += float(requisicao_dic["Total"])
                                    except:
                                        Total = requisicao_dic["Total"].replace(',', '')
                                        Total = float(Total)

                                    Dic_Total = {'Total': f'{Valor: ,.2f}'}

                                    requisicao = requests.patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}/.json", data=json.dumps(Dic_Total))
                                    if requisicao.ok:
                                        nome_perfil = meu_aplicativo.root.ids["homepage"]
                                        nome_perfil.ids["id_nome_vendedor"].text = f"Vendedor {meu_aplicativo.nome}"
                                        nome_perfil.ids["id_nome_vendedor"].color = (0, 0, 0, 1)

                                        novo_valor = meu_aplicativo.root.ids["homepage"]
                                        novo_valor.ids["quantidade"].text = "1"
                                    else:
                                        erro = meu_aplicativo.root.ids["homepage"]
                                        erro.ids["id_nome_vendedor"].text = f"{requisicao.text}"
                                        erro.ids["id_nome_vendedor"].color = (1, 0, 0, 1)
                                else:
                                    erro = meu_aplicativo.root.ids["homepage"]
                                    erro.ids["id_nome_vendedor"].text = f"{requisicao.text}"
                                    erro.ids["id_nome_vendedor"].color = (1, 0, 0, 1)
                            else:
                                erro = meu_aplicativo.root.ids["homepage"]
                                erro.ids["id_nome_vendedor"].text = "Produto em falta!"
                                erro.ids["id_nome_vendedor"].color = (1, 0, 0, 1)
            else:
                pass
        else:
            erro = meu_aplicativo.root.ids["homepage"]
            erro.ids["id_nome_vendedor"].text = "Selecione o produto primeiro!"
            erro.ids["id_nome_vendedor"].color = (1, 0, 0, 1)
        self.nome_produto = None

    # Funções para poder selecionar o Produto
    def selecionar_produto(self, nome_produto, valor_produto, *args):

        meu_aplicativo = App.get_running_app()

        meu_aplicativo.nome_produto = nome_produto
        meu_aplicativo.valor_produto = valor_produto
        # pintar de branco todos os outros caras
        pagina_home = meu_aplicativo.root.ids["homepage"]
        lista_produtos = pagina_home.ids["lista_produtos"]
        for item in list(lista_produtos.children):
            item.color = (0, 0, 0, 1)
            # pintar de azul a letra do item selecionado
            try:
                texto = item.text
                if nome_produto in texto:
                    item.color = (1, 1, 1, 1)
            except:
                pass

    def limpar(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["homepage"]
        carrinho = pagina_carrinho.ids["lista_produtos"]
        try:
            for item in list(carrinho.children):
                carrinho.remove_widget(item)
        except:
            pass

    def __init__(self):

        meu_aplicativo = App.get_running_app()

        self.rows = 1
        super().__init__()

        self.limpar()

        requisicao = requests.get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json")
        requisicao_dic = requisicao.json()
        produtos = requisicao_dic
        pagina_homepage = meu_aplicativo.root.ids["homepage"]
        lista_produtos = pagina_homepage.ids["lista_produtos"]
        for id in produtos:
            if id != "Proximo_Id":
                nome = produtos[id]["Nome"]
                valor = produtos[id]["Valor"]
                quantidade = produtos[id]["Quantidade"]
                item = LabelButton(text=f"{nome} \n R$ {valor: ,.2f} \n Quantidade: {quantidade}",
                                   pos_hint={"right": 1, "top": 0.2}, color=(0, 0, 0, 1),
                                   on_release=partial(self.selecionar_produto, nome, valor))
                lista_produtos.add_widget(item)