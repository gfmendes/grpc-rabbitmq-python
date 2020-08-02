# Code challlenge

## External Dependencies
RabbitMQ
- pika 

MongoDB 
- pymongo

gRPC
- grpcio
- grpcio-tools
- protobuf

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