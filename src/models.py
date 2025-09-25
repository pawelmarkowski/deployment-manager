from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for Project and Template (many-to-many)
project_template_association = Table('project_template', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('template_id', Integer, ForeignKey('templates.id'))
)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teams = relationship("Team", back_populates="product")

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="teams")
    services = relationship("Service", back_populates="team")
    tasks = relationship("Task", back_populates="team")

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="services")
    configs = relationship("Config", back_populates="service")
    # A service can be a dependency for other services
    dependent_services = relationship("ServiceDependency", foreign_keys='ServiceDependency.depends_on_service_id', back_populates="dependent_service")
    # A service can have many dependencies
    dependencies = relationship("ServiceDependency", foreign_keys='ServiceDependency.service_id', back_populates="service")


class Config(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship("Service", back_populates="configs")
    service_dependencies = relationship("ServiceDependency", back_populates="config")

class ServiceDependency(Base):
    __tablename__ = 'service_dependencies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    task_template = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="service_dependencies")

    service_id = Column(Integer, ForeignKey('services.id')) # The service that has a dependency
    service = relationship("Service", foreign_keys=[service_id], back_populates="dependencies")

    depends_on_service_id = Column(Integer, ForeignKey('services.id')) # The service it depends on
    dependent_service = relationship("Service", foreign_keys=[depends_on_service_id], back_populates="dependent_services")

    config_id = Column(Integer, ForeignKey('configs.id'))
    config = relationship("Config", back_populates="service_dependencies")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    service_dependencies = relationship("ServiceDependency", back_populates="project")
    templates = relationship("Template", secondary=project_template_association, back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    projects = relationship("Project", secondary=project_template_association, back_populates="templates")
    service_dependency_templates = relationship("ServiceDependencyTemplate", back_populates="template")

class ServiceDependencyTemplate(Base):
    __tablename__ = 'service_dependency_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # e.g., "full access control"
    template_id = Column(Integer, ForeignKey('templates.id'))
    template = relationship("Template", back_populates="service_dependency_templates")

    base_service_id = Column(Integer, ForeignKey('services.id'))
    base_service = relationship("Service", foreign_keys=[base_service_id])

    dependent_service_id = Column(Integer, ForeignKey('services.id'))
    dependent_service = relationship("Service", foreign_keys=[dependent_service_id])

    config_name = Column(String)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="tasks")

# Example of how to create an engine and session
# DATABASE_URL = "postgresql://user:password@localhost/mydatabase"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)