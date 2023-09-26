import requests
import json

# URL para a qual você deseja enviar a requisição POST
url = 'http://127.0.0.1:5000/bard/analise-imagem'

# Dados que você deseja enviar no corpo da requisição POST
dados = {
    "url": "https://www.decorfacil.com/wp-content/uploads/2018/09/20180909tipos-de-flores-87.jpg",
    "pergunta": "como eu faço para cuidar dela"
}

# Configurar o cabeçalho "Content-Type" como "application/json"
headers = {'Content-Type': 'application/json'}

# Enviar a requisição POST com os dados em formato JSON e o cabeçalho
response = requests.post(url, json=dados, headers=headers)
response = response.json()

# Verificar se a requisição foi bem-sucedida (código de status 200)
if response.get("sucesso"):
    resposta = response.get("sucesso")
    print(resposta)
else:
    resposta = response.get("erro")
    print(resposta)
