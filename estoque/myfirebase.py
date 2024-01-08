import json
from kivy.app import App
import requests
from pyautogui import alert

class MyFirebase():
    API_Chave = "AIzaSyCQdX6Pn9DTIPWBOv2_eDB4lxbP1aEUJIg"

    def fazer_login(self, nome, senha):
        meu_aplicativo = App.get_running_app()
        dic_requisicao = meu_aplicativo.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Estoque")
        id = -1
        for id_vendedor in dic_requisicao:
            nome_aux = dic_requisicao[id_vendedor]['Nome']
            if nome == nome_aux:
                senha_aux = dic_requisicao[id_vendedor]['Senha']
                if senha == senha_aux:
                    id = id_vendedor
                else:
                    id = -2
        return id