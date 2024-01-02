import re
from datetime import datetime
import pyautogui
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

    def Pagar(self):
        meu_aplicativo = App.get_running_app()

        Dic_Venda = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{meu_aplicativo.ID_Link}')
        Financeiro_Vendedor = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Financeiro/Vendedor')

        Dic_Vendedor = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{Dic_Venda["Vendedor"]}')
        Porcentagem_Comissao = (float(Financeiro_Vendedor["Comissao"]))/100
        Comissao = float(Dic_Venda["Total"]) * Porcentagem_Comissao
        Atual_Comissao = float(Dic_Vendedor["Comissao"])
        Nova_Comissao = Atual_Comissao + Comissao
        Dic_Comissao = {"Comissao":f"{Nova_Comissao}"}
        requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{Dic_Venda["Vendedor"]}', Dic_Comissao)

        Dic_Caixa = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Caixa/{meu_aplicativo.id_vendedor}')
        Vendas = int(Dic_Caixa["Vendas"])
        Vendas += 1
        Dic_Caixa_Venda = {"Vendas": Vendas}
        requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Caixa/{meu_aplicativo.id_vendedor}', Dic_Caixa_Venda)

        desconto = meu_aplicativo.Desconto
        data_atual = datetime.now()
        data_atual = data_atual.strftime("%d/%m/%Y")

        if meu_aplicativo.CPF_Valido == True:
            tela = meu_aplicativo.root.ids["pagarvenda"]
            cpf = tela.ids["cpf_input"].text
            Dic_Venda_Fechada = {"Id": Dic_Venda["Id"], "Produtos": Dic_Venda["Produtos"], "Total": Dic_Venda["Total"], "Vendedor": Dic_Venda["Vendedor"],
                                 "Caixa": meu_aplicativo.id_vendedor, "CPF": cpf, "Desconto": desconto, "Data": data_atual}
            if meu_aplicativo.Cupom_Valido == True:
                Dic_Clientes = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes')
                cupom = tela.ids["cupom_input"].text
                for Cliente in Dic_Clientes:
                    if Dic_Clientes[Cliente]["CPF"] == cpf:
                        Dic_Lista_Cupons = Dic_Clientes[Cliente]["Cupons"]
                        for Cupom in Dic_Lista_Cupons:
                            if Cupom == cupom:
                                requisicao = meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Clientes/{Cliente}/Cupons/{Cupom}')
        else:
            Dic_Venda_Fechada = {"Id": Dic_Venda["Id"], "Produtos": Dic_Venda["Produtos"], "Total": Dic_Venda["Total"],
                                 "Vendedor": Dic_Venda["Vendedor"],
                                 "Caixa": meu_aplicativo.id_vendedor, "CPF": "Não Informado", "Desconto": desconto, "Data": data_atual}

        requisicao = meu_aplicativo.Requisicao_Post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Fechadas/', Dic_Venda_Fechada)
        requisicao = meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{meu_aplicativo.ID_Link}')
        pyautogui.alert("Compra Finalizada com Sucesso!\nAguarde a Impressão...")
        meu_aplicativo.bannervendas("Atualizar")

    def ExcluirVenda(self):
        meu_aplicativo = App.get_running_app()
        Id_Compra = meu_aplicativo.Id_Compra

        requisicao_dic = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas')

        for id in requisicao_dic:
            if id != 'Proxima_Venda' and requisicao_dic[id]["Id"] == Id_Compra:
                Produtos_Dic = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')
                for Produto in requisicao_dic[id]["Produtos"]:
                    for id_Produto in Produtos_Dic:
                        try:
                            if id_Produto != "Proximo_Id" and Produtos_Dic[id_Produto]["Nome"] == Produto["Produto"]:
                                qtde_estoque = int(Produtos_Dic[id_Produto]["Quantidade"])
                                qtde_venda = int(Produto["Quantidade"])
                                qtde_nova = qtde_estoque + qtde_venda
                                Dic_Nova_Qtde = {'Quantidade': f'{qtde_nova}'}
                                requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{id_Produto}/', Dic_Nova_Qtde)
                        except:
                            pass
                requisicao = meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id}')

        meu_aplicativo.bannervendas("Atualizar")

    def ExcluirProduto(self):
        meu_aplicativo = App.get_running_app()

        Id_Venda = meu_aplicativo.Id_Compra
        Tela = meu_aplicativo.root.ids["editarproduto"]
        Nome_Produto = meu_aplicativo.Nome_Produto_Alterar
        Qtde_Produto = int(meu_aplicativo.Quantidade_Produto_Alterar)
        Valor_Produto = float(meu_aplicativo.Valor_Produto_Alterar)

        Dic_Vendas = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas')
        for venda in Dic_Vendas:
            if venda != 'Proxima_Venda':
                IdV = int(Dic_Vendas[venda]["Id"])
                if IdV == int(Id_Venda):
                    Total = float(Dic_Vendas[venda]["Total"])
                    Total = Total - Valor_Produto
                    Dic_Novo_Total = {"Total": f"{Total}"}
                    requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}', Dic_Novo_Total)
                    Dic_Produtos = Dic_Vendas[venda]["Produtos"]
                    Dic_Produtos_Sem_None = list(filter(None, Dic_Produtos))
                    # Obtém o número de produtos na lista
                    numero_de_produtos = len(Dic_Produtos_Sem_None)
                    if numero_de_produtos > 1:
                        for produto in Dic_Produtos:
                            if produto != None and produto["Produto"] == Nome_Produto:
                                requisicao_Dic = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')
                                posicao_produto = next(
                                    (i for i, d in enumerate(Dic_Produtos) if d and d.get('Produto') == Nome_Produto),
                                    None)
                                for Id_Produto in requisicao_Dic:
                                    if Id_Produto != 'Proximo_Id':
                                        if requisicao_Dic[Id_Produto]["Nome"] == Nome_Produto:
                                            qtde = int(requisicao_Dic[Id_Produto]["Quantidade"])
                                            qtde = qtde + Qtde_Produto
                                            Nova_Qtde = {"Quantidade": f"{qtde}"}
                                            requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{Id_Produto}/', Nova_Qtde)
                                            requisicao = requests.delete(
                                                f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/Produtos/{posicao_produto}.json')
                                            requisicao = meu_aplicativo.Requisicao_Delete(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/Produtos/{posicao_produto}')
                                            BannerVendas.selecionar_item(self, meu_aplicativo.Id_Compra,meu_aplicativo.ID_Link)
                    else:
                        meu_aplicativo.bannervendas("ExcluirVenda")

    def Salvar_Alteracao(self):
        meu_aplicativo = App.get_running_app()
        id_venda = meu_aplicativo.ID_Link

        tela_mudanca = meu_aplicativo.root.ids["editarproduto"]
        Produto = meu_aplicativo.Nome_Produto_Alterar
        Quantidade_Antiga = int(meu_aplicativo.Quantidade_Produto_Alterar)

        Quantidade_Nova = int(tela_mudanca.ids["quantidade"].text)

        Valor = float(meu_aplicativo.Valor_Produto_Alterar)

        Produto_Dic = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')
        for id in Produto_Dic:
            if id != "Proximo_Id" and Produto_Dic[id]["Nome"] == Produto:
                Nova_Qtde = (int(Produto_Dic[id]["Quantidade"]) + int(Quantidade_Antiga)) - int(Quantidade_Nova)
                if Nova_Qtde > 0:

                    Nova_Qtde_Dic = {'Quantidade': f'{Nova_Qtde}'}
                    requisicao = meu_aplicativo.Requisicao_Patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{id}', Nova_Qtde_Dic)

                    tela = meu_aplicativo.root.ids["editarproduto"]
                    tela.ids["salvar_sair"].text = "Salvar e Sair"
                    tela.ids["salvar_sair"].color = (1, 1, 1, 1)

                    requisicao_dic = meu_aplicativo.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}")

                    Total = float(requisicao_dic["Total"])

                    requisicao_dic = meu_aplicativo.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/Produtos")

                    indice = 0
                    for ID in requisicao_dic:
                        if ID != None:
                            try:
                                if ID["Produto"] == Produto:
                                    Total -= float(ID["Valor"])
                                    Total += (float(Produto_Dic[id]["Valor"]) * Quantidade_Nova)
                                    Dic_Total = {'Total': f'{Total}'}
                                    requisicao = meu_aplicativo.Requisicao_Patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/", Dic_Total)

                                    dados = {'Quantidade': Quantidade_Nova, 'Valor': (float(Produto_Dic[id]["Valor"]) * Quantidade_Nova)}
                                    requisicao = meu_aplicativo.Requisicao_Patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/Produtos/{indice}/", dados)
                            except:
                                if requisicao_dic[ID]["Produto"] == Produto:
                                    Total -= float(requisicao_dic[ID]["Valor"])
                                    Total += (float(Produto_Dic[id]["Valor"]) * Quantidade_Nova)
                                    Dic_Total = {'Total': f'{Total}'}
                                    requisicao = meu_aplicativo.Requisicao_Patch(
                                        f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/",
                                        Dic_Total)

                                    dados = {'Quantidade': Quantidade_Nova,
                                             'Valor': (float(Produto_Dic[id]["Valor"]) * Quantidade_Nova)}
                                    requisicao = meu_aplicativo.Requisicao_Patch(
                                        f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{id_venda}/Produtos/{ID}/",
                                        dados)
                        indice += 1
                    BannerVendas.selecionar_item(self, meu_aplicativo.Id_Compra, meu_aplicativo.ID_Link)
                else:
                    tela = meu_aplicativo.root.ids["editarproduto"]
                    tela.ids["salvar_sair"].text = "Falta de Estoque"
                    tela.ids["salvar_sair"].color = (1, 0, 0, 1)

    def Inserir_Produto_Lista(self):
        meu_aplicativo = App.get_running_app()
        dic_Produto = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')

        self.limpar_lista_produtos()

        id_Venda = meu_aplicativo.Id_Compra
        id_Venda = int(re.search(r'\d+', id_Venda).group())
        Dic_Vendas = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas')

        novo_valor = meu_aplicativo.root.ids["adicionarproduto"]
        novo_valor.ids["quantidade"].text = "1"

        for venda in Dic_Vendas:
            if venda != 'Proxima_Venda':
                if int(Dic_Vendas[venda]['Id']) == id_Venda:
                    lista_Produto = meu_aplicativo.root.ids["adicionarproduto"]
                    lista_Produto = lista_Produto.ids["lista_produtos"]
                    lista = Dic_Vendas[venda]['Produtos']
                    lista = list(filter(None, lista))
                    nomes_produtos_filtrar = {item['Produto'] for item in lista}
                    lista_filtrada = {k: v for k, v in dic_Produto.items() if
                                      isinstance(v, dict) and v.get('Nome') not in nomes_produtos_filtrar}

                    for item in lista_filtrada:
                        nome = lista_filtrada[item]["Nome"]
                        valor = lista_filtrada[item]["Valor"]
                        quantidade = lista_filtrada[item]["Quantidade"]
                        item = LabelButton(text=f"{nome} \n R$ {valor: ,.2f} \n Quantidade: {quantidade}",
                                           pos_hint={"right": 1, "top": 0.2}, color=(0, 0, 0, 1),
                                           on_release=partial(self.Selecionar_Produto_Venda, nome))
                        lista_Produto.add_widget(item)

        meu_aplicativo.mudar_tela("adicionarproduto")

    def selecionar_produto(self, Id_Compra, Id_Link, Produto, *args):
        meu_aplicativo = App.get_running_app()

        Dic_Venda = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{Id_Link}/Produtos')
        for Item in Dic_Venda:
            try:
                if Item != None and Item['Produto'] == Produto:
                    meu_aplicativo.Nome_Produto_Alterar = Item['Produto']
                    meu_aplicativo.Quantidade_Produto_Alterar = Item['Quantidade']
                    meu_aplicativo.Valor_Produto_Alterar = Item['Valor']
                    Valor = float(Item['Valor'])
                    Tela = meu_aplicativo.root.ids["editarproduto"]
                    Tela.ids["quantidade"].text = f"{Item['Quantidade']}"
                    Tela.ids["Id_Produto"].text = f"{Item['Produto']} \nQuantidade: {Item['Quantidade']} \nValor: R$ {Valor: ,.2f}"
            except:
                if Item != None and Dic_Venda[Item]['Produto'] == Produto:
                    meu_aplicativo.Nome_Produto_Alterar = Dic_Venda[Item]['Produto']
                    meu_aplicativo.Quantidade_Produto_Alterar = Dic_Venda[Item]['Quantidade']
                    meu_aplicativo.Valor_Produto_Alterar = Dic_Venda[Item]['Valor']
                    Valor = float(Dic_Venda[Item]['Valor'])
                    Tela = meu_aplicativo.root.ids["editarproduto"]
                    Tela.ids["quantidade"].text = f"{Dic_Venda[Item]['Quantidade']}"
                    Tela.ids[
                        "Id_Produto"].text = f"{Dic_Venda[Item]['Produto']} \nQuantidade: {Dic_Venda[Item]['Quantidade']} \nValor: R$ {Valor: ,.2f}"

        meu_aplicativo.mudar_tela("editarproduto")

    def limpar_produtos(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["pagarvenda"]
        carrinho = pagina_carrinho.ids["lista_produtos"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def selecionar_item(self, Id_Compra, ID_Link, *args):
        meu_aplicativo = App.get_running_app()

        meu_aplicativo.ID_Link = ID_Link
        meu_aplicativo.Id_Compra = Id_Compra

        BannerVendas.limpar_produtos(self)

        dic_Venda = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{ID_Link}')

        Total = float(dic_Venda['Total'])
        Taxt_Total = f'TOTAL DA COMPRA: R${Total: ,.2f}'

        Text_Id = f'CÓDIGO: [color=ff0000]{Id_Compra}'

        Tela_vendas = meu_aplicativo.root.ids["pagarvenda"]

        Tela_vendas.ids["total_compra"].text = f"{Taxt_Total}"

        Codigo = Tela_vendas.ids["id_compra"]
        Codigo.markup = True,
        Codigo.text = f"{Text_Id}"

        dic_Venda = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{ID_Link}/Produtos')

        vendas = Tela_vendas.ids["lista_produtos"]

        for produto in dic_Venda:
            if produto != None:
                try:
                    Total = float(dic_Venda[produto]['Valor'])
                    item = LabelButton(
                        text=f"{dic_Venda[produto]['Produto']} \nQuantidade: {dic_Venda[produto]['Quantidade']} \nValor: R$ {Total: ,.2f}",
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                        on_release=partial(BannerVendas.selecionar_produto,self, Id_Compra, ID_Link, dic_Venda[produto]['Produto'])
                    )
                    vendas.add_widget(item)
                except:
                    Total = float(produto['Valor'])
                    item = LabelButton(
                        text=f"{produto['Produto']} \nQuantidade: {produto['Quantidade']} \nValor: R$ {Total: ,.2f}",
                        size_hint=(1, 0.2),
                        pos_hint={"right": 1, "top": 0.2},
                        color=(0, 0, 0, 1),
                        on_release=partial(BannerVendas.selecionar_produto, self, Id_Compra, ID_Link,
                                           produto['Produto'])
                    )
                    vendas.add_widget(item)

        meu_aplicativo.mudar_tela('pagarvenda')

    def Adicionar_Produto_Lista(self):
        meu_aplicativo = App.get_running_app()

        NomeProduto = meu_aplicativo.adicionar_nome_produto
        Tela = meu_aplicativo.root.ids["adicionarproduto"]
        QtdeVenda = int(Tela.ids['quantidade'].text)
        Dic_Produto = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos')
        for idProduto in Dic_Produto:
            if idProduto != 'Proximo_Id':
                if Dic_Produto[idProduto]['Nome'] == NomeProduto:
                    QtdeEstoque = int(Dic_Produto[idProduto]['Quantidade'])
                    Valor = float(Dic_Produto[idProduto]['Valor'])

                    if (QtdeEstoque - QtdeVenda) > 0:
                        Tela.ids["adicionarBt"].text = "Adicionar"
                        Tela.ids["adicionarBt"].color = (0, 0, 0, 1)

                        NovaQtde = QtdeEstoque - QtdeVenda
                        Dic_Qtde = {"Quantidade": f"{NovaQtde}"}
                        requisicao = meu_aplicativo.Requisicao_Patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{idProduto}/", Dic_Qtde)

                        Id_Venda = meu_aplicativo.Id_Compra
                        Dic_Vendas = meu_aplicativo.Requisicao_Get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas')
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
                                    Dic_Total = {"Total": f"{Total}"}
                                    Dic_Novo_Produto = {id: {"Produto": f"{NomeProduto}", "Quantidade": f"{QtdeVenda}",
                                                             "Valor": f"{ValorProduto}"}}

                                    requisicao = meu_aplicativo.Requisicao_Patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/", Dic_Total)
                                    requisicao = meu_aplicativo.Requisicao_Patch(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/{venda}/Produtos", Dic_Novo_Produto)
                                    meu_aplicativo.adicionar_nome_produto = None
                                    BannerVendas.selecionar_item(self, meu_aplicativo.Id_Compra, meu_aplicativo.ID_Link)

    def limpar_vendas(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["homepage"]
        carrinho = pagina_carrinho.ids["lista_vendas"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def __init__(self, **kwargs):

        meu_aplicativo = App.get_running_app()

        self.cols = 1

        super().__init__()

        try:
            self.limpar_vendas()
        except:
            pass

        requisicao_dic = meu_aplicativo.Requisicao_Get("https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas")

        Tela_vendas = meu_aplicativo.root.ids["homepage"]
        vendas = Tela_vendas.ids["lista_vendas"]

        for id in requisicao_dic:
            if id != 'Proxima_Venda':
                Id = requisicao_dic[id]['Id']
                Total = float(requisicao_dic[id]['Total'])
                produtos = requisicao_dic[id].get('Produtos', [])
                produtos = list(filter(None, produtos))
                Quantidade_Produto = len(produtos)

                Dic_Vendedor = meu_aplicativo.Requisicao_Get(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{requisicao_dic[id]["Vendedor"]}')

                # Separa o texto em partes
                parte_id = f"[color=ff0000]ID: {Id}[/color]"
                parte_vendedor = f" Vendedor: {Dic_Vendedor['Nome']}"
                parte_quantidade_total = f"\nQuantidade de Itens: {Quantidade_Produto} \nTotal: R$ {Total: ,.2f}"

                # Juntar as Partes
                texto_com_cores = parte_id + parte_vendedor + parte_quantidade_total

                item = LabelButton(
                    text=texto_com_cores,
                    markup=True,
                    size_hint=(1, 0.2),
                    pos_hint={"right": 1, "top": 0.2},
                    color=(0, 0, 0, 1),
                    on_release=partial(self.selecionar_item, Id, id)
                )
                vendas.add_widget(item)