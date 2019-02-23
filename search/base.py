
import pika

from search.settings import RABBITMQ


class RabbitMQBase:
    def _connect(self):
        self.credentials = pika.PlainCredentials(
            RABBITMQ['username'], RABBITMQ['password']
            )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                RABBITMQ['host'],
                RABBITMQ['port'],
                '/',
                self.credentials
            )
        )
        self.channel = self.connection.channel()
    