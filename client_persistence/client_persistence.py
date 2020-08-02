from __future__ import print_function

import logging
import json
import sys
import os

import pika
import pymongo


"""Below attributes must exist otherwise application should halt (raising a KeyError)"""
CLIENT_NAME = sys.argv[1]
RABBIT_HOST = os.environ['APP_RABBITMQ_HOST']
TOPIC_PERSIST_NAME = os.environ['APP_RABBITMQ_TOPIC_PERSIST_NAME']
MONGO_CONNECTION_STR = os.environ['APP_MONGO_CONNECTION_STR']


class ClientPersistenceConsumer:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=TOPIC_PERSIST_NAME, exchange_type='topic')
        self.result = self.channel.queue_declare(queue=CLIENT_NAME, durable=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange=TOPIC_PERSIST_NAME, queue=self.queue_name, routing_key='#')

    def store_function(self, ch, method, properties, body):
        self.log.info("[%s] received message=%r" % (CLIENT_NAME, body))
        operation = json.loads(body)
        ClientPersistenceMongoDB().add(operation)
        self.log.info("[%s] added operation to database: %s" % (CLIENT_NAME, body))

    def read_queue(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.store_function, auto_ack=True)
        try:
            self.log.info("[%s] topic [%s] consuming is starting" % (CLIENT_NAME, TOPIC_PERSIST_NAME))
            self.channel.start_consuming()
        finally:
            self.connection.close()
            self.log.info("[$s] RabbitMQ connection closed." % CLIENT_NAME)


class ClientPersistenceMongoDB:
    def __init__(self, *args, **kwargs):
        self.client = pymongo.MongoClient(MONGO_CONNECTION_STR)
        self.database = self.client[CLIENT_NAME]

    def add(self, operation):
        return self.database.operations.insert_one(operation)


def set_log():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    set_log()
    logging.info("App params= [%s] [%s] [%s] [%s]", CLIENT_NAME, RABBIT_HOST, TOPIC_PERSIST_NAME, MONGO_CONNECTION_STR)
    ClientPersistenceConsumer().read_queue()
