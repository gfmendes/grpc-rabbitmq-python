from __future__ import print_function

import logging
import json
import sys
import os

import pika
import pymongo


'''Below attributes must exist otherwise application should halt'''
CLIENT_NAME = sys.argv[1]
RABBIT_HOST = os.environ['APP_RABBITMQ_HOST']
TOPIC_PERSIST_NAME = os.environ['APP_RABBITMQ_TOPIC_PERSIST_NAME']
MONGO_CONNECTION_STR = os.environ['APP_MONGO_CONNECTION_STR']

class ClientPersistenceConsumer:
    def __init__(self, *args, **kwargs):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=TOPIC_PERSIST_NAME, exchange_type='topic')
        self.result = self.channel.queue_declare(queue=CLIENT_NAME, durable=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange=TOPIC_PERSIST_NAME, queue=self.queue_name, routing_key='#')

    @staticmethod
    def store_function(ch, method, properties, body):
        func = json.loads(body);
        print("%s - received %r" % (CLIENT_NAME, func))
        ClientPersistenceMongoDB().add(func)

    def read_queue(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.store_function, auto_ack=True)
        try:
            self.channel.start_consuming()
        # TODO: improve except level
        except:
            print("Error while processing queue.")
        finally:
            self.connection.close()


class ClientPersistenceMongoDB:
    def __init__(self, *args, **kwargs):
        self.client = pymongo.MongoClient(MONGO_CONNECTION_STR)
        self.database = self.client[CLIENT_NAME]

    def add(self, function):
        self.database.functions.insert_one(function)
        return function


if __name__ == '__main__':
    logging.basicConfig()
    print("App params=", CLIENT_NAME, RABBIT_HOST, TOPIC_PERSIST_NAME, MONGO_CONNECTION_STR)
    ClientPersistenceConsumer().read_queue()
