from src.generated import system_pb2
from src import models

def product_to_message(product: models.Product):
    return system_pb2.Product(
        id=product.id,
        name=product.name,
        teams=[team_to_message(t) for t in product.teams] if product.teams else []
    )

def team_to_message(team: models.Team):
    return system_pb2.Team(
        id=team.id,
        name=team.name,
        url=team.url,
        product_id=team.product_id,
        services=[service_to_message(s) for s in team.services] if team.services else []
    )

def service_to_message(service: models.Service):
    return system_pb2.Service(
        id=service.id,
        name=service.name,
        team_id=service.team_id,
        configs=[config_to_message(c) for c in service.configs] if service.configs else [],
        dependencies=[service_dependency_to_message(d) for d in service.dependencies] if service.dependencies else []
    )

def config_to_message(config: models.Config):
    return system_pb2.Config(
        id=config.id,
        name=config.name,
        url=config.url,
        service_id=config.service_id
    )

def service_dependency_to_message(dependency: models.ServiceDependency):
    return system_pb2.ServiceDependency(
        id=dependency.id,
        name=dependency.name,
        task_template=dependency.task_template,
        project_id=dependency.project_id,
        service_id=dependency.service_id,
        depends_on_service_id=dependency.depends_on_service_id,
        config_id=dependency.config_id
    )

def project_to_message(project: models.Project):
    return system_pb2.Project(
        id=project.id,
        name=project.name,
        service_dependencies=[service_dependency_to_message(d) for d in project.service_dependencies] if project.service_dependencies else [],
        templates=[template_to_message(t) for t in project.templates] if project.templates else [],
        tasks=[task_to_message(t) for t in project.tasks] if project.tasks else []
    )

def template_to_message(template: models.Template):
    return system_pb2.Template(
        id=template.id,
        name=template.name,
        service_dependency_templates=[sdt_to_message(sdt) for sdt in template.service_dependency_templates] if template.service_dependency_templates else []
    )

def sdt_to_message(sdt: models.ServiceDependencyTemplate):
    return system_pb2.ServiceDependencyTemplate(
        id=sdt.id,
        name=sdt.name,
        template_id=sdt.template_id,
        base_service_id=sdt.base_service_id,
        dependent_service_id=sdt.dependent_service_id,
        config_name=sdt.config_name
    )

def task_to_message(task: models.Task):
    return system_pb2.Task(
        id=task.id,
        name=task.name,
        project_id=task.project_id,
        team_id=task.team_id
    )