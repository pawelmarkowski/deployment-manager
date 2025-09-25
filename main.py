from src.server import serve
from src.database import init_db
if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Starting gRPC server on port 50051...")
    serve()