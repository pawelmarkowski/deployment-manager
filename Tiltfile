allow_k8s_contexts('^colima.*$')

# --- Configuration ---
GRPC_APP_IMAGE = 'my-python-app'
GRPC_APP_NAME = 'python-app'
WEB_UI_IMAGE = 'my-web-ui'
WEB_UI_NAME = 'web-ui'
DB_NAME = 'postgres'

# --- Docker Image Builds ---
docker_build(
    GRPC_APP_IMAGE,
    '.',
    dockerfile='Dockerfile',
    live_update=[
        sync('./src', '/app/src'),
        sync('./main.py', '/app/main.py'),
        run('pip install -r requirements.txt', trigger='./requirements.txt')
    ]
)

docker_build(
    WEB_UI_IMAGE,
    '.',
    dockerfile='web_ui/Dockerfile',
    live_update=[
        sync('./web_ui', '/app/web_ui'),
        sync('./src', '/app/src'),
        run('pip install -r requirements.txt', trigger='./requirements.txt')
    ]
)

# --- Kubernetes Resources ---
password = str(read_file('postgres-password.txt')).strip()
secrets_yaml = str(read_file('k8s/secrets.yaml')).replace('password: ""', 'password: "%s"' % password)
k8s_yaml(blob(secrets_yaml))

k8s_yaml('k8s/postgres.yaml')
k8s_resource(DB_NAME, port_forwards='5432:5432')

k8s_yaml('k8s/app.yaml')
k8s_resource(GRPC_APP_NAME, port_forwards='50051:50051')

k8s_yaml('k8s/grpcui.yaml')
k8s_resource('grpcui', port_forwards='8080:8080')

k8s_yaml('k8s/web-ui.yaml')
k8s_resource(WEB_UI_NAME, port_forwards='8000:8000')

# --- Kubernetes Job for Seeding ---
k8s_yaml('k8s/seeder-job.yaml')
k8s_resource('db-seeder', resource_deps=[DB_NAME])

# --- Local Resources (Tasks) ---
local_resource(
    'lint:flake8',
    cmd='flake8 src tests web_ui',
    deps=['src', 'tests', 'web_ui']
)

local_resource(
    'lint:pylint',
    cmd='pylint src tests web_ui',
    deps=['src', 'tests', 'web_ui']
)

# Group the linters for a cleaner UI
update_settings(
    k8s_upsert_timeout_secs=60,
    suppress_unused_image_warnings=[GRPC_APP_IMAGE, WEB_UI_IMAGE]
)