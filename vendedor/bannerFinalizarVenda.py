from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from TCC_2023.vendedor.botoes import LabelButton
import requests
import json

class BannerFinalizarVenda(GridLayout):

    def Criar_Venda(self, id_vendedor):

        meu_aplicativo = App.get_running_app()

        requisicao = requests.get(
            f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{meu_aplicativo.id_vendedor}/Lista_Venda/{meu_aplicativo.id_vendedor}.json")
        requisicao_dic = requisicao.json()

        try:
            Total = float(requisicao_dic['Total'])
        except:
            Total = requisicao_dic['Total'].replace(',', '')
            Total = float(Total)

        Produtos = {}
        Quantidade_Total = 0

        indice = 1
        verificar = True

        requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_vendedor}/Lista_Venda.json")
        requisicao_dic = requisicao.json()
        requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos.json')
        Produto_Dic = requisicao.json()
        try:
            for id in requisicao_dic:
                if id != meu_aplicativo.id_vendedor and verificar == True:
                    # print(requisicao_dic[id]["Produto"], requisicao_dic[id]["Quantidade"], requisicao_dic[id]["Valor"])
                    Produtos[indice] = {"Produto" : requisicao_dic[id]["Produto"], "Quantidade" : requisicao_dic[id]["Quantidade"], "Valor" : requisicao_dic[id]["Valor"]}
                    Quantidade_Total += float(requisicao_dic[id]["Valor"])
                    indice += 1

                    for id_Produto in Produto_Dic:
                        if id_Produto != "Proximo_Id" and Produto_Dic[id_Produto]["Nome"] == requisicao_dic[id]["Produto"]:
                            Nova_Qtde = int(Produto_Dic[id_Produto]["Quantidade"]) - int(requisicao_dic[id]["Quantidade"])
                            if Nova_Qtde < 0:
                                verificar = False
        except:
            pass

        if Produtos != {} and verificar == True:

            for id in requisicao_dic:
                if id != meu_aplicativo.id_vendedor:
                    for id_Produto in Produto_Dic:
                        if id_Produto != "Proximo_Id" and Produto_Dic[id_Produto]["Nome"] == requisicao_dic[id]["Produto"]:
                            Nova_Qtde = int(Produto_Dic[id_Produto]["Quantidade"]) - int(requisicao_dic[id]["Quantidade"])
                            Dic_Produto = {"Quantidade": f"{Nova_Qtde}"}
                            requisicao = requests.patch(f'https://tcc2023-9212b-default-rtdb.firebaseio.com/Produtos/{id_Produto}.json', data=json.dumps(Dic_Produto))

            requisicao = requests.get('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/Proxima_Venda.json')
            requisicao_dic = requisicao.json()
            Dic_Vendas = {'Produtos': Produtos, 'Total': Total, 'Vendedor': f'{meu_aplicativo.id_vendedor}', 'Id': f'{requisicao_dic["Id"]}'}

            requisicao = requests.post('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas.json', data=json.dumps(Dic_Vendas))
            if requisicao.ok:
                pagina_finalizacao = meu_aplicativo.root.ids["finalizacao"]
                pagina_finalizacao.ids["codigo_venda"].text = f'{requisicao_dic["Id"]}'

                Proximo_Id = int(requisicao_dic['Id'])
                Proximo_Id += 1
                Dic_Prox_Id = {"Id": f'{Proximo_Id}'}
                requisicao = requests.patch('https://tcc2023-9212b-default-rtdb.firebaseio.com/Vendas/Vendas_Abertas/Proxima_Venda.json', data=json.dumps(Dic_Prox_Id))
                meu_aplicativo.Carrinho("Limpar")
                meu_aplicativo.mudar_tela("finalizacao")

                novo_valor = meu_aplicativo.root.ids["homepage"]
                novo_valor.ids["quantidade"].text = "1"
        else:
            nome_perfil = meu_aplicativo.root.ids["homepage"]
            nome_perfil.ids["id_nome_vendedor"].text = f"Lista de venda vazia!"
            nome_perfil.ids["id_nome_vendedor"].color = (1, 0, 0, 1)
            meu_aplicativo.mudar_tela("homepage")