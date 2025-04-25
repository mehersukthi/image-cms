import grpc
from concurrent import futures
import logging

import image_service_pb2_grpc as pb2_grpc
from app.api.grpc.services.images import ImageServiceServicer


class GrpcServer:
    def __init__(self, port=50051):
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_ImageServiceServicer_to_server(ImageServiceServicer(), self.server)

    def start(self):
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        logging.info(f"gRPC server started on port {self.port}")
        return self

    def stop(self):
        self.server.stop(0)
        logging.info("gRPC server stopped")