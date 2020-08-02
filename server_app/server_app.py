from concurrent import futures
import logging

import grpc

import server_pb2
import server_pb2_grpc


class Server(server_pb2_grpc.ConnectionServicer):

    def Connect(self, request, context):
        print('A new connection request from %s with context %s' % (request.name, context))
        return server_pb2.ConnectionReply(result='true')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ConnectionServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server is running!')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
