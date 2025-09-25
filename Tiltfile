# Load the restart_process extension
load('ext://restart_process', 'docker_build_with_restart')

allow_k8s_contexts('^colima.*$')
# --- Configuration ---
APP_IMAGE = 'my-python-app'
APP_NAME = 'python-app'
DB_NAME = 'postgres'

# --- Docker Image Build ---
# Build the Docker image for the Python application
docker_build_with_restart(
    APP_IMAGE,
    '.',
    entrypoint=['python', '/app/main.py'],
    live_update=[
        # Sync changes from the local 'src' directory to the container's '/app/src'
        sync('./src', '/app/src'),
        # When requirements change, reinstall them without a full image rebuild
        run(
            'pip install -r requirements.txt',
            trigger='./requirements.txt'
        ),
    ]
)

# --- Kubernetes Resources ---
# Read the password from the local file. Tilt will fail with a clear error
# if this file doesn't exist, which is the desired behavior.
password = str(read_file('postgres-password.txt')).strip()

# Read the secrets YAML file, inject the password, and deploy it.
secrets_yaml = str(read_file('k8s/secrets.yaml')).replace('password: ""', 'password: "%s"' % password)
k8s_yaml(blob(secrets_yaml))


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
    k8s_upsert_timeout_secs=60,
    suppress_unused_image_warnings=['my-python-app']
)