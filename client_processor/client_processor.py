from __future__ import print_function
from functools import reduce

import json
import logging
import uuid
import sys
import os

import grpc
import pika

import server_pb2
import server_pb2_grpc

'''Below attributes must exist otherwise application should halt'''
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
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE_OPERATION_NAME)

    def read_queue(self):
        self.channel.basic_consume(queue=QUEUE_OPERATION_NAME, on_message_callback=self.process_operation, auto_ack=True)
        self.channel.start_consuming()

    @staticmethod
    def process_operation(ch, method, properties, body):
        print("%s - received %s %s %s %r" % (CLIENT_NAME, body, ch, method, properties))
        func = json.loads(body)
        result = MathOperation().calc(func)
        ClientPersistenceProducer().produce(result)


class ClientPersistenceProducer:
    def __init__(self, *args, **kwargs):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=TOPIC_PERSIST_NAME, exchange_type='topic')

    def produce(self, func):
        self.channel.basic_publish(exchange=TOPIC_PERSIST_NAME, routing_key='#', body=json.dumps(func))


class MathOperation:
    func_mapping = {'sum': lambda x, y: x + y,
                    'sub': lambda x, y: x - y,
                    'mul': lambda x, y: x * y,
                    'div': lambda x, y: x / y}

    def calc(self, func):
        result = 0
        status = 'fail'
        try:
            operand = self.func_mapping[func['operator']]
            result = reduce(operand, func['operands'])
            status = 'success'
        except ArithmeticError as ae:
            result = ae.__str__()
        except KeyError as ke:
            result = 'Operator %s not supported:' % ke.__str__()
            print("Operator %s not supported!" % func['operator'])
        except TypeError:
            result = 'Operands %s not supported:' % func['operands']
            print("Operands %s not supported!" % func['operands'])
        except:
            result = 'generic error'
            print("Generic error.")
        finally:
            func['result'] = result
            func['status'] = status
            func['uid'] = uuid.uuid4().__str__();
            return func


if __name__ == '__main__':
    logging.basicConfig()
    print("App params=", CLIENT_NAME, RABBIT_HOST, QUEUE_OPERATION_NAME, TOPIC_PERSIST_NAME)
    RemoteConnection().run()
