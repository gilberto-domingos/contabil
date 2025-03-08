import pika
import json
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

load_dotenv()  # Carrega variáveis de ambiente

secret_key_path = os.getenv("SECRET_KEY_FILE", "private_key.pem")
with open(secret_key_path, "r") as f:
    secret_key = f.read().strip()


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = "jrdomingosjr00@gmail.com"
        self.email_password = os.getenv("EMAIL_PASSWORD")

    def send_email(self, to_email, subject, body):
        """Envia um e-mail para o destinatário especificado."""
        msg = MIMEMultipart()
        msg["From"] = self.email_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.sendmail(self.email_user, to_email, msg.as_string())
            server.quit()
            print(f"E-mail enviado para {to_email}")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")


class RabbitMqConsumer:
    def __init__(self, callback) -> None:
        self.__host = "186.250.185.87"
        self.__port = 15672
        self.__username = os.getenv("RABBITMQ_USER")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__queue = "data_queue"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        """Cria e retorna um canal para consumir mensagens."""
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True,
            arguments={
                "x-overflow": "reject-publish"
            }
        )

        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        """Inicia o consumo de mensagens."""
        print("Escutando mensagens no RabbitMQ...")
        print(f"Senha carregada: {os.getenv('EMAIL_PASSWORD')}")
        self.__channel.start_consuming()


def email_callback(ch, method, properties, body):
    """Callback para processar mensagens da fila e enviar e-mails."""
    try:
        data = json.loads(body)
        email_sender = EmailSender()
        email_sender.send_email(data["email"], data["subject"], data["body"])
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


# Inicia o consumidor
if __name__ == "__main__":
    rabbitmq_consumer = RabbitMqConsumer(email_callback)
    rabbitmq_consumer.start()
