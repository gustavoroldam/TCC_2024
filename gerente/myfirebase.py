import json
from kivy.app import App
import requests

class MyFirebase():
    API_Chave = "AIzaSyCQdX6Pn9DTIPWBOv2_eDB4lxbP1aEUJIg"

    def criar_conta(self, nome, senha):
        dados = {'Nome': f'{nome}', 'Senha': f'{senha}', 'Comissao': '0'}
        requisicao = requests.post(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios.json", data=json.dumps(dados))

        if requisicao.ok:
            pass
        else:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = f'{requisicao.text}'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)

    def fazer_login(self, nome, senha):
        meu_aplicativo = App.get_running_app()
        dic_requisicao = meu_aplicativo.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios")
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