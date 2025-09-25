from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
from src.generated import system_pb2
from src.generated import system_pb2_grpc
from src.database import SessionLocal
from src import models

class SystemServicer(system_pb2_grpc.SystemServicer):
    def __init__(self, db_session_factory=SessionLocal):
        self.db_session_factory = db_session_factory

    def _get_db(self):
        return self.db_session_factory()

    def CreateProduct(self, request, context):
        db = self._get_db()
        try:
            db_product = models.Product(name=request.name)
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return system_pb2.Product(id=db_product.id, name=db_product.name)
        finally:
            db.close()

    def GetProduct(self, request, context):
        db = self._get_db()
        try:
            db_product = db.query(models.Product).filter(models.Product.id == request.id).first()
            if db_product is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Product not found')
                return system_pb2.Product()
            return system_pb2.Product(id=db_product.id, name=db_product.name)
        finally:
            db.close()

    def CreateTeam(self, request, context):
        db = self._get_db()
        try:
            db_team = models.Team(name=request.name, url=request.url, product_id=request.product_id)
            db.add(db_team)
            db.commit()
            db.refresh(db_team)
            return system_pb2.Team(id=db_team.id, name=db_team.name, url=db_team.url, product_id=db_team.product_id)
        finally:
            db.close()

    def GetTeam(self, request, context):
        db = self._get_db()
        try:
            db_team = db.query(models.Team).filter(models.Team.id == request.id).first()
            if db_team is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Team not found')
                return system_pb2.Team()
            return system_pb2.Team(id=db_team.id, name=db_team.name, url=db_team.url, product_id=db_team.product_id)
        finally:
            db.close()

    def CreateService(self, request, context):
        db = self._get_db()
        try:
            db_service = models.Service(name=request.name, team_id=request.team_id)
            db.add(db_service)
            db.commit()
            db.refresh(db_service)
            return system_pb2.Service(id=db_service.id, name=db_service.name, team_id=db_service.team_id)
        finally:
            db.close()

    def GetService(self, request, context):
        db = self._get_db()
        try:
            db_service = db.query(models.Service).filter(models.Service.id == request.id).first()
            if db_service is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Service not found')
                return system_pb2.Service()
            return system_pb2.Service(id=db_service.id, name=db_service.name, team_id=db_service.team_id)
        finally:
            db.close()

    def CreateConfig(self, request, context):
        db = self._get_db()
        try:
            db_config = models.Config(name=request.name, url=request.url, service_id=request.service_id)
            db.add(db_config)
            db.commit()
            db.refresh(db_config)
            return system_pb2.Config(id=db_config.id, name=db_config.name, url=db_config.url, service_id=db_config.service_id)
        finally:
            db.close()

    def GetConfig(self, request, context):
        db = self._get_db()
        try:
            db_config = db.query(models.Config).filter(models.Config.id == request.id).first()
            if db_config is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Config not found')
                return system_pb2.Config()
            return system_pb2.Config(id=db_config.id, name=db_config.name, url=db_config.url, service_id=db_config.service_id)
        finally:
            db.close()

    def CreateServiceDependency(self, request, context):
        db = self._get_db()
        try:
            db_sd = models.ServiceDependency(
                name=request.name, task_template=request.task_template, project_id=request.project_id,
                service_id=request.service_id, depends_on_service_id=request.depends_on_service_id,
                config_id=request.config_id
            )
            db.add(db_sd)
            db.commit()
            db.refresh(db_sd)
            return system_pb2.ServiceDependency(
                id=db_sd.id, name=db_sd.name, task_template=db_sd.task_template, project_id=db_sd.project_id,
                service_id=db_sd.service_id, depends_on_service_id=db_sd.depends_on_service_id,
                config_id=db_sd.config_id
            )
        finally:
            db.close()

    def GetServiceDependency(self, request, context):
        db = self._get_db()
        try:
            db_sd = db.query(models.ServiceDependency).filter(models.ServiceDependency.id == request.id).first()
            if db_sd is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('ServiceDependency not found')
                return system_pb2.ServiceDependency()
            return system_pb2.ServiceDependency(
                id=db_sd.id, name=db_sd.name, task_template=db_sd.task_template, project_id=db_sd.project_id,
                service_id=db_sd.service_id, depends_on_service_id=db_sd.depends_on_service_id,
                config_id=db_sd.config_id
            )
        finally:
            db.close()

    def CreateProject(self, request, context):
        db = self._get_db()
        try:
            db_project = models.Project(name=request.name)
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return system_pb2.Project(id=db_project.id, name=db_project.name)
        finally:
            db.close()

    def GetProject(self, request, context):
        db = self._get_db()
        try:
            db_project = db.query(models.Project).filter(models.Project.id == request.id).first()
            if db_project is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Project not found')
                return system_pb2.Project()
            return system_pb2.Project(id=db_project.id, name=db_project.name)
        finally:
            db.close()

    def CreateTemplate(self, request, context):
        db = self._get_db()
        try:
            db_template = models.Template(name=request.name)
            db.add(db_template)
            db.commit()
            db.refresh(db_template)
            return system_pb2.Template(id=db_template.id, name=db_template.name)
        finally:
            db.close()

    def GetTemplate(self, request, context):
        db = self._get_db()
        try:
            db_template = db.query(models.Template).filter(models.Template.id == request.id).first()
            if db_template is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Template not found')
                return system_pb2.Template()
            return system_pb2.Template(id=db_template.id, name=db_template.name)
        finally:
            db.close()

    def CreateServiceDependencyTemplate(self, request, context):
        db = self._get_db()
        try:
            db_sdt = models.ServiceDependencyTemplate(
                name=request.name, template_id=request.template_id, service_name=request.service_name,
                depends_on_service_name=request.depends_on_service_name, config_name=request.config_name
            )
            db.add(db_sdt)
            db.commit()
            db.refresh(db_sdt)
            return system_pb2.ServiceDependencyTemplate(
                id=db_sdt.id, name=db_sdt.name, template_id=db_sdt.template_id, service_name=db_sdt.service_name,
                depends_on_service_name=db_sdt.depends_on_service_name, config_name=db_sdt.config_name
            )
        finally:
            db.close()

    def GetServiceDependencyTemplate(self, request, context):
        db = self._get_db()
        try:
            db_sdt = db.query(models.ServiceDependencyTemplate).filter(models.ServiceDependencyTemplate.id == request.id).first()
            if db_sdt is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('ServiceDependencyTemplate not found')
                return system_pb2.ServiceDependencyTemplate()
            return system_pb2.ServiceDependencyTemplate(
                id=db_sdt.id, name=db_sdt.name, template_id=db_sdt.template_id, service_name=db_sdt.service_name,
                depends_on_service_name=db_sdt.depends_on_service_name, config_name=db_sdt.config_name
            )
        finally:
            db.close()

    def CreateTask(self, request, context):
        db = self._get_db()
        try:
            db_task = models.Task(name=request.name, project_id=request.project_id, team_id=request.team_id)
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return system_pb2.Task(id=db_task.id, name=db_task.name, project_id=db_task.project_id, team_id=db_task.team_id)
        finally:
            db.close()

    def GetTask(self, request, context):
        db = self._get_db()
        try:
            db_task = db.query(models.Task).filter(models.Task.id == request.id).first()
            if db_task is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Task not found')
                return system_pb2.Task()
            return system_pb2.Task(id=db_task.id, name=db_task.name, project_id=db_task.project_id, team_id=db_task.team_id)
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    system_pb2_grpc.add_SystemServicer_to_server(SystemServicer(), server)

    # Enable reflection
    SERVICE_NAMES = (
        system_pb2.DESCRIPTOR.services_by_name['System'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051 with reflection enabled.")
    server.wait_for_termination()