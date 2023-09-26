# pip install flask
# pip install bardapi==0.1.28
# pip install Flask-Cors
import os
import json
from flask import Flask, request, jsonify
import requests
from chave import API_KEY_CHAT, API_KEY_BARD
from flask_cors import CORS
from bardapi import Bard
import os

app = Flask(__name__)
CORS(app)  # Isso permite solicitações de qualquer origem


# Configurações do banco de dados (pode ser substituído por um banco de dados real)
questions_and_answers = [{"question": "Tenho uma pergunta", "answer": "Toma a resposta"}]

# Função para obter resposta do ChatGPT
def get_chatgpt_response(question):
    try:
        endpoint = "https://api.openai.com/v1/chat/completions"
        id_modelo = 'gpt-3.5-turbo'

        headers = {
            "Authorization": f"Bearer {API_KEY_CHAT}",
            "Content-type":"application/json"
        }

        data = {
            "model": id_modelo,
            "messages": [
                {
                    "role": "user",
                    "content": f"Eu como agricultor gostaria de saber {question}"
                }
            ]
        }

        data = json.dumps(data)
        
        response = requests.post(endpoint, headers=headers, data=data)

        response_data = response.json()

        if response_data['error']:
            mensagemErro = response_data['error']['message']
            return f'Erro na solicitação: {mensagemErro}'

        if not "choices" in response_data and len(response_data["choices"]) > 0:
            return "Erro Resposta vazia da API"
        
        return response_data["choices"][0]["text"]
    except Exception as erro:
        print(erro)
        return f'Erro na solicitação'
    

# Rota da API para responder às perguntas dos agricultores
@app.route('/api/ask', methods=['POST'])
def ask_question():
    # if not authenticate_request():
    #     return jsonify({"error": "Autenticação falhou."}), 401

    try:
        data = request.json
        question = data.get("question")
        if not question:
            return jsonify({"error": "A chave 'question' está ausente no corpo da solicitação."}), 400

        response = get_chatgpt_response(question)

        # Obter leitura de umidade do Arduino
        # humidity_reading = get_humidity_reading()

        if 'Erro' in response:
            return jsonify({"error": "erro"}), 500
        
        # Armazenar a pergunta, resposta e leitura de umidade (pode ser substituído por um banco de dados)
        questions_and_answers.append({"question": question, "answer": response})

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota da API para listar todas as perguntas e respostas armazenadas
@app.route('/api/questions', methods=['GET'])
def list_questions():

    return jsonify({"questions": questions_and_answers})

# Rota para a leitura de imagem
@app.route('/bard/analise-imagem', methods=['POST'])
def analiseImagem():
    try:

        data = request.json
        url = data.get("url")
        board = Bard(token=API_KEY_BARD, token_from_browser=True)

        # Envie uma solicitação HTTP GET para a URL
        response = requests.get(url)

        pergunta = 'Olá eu como agricultor, gostaria de ter uma análise '

        # Quando tiver o nome da planta mas não tiver pergunta e nem problema
        if data.get("nome_planta") and not data.get("problema") and not data.get("pergunta"):
            pergunta += f'da minha {data.get("nome_planta")}'
        # Quando tiver o nome da planta e o problema mas não tiver pergunta
        elif data.get("nome_planta") and data.get("problema") and not data.get("pergunta"):
            pergunta += f'da minha {data.get("nome_planta")} que estou enfrentando o problema {data.get("problema")}'
        # Quando tiver o nome da planta e a pergunta mas não tiver problema
        elif data.get("nome_planta") and not data.get("problema") and data.get("pergunta"):
            pergunta += f'da minha {data.get("nome_planta")} e gostaria de perguntar {data.get("pergunta")}'
        # Quando tiver o nome da planta, a pergunta e o problema
        elif data.get("nome_planta") and data.get("problema") and data.get("pergunta"):
            pergunta += f'da minha {data.get("nome_planta")} que estou enfrentando o problema {data.get("problema")} e gostaria de perguntar {data.get("pergunta")}'
        # Quando tiver a pergunta e o problema mas não o nome
        elif not data.get("nome_planta") and data.get("problema") and data.get("pergunta"):
            pergunta += f'de um problema {data.get("problema")} e gostaria de perguntar {data.get("pergunta")}'
        # Quando tiver a pergunta mas não o nome e o problema 
        elif not data.get("nome_planta") and not data.get("problema") and data.get("pergunta"):
            pergunta += f'para saber {data.get("pergunta")}'
        # Quando tiver o problema mas não o nome e o pergunta 
        elif not data.get("nome_planta") and data.get("problema") and not data.get("pergunta"):
            pergunta += f'porque estou enfretando o problema data.get("problema")'

        pergunta += ', com base nesta foto.'

        print(pergunta)


        if 'https://' in url or 'http://' in url:
            # Verifique se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:
                # Nome do arquivo onde você deseja salvar a imagem localmente
                imagem_baixada = 'imagem_local.jpg'

                # Abra o arquivo para escrita binária
                with open(imagem_baixada, 'wb') as arquivo:
                    # Escreva o conteúdo da resposta no arquivo
                    arquivo.write(response.content)

                print(f'Imagem baixada com sucesso como {imagem_baixada}')
                image = open(imagem_baixada, 'rb').read()  # (jpeg, png, webp) are supported.
                bard_answer = board.ask_about_image(pergunta, image)
                os.remove(imagem_baixada)
            else:
                print('Falha ao baixar a imagem. Código de status:', response.status_code)
                raise Exception()


        elif 'C:' in url:
            image = open(url, 'rb').read()  # (jpeg, png, webp) are supported.
            bard_answer = board.ask_about_image(pergunta, image)
            os.remove(url)

        else:
            raise Exception()

        return jsonify({"sucesso": bard_answer['content'].replace("Bard", "AgroSync")})
    except Exception as erro:

        return jsonify({'erro':erro})


app.run(debug=True)
