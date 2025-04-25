import threading
import uvicorn
import logging
from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db.base import Base, engine
from app.api.rest import images, export
from app.api.grpc.server import GrpcServer


class AppServer:
    def __init__(self):
        self.app = FastAPI(title="Image CMS API")
        self.grpc_server = GrpcServer()
        self.configure()
        
    def configure(self):
        # Create database tables
        Base.metadata.create_all(bind=engine)
        
        # Configure REST endpoints
        self.app.include_router(images.router, prefix="/api/v1", tags=["images"])
        self.app.include_router(export.router, prefix="/api/v1", tags=["export"])
        
    def start(self):
        # Start gRPC server in a separate thread
        grpc_thread = threading.Thread(target=self.grpc_server.start, daemon=True)
        grpc_thread.start()
        
        # Start REST server
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
        
    def stop(self):
        self.grpc_server.stop()