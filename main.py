from src.server import serve
from src.database import init_db
from src.seed import seed_data

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Seeding database...")
    seed_data()
    print("Starting gRPC server on port 50051...")
    serve()