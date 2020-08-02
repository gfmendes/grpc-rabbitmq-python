# Code challlenge

<pre>
The solution consists in three apps (server_app, client_processor and client_persistence that can be deployed independently and/or in different nodes/servers/containers.
client_processor comunicates with server_app using RPC protocol
client_processor consumes from a queue the data to process the calculation, then produces in a persistence topic. 
client_persistence consumes from persistence topic and updates the database instance bounded to it.

Complementary modules:
math_operation.py module contains "business rules" and a test case to it.
server_pb2.py and server_pb2_grpc.py are auto generated classes from gRPOC tool. They need to be packaged in both server_app and client_processor applications.
server.proto is proto3 class which defines server and client RPC communication.
</pre>

## External Dependencies
<pre>
RabbitMQ
- pika 

MongoDB 
- pymongo

gRPC
- grpcio
- grpcio-tools
- protobuf
</pre>

## To gerenate gRPC files:
<pre>
<b>cd server_app
python -m grpc_tools.protoc -I ../protos --python_out=. --grpc_python_out=.  ../protos/server.proto

cd client_processor
python -m grpc_tools.protoc -I ../protos --python_out=. --grpc_python_out=.  ../protos/server.proto
</b>
</pre>

## Running the solution:
<pre>
Setting up env properties:
<b>export APP_GRPC_SERVER_URL=localhost:50051
export APP_RABBITMQ_HOST=localhost
export APP_RABBITMQ_QUEUE_OPERATION_NAME=queue_operation
export APP_RABBITMQ_TOPIC_PERSIST_NAME=topic_persistence
export APP_MONGO_CONNECTION_STR="mongodb+srv://boticario-dev:Dummypasswd@cluster0-zmuno.mongodb.net/newtonai?retryWrites=true&w=majority"
</b>

Init RabbitMQ:
<b>sudo service rabbitmq-server restart</b>

Start the server:
<b>python server_app/server_app.py</b>

Start client processor:
<b>python client_processor/client_processor.py [client_name]</b>

Start client persistence  
<b>python client_persistence/client_persistence.py [client_name]</b>

To produce operations:
<b>python operation_producer/operation_producer.py</b>

</pre>

## Unit testing
<pre>
math_operation module is covered with unit testing:

<b>python -m unittest client_processor/test_math_operation.py</b>
</pre>
