import grpc
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.generated import system_pb2, system_pb2_grpc

app = FastAPI()

# --- Setup ---
app.mount("/static", StaticFiles(directory="web_ui/static"), name="static")
templates = Jinja2Templates(directory="web_ui/templates")

GRPC_TARGET = os.environ.get("GRPC_CHANNEL_TARGET", "localhost:50051")
GRPC_CHANNEL = grpc.insecure_channel(GRPC_TARGET)
STUB = system_pb2_grpc.SystemStub(GRPC_CHANNEL)

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Product Routes ---
@app.get("/products", response_class=HTMLResponse)
async def list_products(request: Request, search: str = ""):
    product_list = STUB.ListProducts(system_pb2.ListProductsRequest())
    filtered_products = [p for p in product_list.products if search.lower() in p.name.lower()]
    return templates.TemplateResponse("products_list.html", {"request": request, "products": filtered_products, "search": search})

@app.post("/products", response_class=HTMLResponse)
async def create_product(request: Request, name: str = Form(...)):
    if name:
        STUB.CreateProduct(system_pb2.CreateProductRequest(name=name))
    return await list_products(request)

@app.get("/products/{product_id}", response_class=HTMLResponse)
async def get_product(request: Request, product_id: int):
    product = STUB.GetProduct(system_pb2.GetProductRequest(id=product_id))
    return templates.TemplateResponse("product_detail.html", {"request": request, "product": product})

# --- Team Routes ---
@app.get("/teams", response_class=HTMLResponse)
async def list_teams(request: Request, search: str = ""):
    team_list = STUB.ListTeams(system_pb2.ListTeamsRequest())
    filtered_teams = [t for t in team_list.teams if search.lower() in t.name.lower()]
    product_list = STUB.ListProducts(system_pb2.ListProductsRequest())
    return templates.TemplateResponse("teams_list.html", {"request": request, "teams": filtered_teams, "products": product_list.products, "search": search})

@app.post("/teams", response_class=HTMLResponse)
async def create_team(request: Request, name: str = Form(...), product_id: int = Form(...)):
    if name and product_id:
        STUB.CreateTeam(system_pb2.CreateTeamRequest(name=name, product_id=product_id))
    return await list_teams(request)

# --- Service Routes ---
@app.get("/services", response_class=HTMLResponse)
async def list_services(request: Request):
    service_list = STUB.ListServices(system_pb2.ListServicesRequest())
    team_list = STUB.ListTeams(system_pb2.ListTeamsRequest())
    return templates.TemplateResponse("services_list.html", {"request": request, "services": service_list.services, "teams": team_list.teams})

@app.post("/services", response_class=HTMLResponse)
async def create_service(request: Request, name: str = Form(...), team_id: int = Form(...)):
    if name and team_id:
        STUB.CreateService(system_pb2.CreateServiceRequest(name=name, team_id=team_id))
    return await list_services(request)

# --- Config Routes ---
@app.get("/configs", response_class=HTMLResponse)
async def list_configs(request: Request):
    config_list = STUB.ListConfigs(system_pb2.ListConfigsRequest())
    service_list = STUB.ListServices(system_pb2.ListServicesRequest())
    return templates.TemplateResponse("configs_list.html", {"request": request, "configs": config_list.configs, "services": service_list.services})

@app.post("/configs", response_class=HTMLResponse)
async def create_config(request: Request, name: str = Form(...), url: str = Form(...), service_id: int = Form(...)):
    if name and service_id:
        STUB.CreateConfig(system_pb2.CreateConfigRequest(name=name, url=url, service_id=service_id))
    return await list_configs(request)

# --- Project Routes ---
@app.get("/projects", response_class=HTMLResponse)
async def list_projects(request: Request):
    project_list = STUB.ListProjects(system_pb2.ListProjectsRequest())
    return templates.TemplateResponse("projects_list.html", {"request": request, "projects": project_list.projects})

@app.post("/projects", response_class=HTMLResponse)
async def create_project(request: Request, name: str = Form(...)):
    if name:
        STUB.CreateProject(system_pb2.CreateProjectRequest(name=name))
    return await list_projects(request)

# --- Template Routes ---
@app.get("/templates", response_class=HTMLResponse)
async def list_templates(request: Request):
    template_list = STUB.ListTemplates(system_pb2.ListTemplatesRequest())
    return templates.TemplateResponse("templates_list.html", {"request": request, "templates": template_list.templates})

@app.post("/templates", response_class=HTMLResponse)
async def create_template(request: Request, name: str = Form(...)):
    if name:
        STUB.CreateTemplate(system_pb2.CreateTemplateRequest(name=name))
    return await list_templates(request)

# --- Service Dependency Routes ---
@app.get("/service-dependencies", response_class=HTMLResponse)
async def list_service_dependencies(request: Request):
    sd_list = STUB.ListServiceDependencies(system_pb2.ListServiceDependenciesRequest())
    project_list = STUB.ListProjects(system_pb2.ListProjectsRequest())
    service_list = STUB.ListServices(system_pb2.ListServicesRequest())
    config_list = STUB.ListConfigs(system_pb2.ListConfigsRequest())
    return templates.TemplateResponse("service_dependencies_list.html", {"request": request, "service_dependencies": sd_list.service_dependencies, "projects": project_list.projects, "services": service_list.services, "configs": config_list.configs})

@app.post("/service-dependencies", response_class=HTMLResponse)
async def create_service_dependency(request: Request, name: str = Form(...), project_id: int = Form(...), service_id: int = Form(...), depends_on_service_id: int = Form(...), config_id: int = Form(...)):
    if name:
        STUB.CreateServiceDependency(system_pb2.CreateServiceDependencyRequest(name=name, project_id=project_id, service_id=service_id, depends_on_service_id=depends_on_service_id, config_id=config_id))
    return await list_service_dependencies(request)

# --- Service Dependency Template Routes ---
@app.get("/service-dependency-templates", response_class=HTMLResponse)
async def list_sdt(request: Request):
    sdt_list = STUB.ListServiceDependencyTemplates(system_pb2.ListServiceDependencyTemplatesRequest())
    template_list = STUB.ListTemplates(system_pb2.ListTemplatesRequest())
    service_list = STUB.ListServices(system_pb2.ListServicesRequest())
    return templates.TemplateResponse("service_dependency_templates_list.html", {"request": request, "service_dependency_templates": sdt_list.service_dependency_templates, "templates": template_list.templates, "services": service_list.services})

@app.post("/service-dependency-templates", response_class=HTMLResponse)
async def create_sdt(request: Request, name: str = Form(...), template_id: int = Form(...), base_service_id: int = Form(...), dependent_service_id: int = Form(...), config_name: str = Form(...)):
    if name:
        STUB.CreateServiceDependencyTemplate(system_pb2.CreateServiceDependencyTemplateRequest(name=name, template_id=template_id, base_service_id=base_service_id, dependent_service_id=dependent_service_id, config_name=config_name))
    return await list_sdt(request)