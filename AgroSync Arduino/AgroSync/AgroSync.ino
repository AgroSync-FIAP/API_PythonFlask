#include <ArduinoHttpClient.h>
#include <Ethernet.h>

// Definição dos pinos
const int pinoSensor = A0; // Pino do sensor de umidade
const int pinoRele = 2;    // Pino do relé

// Configuração da conexão Ethernet
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED}; // Endereço MAC
EthernetClient cliente;
HttpClient http(cliente, "http://192.168.15.6:5000", 5000); // Endereço e porta do servidor Flask

void setup() {
  pinMode(pinoSensor, INPUT);  // Define o pino do sensor como entrada
  pinMode(pinoRele, OUTPUT);   // Define o pino do relé como saída
  Serial.begin(9600);          // Inicializa a comunicação serial
  Ethernet.begin(mac);         // Inicializa a conexão Ethernet
}

void loop() {
  // Lê o valor analógico do sensor de umidade
  int leitura = analogRead(pinoSensor);

  // Converte o valor lido em porcentagem de umidade
  float porcentoUmidade = map(leitura, 0, 1023, 0, 100);

  // Exibe a leitura no monitor serial
  Serial.print("Umidade: ");
  Serial.print(porcentoUmidade);
  Serial.println("%");

  // Crie uma mensagem JSON para enviar ao Flask
  String mensagem = "{\"umidade\":" + String(porcentoUmidade) + "}";

  // Envie a mensagem JSON para o Flask usando uma solicitação HTTP POST
  http.beginRequest();
  http.post("/atualizar-sensor", "application/json", mensagem);
  http.endRequest();

  // Aguarde uma resposta do Flask
  HttpClient::Response response = http.response();
  int statusCode = response.status;
  
  // Verifique a resposta do Flask e controle o relé com base nela
  if (statusCode == 200) {
    String resposta = response.body;
    Serial.println("Resposta do Flask: " + resposta);
    if (resposta == "ligar_rele") {
      digitalWrite(pinoRele, HIGH);  // Liga o relé
      Serial.println("Relé ligado!");
    } else if (resposta == "desligar_rele") {
      digitalWrite(pinoRele, LOW);   // Desliga o relé
      Serial.println("Relé desligado!");
    }
  }
  
  delay(1000);  // Espera um segundo antes da próxima leitura
}
