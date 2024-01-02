import pyautogui
import requests
from pyautogui import alert
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from telas import *
from botoes import *
from myfirebase import MyFirebase
from functools import partial
from BannerVendas import BannerVendas
from BannerCliente import BannerCliente
import json

GUI = Builder.load_file("main.kv")


class MainApp(App):
    id_vendedor = None
    nome_Caixa = None
    Id_Compra = None
    ID_Link = None
    Nome_Produto_Alterar = None
    Quantidade_Produto_Alterar = None
    Valor_Produto_Alterar = None
    adicionar_nome_produto = None
    CPF_Valido = False
    Login_Cliente = False
    Cupom_Valido = False
    Desconto = 0

    def build(self):
        self.title = "CAIXA"
        self.icon = "../imagens/icones/caixa.png"
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = "login"

    def Requisicao_Delete(self, url):
        try:
            requisicao = requests.delete(f'{url}.json')
            if requisicao.ok:
                return requisicao
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def Requisicao_Post(self, url, dic):
        try:
            requisicao = requests.post(f'{url}.json', data=json.dumps(dic))
            if requisicao.ok:
                return requisicao
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def Requisicao_Patch(self, url, dic):
        try:
            requisicao = requests.patch(f'{url}.json', data=json.dumps(dic))
            if requisicao.ok:
                return requisicao
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def Requisicao_Get(self, url):
        try:
            requisicao = requests.get(f'{url}.json')
            if requisicao.ok:
                requisicao_Dic = requisicao.json()
                return requisicao_Dic
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def bannervendas(self, funcao, **kwargs):
        if funcao == "Carregar":
            BannerVendas()
        elif funcao == "Atualizar":
            try:
                cpf = kwargs["CPF"]
                tela = self.root.ids["pagarvenda"]
                #CPF Compra
                self.CPF_Valido = False
                tela.ids["cpf_input"].text = ''
                tela.ids["label_cpf"].text = 'CPF:'
                tela.ids["label_cpf"].color = (0, 0, 0, 1)
                #Cupom
                self.Cupom_Valido = False
                self.Desconto = 0
                tela.ids["cupom_input"].text = ''
                tela.ids["label_cupom"].text = 'CUPOM DE DESCONTO:'
                tela.ids["label_cupom"].color = (0, 0, 0, 1)
                #CPF / NOME / EMAIL -> Cadastro
                tela = self.root.ids["cadastrarcliente"]
                tela.ids["nome_input"].text = ''
                tela.ids["email_input"].text = ''
                tela.ids["cpf_input"].text = ''
                self.Login_Cliente = False
                tela.ids["cadastrar_bt"].color = (1, 1, 1, 1)
                tela.ids["cadastrar_bt"].text = "CADASTRAR"
            except:
                pass
            BannerVendas()
            self.mudar_tela("homepage")
        elif funcao == "AdicionarProduto":
            BannerVendas.Inserir_Produto_Lista(self)
        elif funcao == "AdicionarProdutoLista":
            BannerVendas.Adicionar_Produto_Lista(self)
        elif funcao == "Recarregar":
            BannerVendas.selecionar_item(self, self.Id_Compra, self.ID_Link)
        elif funcao == "SalvarAlteracao":
            BannerVendas.Salvar_Alteracao(self)
        elif funcao == "ExcluirProduto":
            BannerVendas.ExcluirProduto(self)
        elif funcao == "ExcluirVenda":
            BannerVendas.ExcluirVenda(self)
        elif funcao == "Pagar":
            BannerVendas.Pagar(self)

    def bannercliente(self, funcao):
        if funcao == "Validar_CPF":
            BannerCliente.Validar_CPF(self)
        elif funcao == "Cadastrar":
            tela = self.root.ids["cadastrarcliente"]
            if self.Login_Cliente == False:
                tela.ids["cadastrar_bt"].color = (1, 1, 1, 1)
                tela.ids["cadastrar_bt"].text = "CADASTRAR"
                BannerCliente()
            else:
                tela.ids["cadastrar_bt"].color = (0, 0, 0, 1)
                tela.ids["cadastrar_bt"].text = "Logado"
        elif funcao == "Validar_Cupom":
            BannerCliente.Validar_Cupom(self)

    def carregarInfos(self, id_Usuario):
        # Limpar Login
        tela = self.root.ids["login"]
        tela.ids["usuario_input"].text = ''
        tela.ids["senha_input"].text = ''
        # Pegar Dados do Usuario
        requisicao_dic = self.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Caixa/{id_Usuario}")

        # Carregar Nome
        nome = requisicao_dic['Nome']
        self.nome_Caixa = nome
        nome_perfil = self.root.ids["homepage"]
        nome_perfil.ids["id_nome_vendedor"].text = f"Caixa {requisicao_dic['Nome']}"

        #Carregar Vendas
        self.bannervendas("Carregar")

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

    def limpar_lista_produtos(self):
        meu_aplicativo = App.get_running_app()

        pagina_carrinho = meu_aplicativo.root.ids["adicionarproduto"]
        carrinho = pagina_carrinho.ids["lista_produtos"]
        for item in list(carrinho.children):
            carrinho.remove_widget(item)

    def Selecionar_Produto_Venda(self, nome, *args):
        meu_aplicativo = App.get_running_app()

        self.adicionar_nome_produto = nome
        # pintar de branco todos os outros caras
        pagina_home = meu_aplicativo.root.ids["adicionarproduto"]
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

    def ModificarQuantidade(self, fazer, pagina):

        meu_aplicativo = App.get_running_app()

        if fazer == 1:
            novo_valor = meu_aplicativo.root.ids[pagina]
            valor = int(novo_valor.ids["quantidade"].text)
            valor = valor + 1
            novo_valor.ids["quantidade"].text = f"{valor}"
        elif fazer == -1:
            novo_valor = meu_aplicativo.root.ids[pagina]
            valor = int(novo_valor.ids["quantidade"].text)
            if valor > 1:
                valor = valor - 1
            novo_valor.ids["quantidade"].text = f"{valor}"

MainApp().run()