import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

secret_key_path = os.getenv("SECRET_KEY_FILE", "private_key.pem")
with open(secret_key_path, "r") as f:
    secret_key = f.read().strip()


class RabbitMqPublisher:
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.__virtual_host = os.getenv(
            "RABBITMQ_VHOST", "/")
        self.__port = 5672
        self.__username = os.getenv("RABBITMQ_USER")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__exchange = "data_exchange"
        self.__routing_key = "data_route"

        if not self.__username or not self.__password:
            raise ValueError(
                "Usuário ou senha do RabbitMQ não definidos nas variáveis de ambiente.")

        self.__channel = self.__create_channel()

    def __create_channel(self):
        try:
            connection_parameters = pika.ConnectionParameters(
                host=self.__host,
                port=self.__port,
                virtual_host=self.__virtual_host,
                credentials=pika.PlainCredentials(
                    username=self.__username,
                    password=self.__password
                )
            )
            connection = pika.BlockingConnection(connection_parameters)
            channel = connection.channel()

            channel.exchange_declare(
                exchange=self.__exchange, exchange_type='direct')

            return channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar ao RabbitMQ: {e}")
            raise

    def send_message(self, message: dict):
        """Publica uma mensagem no RabbitMQ."""
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        print(f"Mensagem enviada: {message}")


if __name__ == "__main__":
    rabbitMqPublisher = RabbitMqPublisher()
    message = {
        "email": "jrdomingosjr00@gmail.com",
        "subject": "Notificação de Balanço",
        "body": "Você está sendo notificado que a sua conferência de balanço foi reprovada. Faça uma revisão no seu balanço!"
    }
    rabbitMqPublisher.send_message(message)
