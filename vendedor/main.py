import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from telas import *
from botoes import *
from bannerVendas import BannerVendas
from bannerCarrinho import BannerCarrinho
from bannerProdutos import BannerProdutos
from bannerFinalizarVenda import BannerFinalizarVenda
from myfirebase import MyFirebase
from functools import partial
import json

GUI = Builder.load_file("main.kv")


class MainApp(App):
    id_vendedor = None
    nome_produto = None
    valor_produto = None
    Novo_valor_produto = None
    Id_Link = None
    adicionar_nome_produto = None

    def build(self):
        self.title = "VENDAS"
        self.icon = "../imagens/icones/vendedor.png"
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        # Carregar Dados dos Produtos
        self.Produto("Carregar")

    #Mudar Tela
    def mudar_tela(self, id_tela):

        if id_tela == "homepage":
            BannerProdutos()

        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def carregarInfos(self, id_Usuario):
        # Limpar Login
        tela = self.root.ids["login"]
        tela.ids["usuario_input"].text = ''
        tela.ids["senha_input"].text = ''
        # Pegar Dados do Usuario
        requisicao = requests.get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Vendedor/{id_Usuario}.json")
        requisicao_dic = requisicao.json()

        # Carregar Nome
        nome = requisicao_dic['Nome']
        self.nome = nome
        nome_perfil = self.root.ids["homepage"]
        nome_perfil.ids["id_nome_vendedor"].text = f"Vendedor {requisicao_dic['Nome']}"

    def realizar_login(self, nome, senha):
        self.id_vendedor = MyFirebase.fazer_login(self, nome, senha)
        if self.id_vendedor != -1 and self.id_vendedor != -2:
            self.carregarInfos(self.id_vendedor)
            self.mudar_tela('homepage')
        elif self.id_vendedor == -2:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = 'Senha Incorreta'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)
        else:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = 'Usuario Incorreto'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)

    def Produto(self, funcao):
        if funcao == "Carregar":
            BannerProdutos()
        elif funcao == "Adicionar":
            BannerProdutos.adicionar_carrinho(self)
        elif funcao == 1 or funcao == -1:
            BannerProdutos.ModificarQuantidade(self, funcao)

    def Carrinho(self, funcao):
        if funcao == "Carregar":
            BannerCarrinho(id_vendedor=self.id_vendedor)
        elif funcao == 1 or funcao == -1:
            BannerCarrinho.ModificarQuantidade_Carrinho(self, funcao)
        elif funcao == "Salvar":
            BannerCarrinho.Salvar_Alteracao(self, self.id_vendedor)
        elif funcao == "Deletar":
            BannerCarrinho.Deletar_Item(self, self.id_vendedor)
        elif funcao == "Limpar":
            BannerCarrinho.Limpar_Carrinho(self, self.id_vendedor)

    def Venda(self, funcao, **kwargs):
        if funcao == "Finalizar":
            BannerFinalizarVenda.Criar_Venda(self, self.id_vendedor)
        elif funcao == "Carregar":
            BannerVendas()
        elif funcao == "Excluir":
            BannerVendas.excluir(self)
        elif funcao == 1 or funcao == -1:
            try:
                tela = kwargs["Tela"]
                BannerVendas.ModificarQuantidade_Produto(self, funcao)
            except:
                BannerVendas.ModificarQuantidade_Carrinho(self, funcao)
        elif funcao == "Salvar":
            BannerVendas.Salvar_Alteracao(self)
        elif funcao == "Deletar":
            BannerVendas.Deletar_Item(self)
        elif funcao == "SalvarAlteracao":
            codigo = kwargs["Codigo"]
            link = kwargs["Link"]
            BannerVendas.selecionar_item(self, codigo, link)
        elif funcao == "Adicionar":
            BannerVendas.Adicionar(self)
        elif funcao == "Adicionar_Produto":
            BannerVendas.Adicionar_Produto(self)

    def Limpar_Selecionar_Produto_Venda(self):
        meu_aplicativo = App.get_running_app()
        pagina_home = meu_aplicativo.root.ids["adicionarprodutodavenda"]
        lista_produtos = pagina_home.ids["lista_produtos"]
        for item in list(lista_produtos.children):
            lista_produtos.remove_widget(item)
        pagina_home.ids["quantidade"].text = "1"

    def Selecionar_Produto_Venda(self, nome, *args):
        meu_aplicativo = App.get_running_app()

        meu_aplicativo.adicionar_nome_produto = nome
        # pintar de branco todos os outros caras
        pagina_home = meu_aplicativo.root.ids["adicionarprodutodavenda"]
        lista_produtos = pagina_home.ids["lista_produtos"]
        for item in list(lista_produtos.children):
            item.color = (0, 0, 0, 1)
            # pintar de azul a letra do item selecionado
            try:
                texto = item.text
                if nome in texto:
                    item.color = (1, 1, 1, 1)
            except:
                pass

MainApp().run()