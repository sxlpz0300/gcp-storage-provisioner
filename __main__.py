import os
import yaml
import pulumi
import pulumi_gcp as gcp
from modules import MedallionStorage, OrchestratorComposer

# 1. Load Dynamic Configuration Environment File
env_config_file = os.getenv("PULUMI_CONFIG_FILE", "config/dev.yaml")
config_path = os.path.join(os.path.dirname(__file__), env_config_file)

with open(config_path, "r") as stream:
    try:
        config_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise Exception(f"Failed to parse configuration file: {exc}")

# 2. Extract Base Parameters
gcp_project = config_data.get("project_id")
gcp_region = config_data.get("region")
environment = config_data.get("environment")

# 3. Initialize Provider using Impersonation Strategy
gcp_provider = gcp.Provider(
    "impersonated-gcp-provider",
    project=gcp_project,
    region=gcp_region
)

# Resource options passing the standard provider inherited locally
resource_opts = pulumi.ResourceOptions(provider=gcp_provider)

# 4. Provision Medallion Storage Component
storage_infrastructure = MedallionStorage(
    name="medallion-data-lake",
    project_id=gcp_project,
    region=gcp_region,
    env=environment,
    layers=config_data.get("storage_layers", []),
    opts=resource_opts
)

# 5. Provision Cloud Composer Component
orchestration_infrastructure = OrchestratorComposer(
    name="workflow-orchestrator",
    project_id=gcp_project,
    region=gcp_region,
    env=environment,
    config=config_data.get("composer_env", {}),
    opts=resource_opts
)

# 6. Global Platform Exports
pulumi.export("deployed_environment", environment)
pulumi.export("storage_buckets", storage_infrastructure.bucket_outputs)
pulumi.export("composer_env_name", orchestration_infrastructure.composer_name)
pulumi.export("airflow_ui_url", orchestration_infrastructure.airflow_uri)