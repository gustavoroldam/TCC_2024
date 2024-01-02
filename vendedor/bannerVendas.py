import re
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC.vendedor.botoes import LabelButton
import requests
import json

class BannerVendas(GridLayout):

    def Deletar_Item(self):
        meu_aplicativo = App.get_running_app()

        Tela = meu_aplicativo.root.ids["visualizarvenda"]
        Id_Venda = Tela.ids["id_venda"].text
        Id_Venda = re.search(r'\d+', Id_Venda).group()
        Tela = meu_aplicativo.root.ids["editarvendafeita"]
        Nome_Produto = Tela.ids["id_Produto"].text
        Qtde_Produto = Tela.ids["id_Quantidade"].text
        Qtde_Produto = int(re.search(r'\d+', Qtde_Produto).group())
        Valor_Produto = Tela.ids["id_Valor"].text
        Valor_Produto = int(re.search(r'\d+', Valor_Produto).group())

        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json')
        Dic_Vendas = requisicao.json()
        for venda in Dic_Vendas:
            if venda != 'Proxima_Venda':
                IdV = int(Dic_Vendas[venda]["Id"])
                if IdV == int(Id_Venda):
                    Total = float(Dic_Vendas[venda]["Total"])
                    Total = Total - Valor_Produto
                    Dic_Novo_Total = {"Total":f"{Total}"}
                    requisicao = requests.patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}.json', data=json.dumps(Dic_Novo_Total))
                    Dic_Produtos = Dic_Vendas[venda]["Produtos"]
                    Dic_Produtos_Sem_None = list(filter(None, Dic_Produtos))
                    # Obtém o número de produtos na lista
                    numero_de_produtos = len(Dic_Produtos_Sem_None)
                    if numero_de_produtos > 1:
                        for produto in Dic_Produtos:
                            if produto != None and produto["Produto"] == Nome_Produto:
                                requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
                                requisicao_Dic = requisicao.json()
                                posicao_produto = next((i for i, d in enumerate(Dic_Produtos) if d and d.get('Produto') == Nome_Produto), None)
                                for Id_Produto in requisicao_Dic:
                                    if Id_Produto != 'Proximo_Id':
                                        if requisicao_Dic[Id_Produto]["Nome"] == Nome_Produto:
                                            qtde = int(requisicao_Dic[Id_Produto]["Quantidade"])
                                            qtde = qtde + Qtde_Produto
                                            Nova_Qtde = {"Quantidade":f"{qtde}"}
                                            requisicao = requests.patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{Id_Produto}/.json', data=json.dumps(Nova_Qtde))
                                            requisicao = requests.delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/Produtos/{posicao_produto}.json')
                    else:
                        meu_aplicativo.Venda("Excluir")
        meu_aplicativo.Venda("Carregar")

    def Adicionar_Produto(self):
        meu_aplicativo = App.get_running_app()

        NomeProduto = meu_aplicativo.adicionar_nome_produto
        Tela = meu_aplicativo.root.ids["adicionarprodutodavenda"]
        QtdeVenda = int(Tela.ids['quantidade'].text)
        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
        Dic_Produto = requisicao.json()
        for idProduto in Dic_Produto:
            if idProduto != 'Proximo_Id':
                if Dic_Produto[idProduto]['Nome'] == NomeProduto:
                    QtdeEstoque = int(Dic_Produto[idProduto]['Quantidade'])
                    Valor = float(Dic_Produto[idProduto]['Valor'])

                    if (QtdeEstoque-QtdeVenda) > 0:
                        Tela.ids["adicionarBt"].text = "Adicionar"
                        Tela.ids["adicionarBt"].color = (0, 0, 0, 1)

                        NovaQtde = QtdeEstoque-QtdeVenda
                        Dic_Qtde = {"Quantidade":f"{NovaQtde}"}
                        requisicao = requests.patch(
                            f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{idProduto}/.json",
                            data=json.dumps(Dic_Qtde))

                        Tela = meu_aplicativo.root.ids["visualizarvenda"]
                        Id_Venda = Tela.ids["id_venda"].text
                        Id_Venda = int(re.search(r'\d+', Id_Venda).group())
                        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json')
                        Dic_Vendas = requisicao.json()
                        for venda in Dic_Vendas:
                            if venda != 'Proxima_Venda':
                                IdV = int(Dic_Vendas[venda]["Id"])
                                if IdV == int(Id_Venda):
                                    id = 0
                                    Dic_Aux = Dic_Vendas[venda]
                                    Total = float(Dic_Aux["Total"])
                                    ValorProduto = Valor * QtdeVenda
                                    Total = Total + ValorProduto
                                    for i in Dic_Vendas[venda]["Produtos"]:
                                        id += 1
                                    Dic_Total = {"Total":f"{Total}"}
                                    Dic_Novo_Produto = {id:{"Produto":f"{NomeProduto}","Quantidade":f"{QtdeVenda}","Valor":f"{ValorProduto}"}}

                                    requisicao = requests.patch(
                                        f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/.json",
                                        data=json.dumps(Dic_Total))
                                    requisicao = requests.patch(
                                        f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/Produtos/.json",
                                        data=json.dumps(Dic_Novo_Produto))
                                    meu_aplicativo.adicionar_nome_produto = None
                    else:
                        Tela.ids["adicionarBt"].text = "Falta de Estoque"
                        Tela.ids["adicionarBt"].color = (1, 0, 0, 1)

        meu_aplicativo.Venda("Carregar")

    def ModificarQuantidade_Produto(self, fazer):

        meu_aplicativo = App.get_running_app()

        if fazer == 1:
            novo_valor = meu_aplicativo.root.ids["adicionarprodutodavenda"]
            valor = int(novo_valor.ids["quantidade"].text)
            valor = valor + 1
            novo_valor.ids["quantidade"].text = f"{valor}"
        elif fazer == -1:
            novo_valor = meu_aplicativo.root.ids["adicionarprodutodavenda"]
            valor = int(novo_valor.ids["quantidade"].text)
            if valor > 1:
                valor = valor - 1
            novo_valor.ids["quantidade"].text = f"{valor}"

    def Adicionar(self):
        meu_aplicativo = App.get_running_app()
        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
        dic_Produto = requisicao.json()

        try:
            meu_aplicativo.Limpar_Selecionar_Produto_Venda()
        except:
            pass

        id_Venda = meu_aplicativo.root.ids["visualizarvenda"]
        id_Venda = id_Venda.ids["id_venda"].text
        id_Venda = int(re.search(r'\d+', id_Venda).group())
        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json')
        Dic_Vendas = requisicao.json()

        for venda in Dic_Vendas:
            if venda != 'Proxima_Venda':
                if int(Dic_Vendas[venda]['Id']) == id_Venda:
                    lista_Produto = meu_aplicativo.root.ids["adicionarprodutodavenda"]
                    lista_Produto = lista_Produto.ids["lista_produtos"]
                    lista = Dic_Vendas[venda]['Produtos']
                    lista = list(filter(None, lista))
                    nomes_produtos_filtrar = {item['Produto'] for item in lista}
                    lista_filtrada = {k: v for k, v in dic_Produto.items() if isinstance(v, dict) and v.get('Nome') not in nomes_produtos_filtrar}

                    for item in lista_filtrada:
                        nome = lista_filtrada[item]["Nome"]
                        valor = lista_filtrada[item]["Valor"]
                        quantidade = lista_filtrada[item]["Quantidade"]
                        item = LabelButton(text=f"{nome} \n R$ {valor: ,.2f} \n Quantidade: {quantidade}",
                                           pos_hint={"right": 1, "top": 0.2}, color=(0, 0, 0, 1),
                                           on_release=partial(self.Selecionar_Produto_Venda, nome))
                        lista_Produto.add_widget(item)

        meu_aplicativo.mudar_tela("adicionarprodutodavenda")

    def excluir(self):
        meu_aplicativo = App.get_running_app()
        pagina = meu_aplicativo.root.ids["visualizarvenda"]
        Id_Compra = pagina.ids["id_venda"].text
        Id_Compra = re.search(r'\d+', Id_Compra).group()

        requisicao = requests.get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json')
        requisicao_dic = requisicao.json()

        for id in requisicao_dic:
            if id != 'Proxima_Venda' and requisicao_dic[id]["Id"] == Id_Compra:
                requisicao = requests.get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
                Produtos_Dic = requisicao.json()
                for Produto in requisicao_dic[id]["Produtos"]:
                    for id_Produto in Produtos_Dic:
                        try:
                            if id_Produto != "Proximo_Id" and Produtos_Dic[id_Produto]["Nome"] == Produto["Produto"]:
                                qtde_estoque = int(Produtos_Dic[id_Produto]["Quantidade"])
                                qtde_venda = int(Produto["Quantidade"])
                                qtde_nova = qtde_estoque + qtde_venda
                                Dic_Nova_Qtde = {'Quantidade':f'{qtde_nova}'}
                                requisicao = requests.patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{id_Produto}/.json', data=json.dumps(Dic_Nova_Qtde))
                        except:
                            pass
                requisicao = requests.delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id}.json')

        meu_aplicativo.Venda("Carregar")

    def ModificarQuantidade_Carrinho(self, fazer):

        meu_aplicativo = App.get_running_app()

        produto = meu_aplicativo.root.ids["editarvendafeita"]
        Produto_Carrinho = produto.ids["id_Produto"].text

        if fazer == 1:
            novo_valor = meu_aplicativo.root.ids["editarvendafeita"]
            valor = int(novo_valor.ids["quantidade"].text)
            valor = valor + 1
            novo_valor.ids["quantidade"].text = f"{valor}"
        elif fazer == -1:
            novo_valor = meu_aplicativo.root.ids["editarvendafeita"]
            valor = int(novo_valor.ids["quantidade"].text)
            if valor > 1:
                valor = valor - 1
            novo_valor.ids["quantidade"].text = f"{valor}"

        novo_valor = meu_aplicativo.root.ids["editarvendafeita"]
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

    def selecionar_produto(self, nome, qtde, valor, *args):
        meu_aplicativo = App.get_running_app()

        pagina = meu_aplicativo.root.ids["editarvendafeita"]
        pagina.ids["id_Produto"].text = nome
        pagina.ids["id_Quantidade"].text = f"Quantidade: {qtde}"
        pagina.ids["quantidade"].text = f"{qtde}"
        pagina.ids["id_Valor"].text = f"R$ {valor}"

        meu_aplicativo.mudar_tela("editarvendafeita")

    def limpar_venda_selecionada(self):
        meu_aplicativo = App.get_running_app()

        pagina = meu_aplicativo.root.ids["visualizarvenda"]
        carrinho = pagina.ids["lista_compra"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def selecionar_item(self, Id_Compra, ID_Link, *args):
        meu_aplicativo = App.get_running_app()
        meu_aplicativo.Id_Link = ID_Link
        pagina = meu_aplicativo.root.ids["visualizarvenda"]
        pagina.ids["id_venda"].text = f"Venda: {Id_Compra}"
        carrinho = pagina.ids["lista_compra"]
        try:
            self.limpar_venda_selecionada()
        except:
            pass

        requisicao = requests.get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json')
        requisicao_dic = requisicao.json()

        for id in requisicao_dic:
            if id != 'Proxima_Venda' and requisicao_dic[id]["Id"] == Id_Compra:
                pagina.ids["total_venda"].text = f"Total: {requisicao_dic[id]['Total']}"
                for Produto in requisicao_dic[id]["Produtos"]:
                    try:
                        nome = Produto['Produto']
                        qtde = Produto['Quantidade']
                        valor = Produto['Valor']

                        item = LabelButton(
                            text=f"Produto: {nome}\n Quantidade: {qtde}\n Valor Total:{valor}",
                            size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2},
                            color=(0, 0, 0, 1),
                            on_release=partial(self.selecionar_produto, nome, qtde, valor))
                        carrinho.add_widget(item)
                    except:
                        pass

        meu_aplicativo.mudar_tela("visualizarvenda")

    def Salvar_Alteracao(self):

        meu_aplicativo = App.get_running_app()
        id_venda = meu_aplicativo.Id_Link

        tela_mudanca = meu_aplicativo.root.ids["editarvendafeita"]
        Produto = tela_mudanca.ids["id_Produto"].text
        Quantidade_Nova = tela_mudanca.ids["quantidade"].text

        Quantidade_Antiga = tela_mudanca.ids["id_Quantidade"].text
        Quantidade_Antiga = re.search(r'\d+', Quantidade_Antiga).group()
        Quantidade_Antiga = int(Quantidade_Antiga)

        Valor = tela_mudanca.ids["id_Valor"].text
        Valor = re.search(r'\d+', Valor).group()
        Valor = float(Valor)

        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
        Produto_Dic = requisicao.json()
        for id in Produto_Dic:
            if id != "Proximo_Id" and Produto_Dic[id]["Nome"] == Produto:
                Nova_Qtde = (int(Produto_Dic[id]["Quantidade"]) + int(Quantidade_Antiga)) - int(Quantidade_Nova)
                if Nova_Qtde > 0:

                    Nova_Qtde_Dic = {'Quantidade':f'{Nova_Qtde}'}
                    requisicao = requests.patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{id}.json',
                                                data=json.dumps(Nova_Qtde_Dic))

                    tela = meu_aplicativo.root.ids["editarvendafeita"]
                    tela.ids["salvar_sair"].text = "Salvar e Sair"
                    tela.ids["salvar_sair"].color = (1, 1, 1, 1)

                    requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}.json")
                    requisicao_dic = requisicao.json()

                    Total = float(requisicao_dic["Total"])

                    requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/Produtos.json")
                    requisicao_dic = requisicao.json()

                    indice = 0
                    for id in requisicao_dic:
                        if id != None:
                            if id["Produto"] == Produto:

                                Total -= float(id["Valor"])
                                Total += Valor
                                Dic_Total = {'Total':f'{Total}'}
                                requisicao = requests.patch(
                                    f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/.json",
                                    data=json.dumps(Dic_Total))
                                pagina_carrinho = meu_aplicativo.root.ids["visualizarvenda"]
                                pagina_carrinho.ids["total_venda"].text = f"Total: {Total}"

                                dados = {'Quantidade': Quantidade_Nova, 'Valor': Valor}
                                requisicao = requests.patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/Produtos/{indice}/.json", data=json.dumps(dados))
                        indice += 1
                    pagina = meu_aplicativo.root.ids["visualizarvenda"]
                    cod_venda = re.search(r'\d+', pagina.ids["id_venda"].text).group()
                    meu_aplicativo.Venda("SalvarAlteracao",Codigo=cod_venda, Link=id_venda)
                else:
                    tela = meu_aplicativo.root.ids["editarvendafeita"]
                    tela.ids["salvar_sair"].text = "Falta de Estoque"
                    tela.ids["salvar_sair"].color = (1, 0, 0, 1)

    def limpar_vendas(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["listarvendas"]
        carrinho = pagina_carrinho.ids["lista_vendas"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        self.limpar_vendas()

        try:
            requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json')
            requisicao_dic = requisicao.json()

            Tela_vendas = meu_aplicativo.root.ids["listarvendas"]
            vendas = Tela_vendas.ids["lista_vendas"]

            for id in requisicao_dic:
                if id != 'Proxima_Venda':
                    Id = requisicao_dic[id]['Id']
                    Total = float(requisicao_dic[id]['Total'])
                    produtos = requisicao_dic[id].get('Produtos', [])
                    produtos = list(filter(None, produtos))
                    Quantidade_Produto = len(produtos)

                    requisicao = requests.get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{requisicao_dic[id]["Vendedor"]}.json')
                    Dic_Vendedor = requisicao.json()

                    item = LabelButton(
                        text=f"ID: {Id} Vendedor: {Dic_Vendedor['Nome']} \n Quantidade de Itens: {Quantidade_Produto} \n Total: R$ {Total: ,.2f}",
                        size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                        on_release=partial(self.selecionar_item, Id, id))
                    vendas.add_widget(item)
        except:
            pass

        meu_aplicativo.mudar_tela("listarvendas")
