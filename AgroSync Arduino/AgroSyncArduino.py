from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import time

app = Flask(__name__)
CORS(app)

# Configuração da comunicação serial com o Arduino
ser = serial.Serial('COM3', 9600, timeout=1)


@app.route('/atualizar-sensor', methods=['POST'])
def atualizar_sensor():
    data = request.get_json()
    umidade = data['umidade']

    # Envia a umidade para o Arduino
    ser.write(f'{umidade}\n'.encode())

    # Aguarda a resposta do Arduino
    resposta = ser.readline().decode().strip()

    # Imprime a umidade lida no console
    print(f'Umidade lida: {resposta}')
    print(f'Umidade atual: {umidade}')

    return jsonify({'': resposta})


@app.route('/umidade-atual', methods=['GET'])
def umidade_atual():
    # Solicita a leitura atual do Arduino
    ser.write(b'LER\n')

    # Aguarda a resposta do Arduino
    umidade = ser.readline().decode().strip()

    # Imprime a umidade lida no console
    print(f'Umidade atual: {umidade}')

    return jsonify({'umidade': umidade})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
