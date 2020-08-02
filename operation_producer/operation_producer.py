import pika
import json

# TODO:create a operation generator
func = {'operator': 'sub', 'operands': [60, 1, 7, 8, 8]}

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_operation')

channel.basic_publish(exchange='', routing_key='operation', body=json.dumps(func))
print(" Function sent: %s" % func)

connection.close()
