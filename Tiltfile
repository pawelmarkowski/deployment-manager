# Load extensions directly from the official Tilt repository for robustness
load('github.com/tilt-dev/tilt-extensions/k8s_yaml/Tiltfile', 'k8s_yaml')
load('github.com/tilt-dev/tilt-extensions/docker_build/Tiltfile', 'docker_build')
load('github.com/tilt-dev/tilt-extensions/live_update/Tiltfile', 'live_update')

# --- Configuration ---
APP_IMAGE = 'my-python-app'
APP_NAME = 'python-app'
DB_NAME = 'postgres'

# --- Docker Image Build ---
# Build the Docker image for the Python application
docker_build(
    APP_IMAGE,
    '.',
    live_update=[
        # Sync changes from the local 'src' directory to the container's '/app/src'
        live_update.sync('./src', '/app/src'),
        # When requirements change, reinstall them without a full image rebuild
        live_update.run(
            'pip install -r requirements.txt',
            trigger='./requirements.txt'
        ),
        # Restart the application process when source code changes
        live_update.restart_process(
            'python main.py',
            trigger=['./src', './main.py']
        )
    ]
)

# --- Kubernetes Resources ---
# Check for the local password file and create it if it doesn't exist
if not os.path.exists('postgres-password.txt'):
    fail("File 'postgres-password.txt' not found. Please create it with your desired database password.")

# Deploy the PostgreSQL secret, injecting the password from the local file
k8s_yaml(k8s_yaml('k8s/secrets.yaml').replace('password: ""', 'password: %s' % open('postgres-password.txt').read().strip()))

# Deploy the PostgreSQL database
k8s_yaml('k8s/postgres.yaml')
k8s_resource(DB_NAME, port_forwards='5432:5432')

# Deploy the Python application
k8s_yaml('k8s/app.yaml')
k8s_resource(APP_NAME, port_forwards='50051:50051')

# Deploy the gRPC UI
k8s_yaml('k8s/grpcui.yaml')
k8s_resource('grpcui', port_forwards='8080:8080')


# --- Local Resources (Tasks) ---
# Command to seed the database. This runs once the DB is ready.
local_resource(
    'db:seed',
    cmd='python src/seed.py',
    deps=['src/seed.py', 'src/models.py'],
    resource_deps=[DB_NAME]
)

# Command to run flake8 linter
local_resource(
    'lint:flake8',
    cmd='flake8 src tests',
    deps=['src', 'tests']
)

# Command to run pylint linter
local_resource(
    'lint:pylint',
    cmd='pylint src tests',
    deps=['src', 'tests']
)

# Group the linters for a cleaner UI
update_settings(
    ui_groups=[
        {'name': 'linters', 'resources': ['lint:flake8', 'lint:pylint']},
        {'name': 'app', 'resources': [APP_NAME]},
        {'name': 'db', 'resources': [DB_NAME, 'db:seed']},
        {'name': 'ui', 'resources': ['grpcui']}
    ]
)