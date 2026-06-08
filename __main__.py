import os
import yaml
import pulumi
import pulumi_gcp as gcp

# 1. Load custom YAML configuration
config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(config_path, "r") as stream:
    try:
        config_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise Exception(f"Error parsing config.yaml: {exc}")

# 2. Extract configuration variables
gcp_project = config_data.get("project_id")
gcp_region = config_data.get("region", "us-central1")
bucket_suffix = config_data.get("bucket_name_suffix", "storage-bucket")
storage_class = config_data.get("storage_class", "STANDARD")

# 3. Explicitly configure the GCP Provider using local gcloud credentials
gcp_provider = gcp.Provider(
    "local-gcp-provider",
    project=gcp_project,
    region=gcp_region
)

# 4. Generate a unique bucket name to avoid collisions
bucket_name = f"{gcp_project}-{bucket_suffix}"

# 5. Provision the GCP Cloud Storage Bucket
storage_bucket = gcp.storage.Bucket(
    "gcp-storage-bucket",
    name=bucket_name,
    location=gcp_region,
    storage_class=storage_class,
    force_destroy=True,  # Allows deletion even if it contains objects (useful for dev)
    uniform_bucket_level_access=True,
    opts=pulumi.ResourceOptions(provider=gcp_provider)
)

# 6. Export outputs
pulumi.export("bucket_name", storage_bucket.name)
pulumi.export("bucket_url", storage_bucket.url)