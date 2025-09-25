import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, Product, Team, Service, Config, ServiceDependency, Project, Template, ServiceDependencyTemplate, Task

class TestModels(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.session.close()

    def test_create_product(self):
        product = Product(name="Test Product")
        self.session.add(product)
        self.session.commit()
        self.assertEqual(self.session.query(Product).count(), 1)

    def test_create_team(self):
        product = Product(name="Test Product")
        self.session.add(product)
        self.session.commit()
        team = Team(name="Test Team", url="http://example.com", product_id=product.id)
        self.session.add(team)
        self.session.commit()
        self.assertEqual(self.session.query(Team).count(), 1)
        self.assertEqual(team.product, product)

    def test_create_service(self):
        product = Product(name="Test Product")
        team = Team(name="Test Team", product=product)
        self.session.add_all([product, team])
        self.session.commit()
        service = Service(name="Test Service", team_id=team.id)
        self.session.add(service)
        self.session.commit()
        self.assertEqual(self.session.query(Service).count(), 1)
        self.assertEqual(service.team, team)

    def test_create_config(self):
        product = Product(name="Test Product")
        team = Team(name="Test Team", product=product)
        service = Service(name="Test Service", team=team)
        self.session.add_all([product, team, service])
        self.session.commit()
        config = Config(name="Test Config", url="http://config.com", service_id=service.id)
        self.session.add(config)
        self.session.commit()
        self.assertEqual(self.session.query(Config).count(), 1)
        self.assertEqual(config.service, service)

    def test_create_project(self):
        project = Project(name="Test Project")
        self.session.add(project)
        self.session.commit()
        self.assertEqual(self.session.query(Project).count(), 1)

    def test_create_template(self):
        template = Template(name="Test Template")
        self.session.add(template)
        self.session.commit()
        self.assertEqual(self.session.query(Template).count(), 1)

    def test_create_service_dependency(self):
        product = Product(name="Test Product")
        team1 = Team(name="Team 1", product=product)
        team2 = Team(name="Team 2", product=product)
        service1 = Service(name="Service 1", team=team1)
        service2 = Service(name="Service 2", team=team2)
        project = Project(name="Test Project")
        config = Config(name="Test Config", service=service1)

        self.session.add_all([product, team1, team2, service1, service2, project, config])
        self.session.commit()

        dependency = ServiceDependency(
            name="Test Dependency",
            project_id=project.id,
            service_id=service1.id,
            depends_on_service_id=service2.id,
            config_id=config.id
        )
        self.session.add(dependency)
        self.session.commit()

        self.assertEqual(self.session.query(ServiceDependency).count(), 1)
        self.assertEqual(dependency.project, project)
        self.assertEqual(dependency.service, service1)
        self.assertEqual(dependency.dependent_service, service2)
        self.assertEqual(dependency.config, config)

    def test_create_service_dependency_template(self):
        template = Template(name="Test Template")
        self.session.add(template)
        self.session.commit()

        sdt = ServiceDependencyTemplate(
            name="Test SDT",
            template_id=template.id,
            service_name="Service A",
            depends_on_service_name="Service B",
            config_name="Config X"
        )
        self.session.add(sdt)
        self.session.commit()
        self.assertEqual(self.session.query(ServiceDependencyTemplate).count(), 1)
        self.assertEqual(sdt.template, template)

    def test_create_task(self):
        product = Product(name="Test Product")
        team = Team(name="Test Team", product=product)
        project = Project(name="Test Project")
        self.session.add_all([product, team, project])
        self.session.commit()

        task = Task(name="Test Task", project_id=project.id, team_id=team.id)
        self.session.add(task)
        self.session.commit()
        self.assertEqual(self.session.query(Task).count(), 1)
        self.assertEqual(task.project, project)
        self.assertEqual(task.team, team)

if __name__ == '__main__':
    unittest.main()