from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
from google.protobuf import empty_pb2
from sqlalchemy.orm import subqueryload

from src.generated import system_pb2, system_pb2_grpc
from src.database import SessionLocal
from src import models, converters
from src.generics import GenericServicer

class ProductServicer(GenericServicer):
    def _get_load_options(self):
        return [subqueryload(models.Product.teams).subqueryload(models.Team.services)]

class TeamServicer(GenericServicer):
    def _get_load_options(self):
        return [subqueryload(models.Team.services).subqueryload(models.Service.configs)]

class ServiceServicer(GenericServicer):
    def _get_load_options(self):
        return [subqueryload(models.Service.configs), subqueryload(models.Service.dependencies)]

class ProjectServicer(GenericServicer):
    def _get_load_options(self):
        return [
            subqueryload(models.Project.service_dependencies),
            subqueryload(models.Project.templates).subqueryload(models.Template.service_dependency_templates),
            subqueryload(models.Project.tasks)
        ]

class TemplateServicer(GenericServicer):
    def _get_load_options(self):
        return [subqueryload(models.Template.service_dependency_templates)]

class SystemServicer(system_pb2_grpc.SystemServicer):
    def __init__(self, db_session_factory=SessionLocal):
        self.product_servicer = ProductServicer(models.Product, converters.product_to_message, db_session_factory)
        self.team_servicer = TeamServicer(models.Team, converters.team_to_message, db_session_factory)
        self.service_servicer = ServiceServicer(models.Service, converters.service_to_message, db_session_factory)
        self.config_servicer = GenericServicer(models.Config, converters.config_to_message, db_session_factory)
        self.sd_servicer = GenericServicer(models.ServiceDependency, converters.service_dependency_to_message, db_session_factory)
        self.project_servicer = ProjectServicer(models.Project, converters.project_to_message, db_session_factory)
        self.template_servicer = TemplateServicer(models.Template, converters.template_to_message, db_session_factory)
        self.sdt_servicer = GenericServicer(models.ServiceDependencyTemplate, converters.sdt_to_message, db_session_factory)
        self.task_servicer = GenericServicer(models.Task, converters.task_to_message, db_session_factory)

    # --- Product Methods ---
    def CreateProduct(self, request, context): return self.product_servicer.Create(request, context)
    def GetProduct(self, request, context): return self.product_servicer.Get(request, context)
    def ListProducts(self, request, context):
        db_items = self.product_servicer.List(request, context)
        return system_pb2.ListProductsResponse(products=db_items)
    def DeleteProduct(self, request, context): return self.product_servicer.Delete(request, context)

    # --- Team Methods ---
    def CreateTeam(self, request, context): return self.team_servicer.Create(request, context)
    def GetTeam(self, request, context): return self.team_servicer.Get(request, context)
    def ListTeams(self, request, context):
        db_items = self.team_servicer.List(request, context)
        return system_pb2.ListTeamsResponse(teams=db_items)
    def DeleteTeam(self, request, context): return self.team_servicer.Delete(request, context)

    # --- Service Methods ---
    def CreateService(self, request, context): return self.service_servicer.Create(request, context)
    def GetService(self, request, context): return self.service_servicer.Get(request, context)
    def ListServices(self, request, context):
        db_items = self.service_servicer.List(request, context)
        return system_pb2.ListServicesResponse(services=db_items)
    def DeleteService(self, request, context): return self.service_servicer.Delete(request, context)

    # --- Config Methods ---
    def CreateConfig(self, request, context): return self.config_servicer.Create(request, context)
    def GetConfig(self, request, context): return self.config_servicer.Get(request, context)
    def ListConfigs(self, request, context):
        db_items = self.config_servicer.List(request, context)
        return system_pb2.ListConfigsResponse(configs=db_items)
    def DeleteConfig(self, request, context): return self.config_servicer.Delete(request, context)

    # --- ServiceDependency Methods ---
    def CreateServiceDependency(self, request, context): return self.sd_servicer.Create(request, context)
    def GetServiceDependency(self, request, context): return self.sd_servicer.Get(request, context)
    def ListServiceDependencies(self, request, context):
        db_items = self.sd_servicer.List(request, context)
        return system_pb2.ListServiceDependenciesResponse(service_dependencies=db_items)
    def DeleteServiceDependency(self, request, context): return self.sd_servicer.Delete(request, context)

    # --- Project Methods ---
    def CreateProject(self, request, context): return self.project_servicer.Create(request, context)
    def GetProject(self, request, context): return self.project_servicer.Get(request, context)
    def ListProjects(self, request, context):
        db_items = self.project_servicer.List(request, context)
        return system_pb2.ListProjectsResponse(projects=db_items)
    def DeleteProject(self, request, context): return self.project_servicer.Delete(request, context)

    # --- Template Methods ---
    def CreateTemplate(self, request, context): return self.template_servicer.Create(request, context)
    def GetTemplate(self, request, context): return self.template_servicer.Get(request, context)
    def ListTemplates(self, request, context):
        db_items = self.template_servicer.List(request, context)
        return system_pb2.ListTemplatesResponse(templates=db_items)
    def DeleteTemplate(self, request, context): return self.template_servicer.Delete(request, context)

    # --- ServiceDependencyTemplate Methods ---
    def CreateServiceDependencyTemplate(self, request, context):
        db = self.sdt_servicer._get_db()
        try:
            db_sdt = models.ServiceDependencyTemplate(
                name=request.name,
                template_id=request.template_id,
                base_service_id=request.base_service_id,
                dependent_service_id=request.dependent_service_id,
                config_name=request.config_name
            )
            db.add(db_sdt)
            db.commit()
            db.refresh(db_sdt)
            return converters.sdt_to_message(db_sdt)
        finally:
            db.close()

    def GetServiceDependencyTemplate(self, request, context): return self.sdt_servicer.Get(request, context)
    def ListServiceDependencyTemplates(self, request, context):
        db_items = self.sdt_servicer.List(request, context)
        return system_pb2.ListServiceDependencyTemplatesResponse(service_dependency_templates=db_items)
    def DeleteServiceDependencyTemplate(self, request, context): return self.sdt_servicer.Delete(request, context)

    # --- Task Methods ---
    def CreateTask(self, request, context): return self.task_servicer.Create(request, context)
    def GetTask(self, request, context): return self.task_servicer.Get(request, context)
    def ListTasks(self, request, context):
        db_items = self.task_servicer.List(request, context)
        return system_pb2.ListTasksResponse(tasks=db_items)
    def DeleteTask(self, request, context): return self.task_servicer.Delete(request, context)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    system_pb2_grpc.add_SystemServicer_to_server(SystemServicer(), server)

    SERVICE_NAMES = (
        system_pb2.DESCRIPTOR.services_by_name['System'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051 with reflection enabled.")
    server.wait_for_termination()