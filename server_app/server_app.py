from concurrent import futures
import logging

import grpc

import server_pb2
import server_pb2_grpc


class Server(server_pb2_grpc.ConnectionServicer):

    def Connect(self, request, context):
        logging.info('A new connection request from %s' % request.name)
        return server_pb2.ConnectionReply(result='true')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ConnectionServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server app is running.")
    server.wait_for_termination()


def set_log():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    set_log()
    serve()
