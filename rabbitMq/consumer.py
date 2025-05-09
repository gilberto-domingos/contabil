import pika
import json
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

secret_key_path = os.getenv("SECRET_KEY_FILE", "private_key.pem")
with open(secret_key_path, "r") as f:
    secret_key = f.read().strip()


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = "jrdomingosjr00@gmail.com"
        self.email_password = os.getenv("EMAIL_PASSWORD")

        # Lista de destinatários adicionais
        self.additional_recipients = [
            "ana.voss99@gmail.com",
            "pessoal@mosimann.com.br",
            "itamar@mosimann.com.br",
            "itamosimann@gmail.com",
            "jrdomingosjr00@gmail.com"
        ]

    def send_email(self, to_email, subject, body):
        # Inclui os destinatários extras
        recipients = [to_email] + self.additional_recipients

        msg = MIMEMultipart()
        msg["From"] = self.email_user
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            print(
                f"Conectando ao servidor SMTP: {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            print(f"Enviando e-mail para: {recipients}")
            server.sendmail(self.email_user, recipients, msg.as_string())
            server.quit()
            print(f"E-mail enviado com sucesso para: {', '.join(recipients)}")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")


class RabbitMqConsumer:
    def __init__(self, callback) -> None:
        self.__host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.__port = 5672
        self.__username = os.getenv("RABBITMQ_USER")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__vhost = os.getenv("RABBITMQ_VHOST", "/")
        self.__queue = "data_queue"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            virtual_host=self.__vhost,
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
        print("Escutando mensagens no RabbitMQ...")
        print(f"Senha carregada: {os.getenv('EMAIL_PASSWORD')}")
        self.__channel.start_consuming()


def email_callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        email_sender = EmailSender()
        email_sender.send_email(data["email"], data["subject"], data["body"])
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


if __name__ == "__main__":
    rabbitmq_consumer = RabbitMqConsumer(email_callback)
    rabbitmq_consumer.start()
