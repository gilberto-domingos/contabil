import pika
import json
import os
from dotenv import load_dotenv
import os


secret_key_path = os.getenv("SECRET_KEY_FILE", "private_key.pem")
with open(secret_key_path, "r") as f:
    secret_key = f.read().strip()


load_dotenv()  # Carrega variáveis de ambiente


class RabbitMqPublisher:
    def __init__(self) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = os.getenv("RABBITMQ_USER")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__exchange = "data_exchange"
        self.__routing_key = "data_route"
        self.__channel = self.__create_channel()

    def __create_channel(self):
        """Cria e retorna um canal para publicar mensagens."""
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel

    def send_message(self, message: dict):
        """Publica uma mensagem no RabbitMQ."""
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2)  # Mensagem persistente
        )
        print(f"Mensagem enviada: {message}")


# Exemplo de uso
if __name__ == "__main__":
    rabbitMqPublisher = RabbitMqPublisher()
    message = {
        "email": "jrdomingosjr00@gmail.com",
        "subject": "Notificação de Balanço",
        "body": "Você está sendo notificado que a sua conferência de balanço foi reprovada. Faça uma revisão no seu balanço!"
    }
    rabbitMqPublisher.send_message(message)
