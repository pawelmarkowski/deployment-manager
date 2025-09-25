import unittest
import grpc
from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.server import SystemServicer
from src.generated import system_pb2, system_pb2_grpc
from src.models import Base
from src import database

class TestServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

        Base.metadata.create_all(cls.engine)

        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicer = SystemServicer(db_session_factory=cls.TestingSessionLocal)
        system_pb2_grpc.add_SystemServicer_to_server(servicer, cls.server)
        cls.server.add_insecure_port('[::]:50052')
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(0)
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        self.channel = grpc.insecure_channel('localhost:50052')
        self.stub = system_pb2_grpc.SystemStub(self.channel)
        with self.engine.begin() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                connection.execute(table.delete())

    def tearDown(self):
        self.channel.close()

    def test_product_lifecycle_and_relationships(self):
        # 1. Create a Product
        product_res = self.stub.CreateProduct(system_pb2.CreateProductRequest(name="DevOps Platform"))
        self.assertEqual(product_res.name, "DevOps Platform")
        self.assertEqual(len(product_res.teams), 0) # Should have no teams initially

        # 2. Create a Team for that Product
        team_res = self.stub.CreateTeam(system_pb2.CreateTeamRequest(name="SRE Team", product_id=product_res.id))
        self.assertEqual(team_res.name, "SRE Team")

        # 3. Get the Product again and verify it now contains the new Team
        get_product_res = self.stub.GetProduct(system_pb2.GetProductRequest(id=product_res.id))
        self.assertEqual(len(get_product_res.teams), 1)
        self.assertEqual(get_product_res.teams[0].id, team_res.id)
        self.assertEqual(get_product_res.teams[0].name, "SRE Team")

        # 4. List all products
        list_products_res = self.stub.ListProducts(system_pb2.ListProductsRequest())
        self.assertEqual(len(list_products_res.products), 1)
        self.assertEqual(list_products_res.products[0].name, "DevOps Platform")
        self.assertEqual(len(list_products_res.products[0].teams), 1) # Verify nested object in list

        # 5. Delete the Team
        self.stub.DeleteTeam(system_pb2.DeleteTeamRequest(id=team_res.id))

        # 6. Get the Product again and verify the team is gone
        get_product_res_after_delete = self.stub.GetProduct(system_pb2.GetProductRequest(id=product_res.id))
        self.assertEqual(len(get_product_res_after_delete.teams), 0)

        # 7. Delete the Product
        self.stub.DeleteProduct(system_pb2.DeleteProductRequest(id=product_res.id))

        # 8. Verify the product is deleted
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.GetProduct(system_pb2.GetProductRequest(id=product_res.id))
        self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

if __name__ == '__main__':
    unittest.main()