import unittest
import grpc
from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.server import SystemServicer
from src.generated import system_pb2, system_pb2_grpc
from src.models import Base

class TestServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use an in-memory SQLite database for testing with a static connection pool
        cls.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

        # Create tables
        Base.metadata.create_all(cls.engine)

        # Start the server with the test session factory
        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicer = SystemServicer(db_session_factory=cls.TestingSessionLocal)
        system_pb2_grpc.add_SystemServicer_to_server(servicer, cls.server)
        cls.server.add_insecure_port('[::]:50052')  # Use a different port for testing
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(0)
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        self.channel = grpc.insecure_channel('localhost:50052')
        self.stub = system_pb2_grpc.SystemStub(self.channel)
        # Clear data from tables before each test
        with self.engine.begin() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                connection.execute(table.delete())

    def tearDown(self):
        self.channel.close()

    def test_product_service(self):
        # Test CreateProduct
        create_request = system_pb2.CreateProductRequest(name="New Product")
        create_response = self.stub.CreateProduct(create_request)
        self.assertEqual(create_response.name, "New Product")
        self.assertIsNotNone(create_response.id)

        # Test GetProduct
        get_request = system_pb2.GetProductRequest(id=create_response.id)
        get_response = self.stub.GetProduct(get_request)
        self.assertEqual(get_response.id, create_response.id)
        self.assertEqual(get_response.name, "New Product")

    def test_team_service(self):
        # First, create a product to associate the team with
        product_req = system_pb2.CreateProductRequest(name="Associated Product")
        product_res = self.stub.CreateProduct(product_req)

        # Test CreateTeam
        create_request = system_pb2.CreateTeamRequest(name="New Team", url="http://team.com", product_id=product_res.id)
        create_response = self.stub.CreateTeam(create_request)
        self.assertEqual(create_response.name, "New Team")
        self.assertEqual(create_response.url, "http://team.com")
        self.assertEqual(create_response.product_id, product_res.id)

        # Test GetTeam
        get_request = system_pb2.GetTeamRequest(id=create_response.id)
        get_response = self.stub.GetTeam(get_request)
        self.assertEqual(get_response.id, create_response.id)
        self.assertEqual(get_response.name, "New Team")

    def test_service_service(self):
        # Create a product and a team first
        product_res = self.stub.CreateProduct(system_pb2.CreateProductRequest(name="P"))
        team_res = self.stub.CreateTeam(system_pb2.CreateTeamRequest(name="T", product_id=product_res.id))

        # Test CreateService
        create_request = system_pb2.CreateServiceRequest(name="New Service", team_id=team_res.id)
        create_response = self.stub.CreateService(create_request)
        self.assertEqual(create_response.name, "New Service")
        self.assertEqual(create_response.team_id, team_res.id)

        # Test GetService
        get_request = system_pb2.GetServiceRequest(id=create_response.id)
        get_response = self.stub.GetService(get_request)
        self.assertEqual(get_response.id, create_response.id)
        self.assertEqual(get_response.name, "New Service")

    def test_config_service(self):
        # Create dependencies
        product_res = self.stub.CreateProduct(system_pb2.CreateProductRequest(name="P"))
        team_res = self.stub.CreateTeam(system_pb2.CreateTeamRequest(name="T", product_id=product_res.id))
        service_res = self.stub.CreateService(system_pb2.CreateServiceRequest(name="S", team_id=team_res.id))

        # Test CreateConfig
        create_request = system_pb2.CreateConfigRequest(name="New Config", url="http://config.io", service_id=service_res.id)
        create_response = self.stub.CreateConfig(create_request)
        self.assertEqual(create_response.name, "New Config")
        self.assertEqual(create_response.service_id, service_res.id)

        # Test GetConfig
        get_request = system_pb2.GetConfigRequest(id=create_response.id)
        get_response = self.stub.GetConfig(get_request)
        self.assertEqual(get_response.id, create_response.id)

    def test_project_service(self):
        create_req = system_pb2.CreateProjectRequest(name="New Project")
        create_res = self.stub.CreateProject(create_req)
        self.assertEqual(create_res.name, "New Project")

        get_req = system_pb2.GetProjectRequest(id=create_res.id)
        get_res = self.stub.GetProject(get_req)
        self.assertEqual(get_res.id, create_res.id)

    def test_template_service(self):
        create_req = system_pb2.CreateTemplateRequest(name="New Template")
        create_res = self.stub.CreateTemplate(create_req)
        self.assertEqual(create_res.name, "New Template")

        get_req = system_pb2.GetTemplateRequest(id=create_res.id)
        get_res = self.stub.GetTemplate(get_req)
        self.assertEqual(get_res.id, create_res.id)

if __name__ == '__main__':
    unittest.main()