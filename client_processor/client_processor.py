from __future__ import print_function
import math_operation
import json
import logging
import sys
import os

import grpc
import pika

import server_pb2
import server_pb2_grpc

"""Below attributes must exist otherwise application should halt (raising a KeyError)"""
CLIENT_NAME = sys.argv[1]
GRPC_SERVER_URL = os.environ['APP_GRPC_SERVER_URL']
RABBIT_HOST = os.environ['APP_RABBITMQ_HOST']
QUEUE_OPERATION_NAME = os.environ['APP_RABBITMQ_QUEUE_OPERATION_NAME']
TOPIC_PERSIST_NAME = os.environ['APP_RABBITMQ_TOPIC_PERSIST_NAME']


class RemoteConnection:
    def run(self):
        with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
            stub = server_pb2_grpc.ConnectionStub(channel)
            self.connect_to_server(stub)

    @staticmethod
    def connect_to_server(stub):
        response = stub.Connect(server_pb2.ConnectionRequest(name=CLIENT_NAME))
        if response.result == 'true':
            ClientConsumer().read_queue()


class ClientConsumer:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE_OPERATION_NAME)

    def read_queue(self):
        self.channel.basic_consume(queue=QUEUE_OPERATION_NAME, on_message_callback=self.process_operation, auto_ack=True)
        self.log.info("[%s] queue [%s] consuming is starting" % (CLIENT_NAME,QUEUE_OPERATION_NAME))
        self.channel.start_consuming()

    def process_operation(self, ch, method, properties, body):
        self.log.info("[%s] received message=%r" % (CLIENT_NAME, body))
        func = json.loads(body)
        result = math_operation.MathOperation().calc(func)
        ClientPersistenceProducer().produce(result)


class ClientPersistenceProducer:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=TOPIC_PERSIST_NAME, exchange_type='topic')

    def produce(self, operation):
        self.channel.basic_publish(exchange=TOPIC_PERSIST_NAME, routing_key='#', body=json.dumps(operation))
        self.log.info("[%s] published message=%s" % (CLIENT_NAME, operation))


def set_log():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    set_log()
    logging.info("App params= [%s] [%s] [%s] [%s]", CLIENT_NAME, RABBIT_HOST, QUEUE_OPERATION_NAME, TOPIC_PERSIST_NAME)
    RemoteConnection().run()
